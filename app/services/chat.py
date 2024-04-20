import uuid
from typing import List

from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from app.schemas import db_schemas
from app.common.azure import get_chat_result
from app.schemas.data_schemas import GptContentObj
from app.schemas.request_schemas import ChatTextRequest
from app.schemas.response_schemas import ChatTextResponse
from app.models.chat import ChatSession, ChatMessage, ChatRole
from app.crud.crud_chat import crud_chat_session, crud_chat_role, crud_chat_message


def _create_chat_session(db: Session) -> ChatSession:
    """建立 chat session 資料到 chat_session table

    session_id 會使用 uuid 自動生成

    Args:
        db: ORM Session

    Returns:
        回傳一個建立完成的 `ChatSession` 實例
    """

    session_id = str(uuid.uuid4())

    obj_in = db_schemas.CreateChatSession(id=session_id)

    db_obj = crud_chat_session.create(db=db, obj_in=obj_in)

    return db_obj


def _create_chat_message(
    db: Session, *, chat_session_obj: ChatSession, chat_role_obj: ChatRole, message: str
) -> ChatMessage:
    """建立 chat message 到 chat_message table

    Args:
        db: ORM Session
        chat_session_obj: `ChatSession` model 實例 (建立與 chat_session table 的一對多關係)
        role_name: `ChatRole` model 實例 (建立與 chat_role table 的一對多關係)
        message: 訊息文字

    Returns:
        回傳一個建立完成的 `ChatMessage` model 實例
    """

    obj_in = db_schemas.CreateChatMessage(message=message)

    db_obj = crud_chat_message.create(
        db, chat_session_obj=chat_session_obj, chat_role_obj=chat_role_obj, obj_in=obj_in
    )

    return db_obj


def _get_gpt_input(
    role1_name: str, chat_messages1: List[str], role2_name: str, chat_messages2: List[str]
) -> List[GptContentObj]:
    """將兩個 message list 整合成一個 list，並且會根據順序排列

    像是：

    ```
    user_chat_messages = ["q1", "q2", "q3"]
    ```
    ```
    assistant_chat_messages = ["a1", "a2"]
    ```

    整理出來會變成：

    ```
    [
        {"role" : "user", "content" : "q1"},
        {"role" : "assistant", "content" : "a1"},
        ...
        {"role" : "user", "content" : "q3"}
    ]
    ```
    注意其中的 dict 會轉換成 :class:`GptContentObj` 類別的物件


    Args:
        role1_name: 第一個 chat role name
        role_messages1: chat messages list
        role2_name: 第二個 chat role name
        role_messages2: chat messages list
    """

    # pointer
    i = j = 0
    result = []

    while i < len(chat_messages1) and j < len(chat_messages2):

        obj = GptContentObj(role=role1_name, content=chat_messages1[i])
        result.append(obj)
        i += 1

        obj = GptContentObj(role=role2_name, content=chat_messages2[j])
        result.append(obj)
        j += 1

    # 處理 list 長度不一樣導致有的資料還沒被到 result 中
    while i < len(chat_messages1):

        obj = GptContentObj(role=role1_name, content=chat_messages1[i])
        result.append(obj)
        i += 1

    while j < len(chat_messages2):

        obj = GptContentObj(role=role2_name, content=chat_messages2[j])
        result.append(obj)
        j += 1

    return result


def chat(data: ChatTextRequest, db: Session) -> ChatTextResponse:
    """使用 GPT model 取得問題的答案，並將資料記錄到資料庫中

    流程：

    建立或取得 `session_id` 資料 -> 將使用者的 message 儲存到資料庫
    -> 取得 `session_id` 的歷史對話資料 -> 將歷史對話資料整理成可以餵給 gpt model 的格式
    -> 將資料喂給 gpt model 並取得結果 -> 將 model 的結果紀錄到資料庫

    目前的 role 只有兩個：
    1. user
    2. assistant

    Args:
        data: 使用者 POST 的資料
        db: ORM Session
    """

    # 先檢查有沒有傳入 session_id
    # 如果沒有，就建立一個
    if not data.session_id:

        session_db_obj = _create_chat_session(db=db)
        session_id = session_db_obj.id

    else:

        session_id = data.session_id
        session_db_obj = crud_chat_session.get(db, id=session_id)

        if session_db_obj is None:
            raise HTTPException(status_code=404, detail=f"Session id: {session_id} is not exist.")

    # 先將使用者傳入的 message 儲存到資料庫中
    # NOTE 這邊先寫死成 user
    user_role_name = "user"
    user_role_db_obj = crud_chat_role.get_by_role_name(db, name=user_role_name)

    if user_role_db_obj is None:
        raise HTTPException(
            status_code=404, detail=f"Chat role name: {user_role_name} is not exist."
        )

    _create_chat_message(
        db, chat_session_obj=session_db_obj, chat_role_obj=user_role_db_obj, message=data.message
    )

    # 取得 chat session 的歷史對話
    # 並整理成 gpt model 可以傳入的格式
    # NOTE 這邊先寫死成 assistant
    assistant_role_name = "assistant"
    assistant_role_db_obj = crud_chat_role.get_by_role_name(db, name=assistant_role_name)

    if assistant_role_db_obj is None:
        raise HTTPException(
            status_code=404, detail=f"Chat role name: {assistant_role_db_obj} is not exist."
        )

    user_role_messages = crud_chat_session.get_chat_messages_filter_with_role(
        db, id=session_id, role=user_role_db_obj
    )
    assistant_role_messages = crud_chat_session.get_chat_messages_filter_with_role(
        db, id=session_id, role=assistant_role_db_obj
    )

    raw_gpt_model_input = _get_gpt_input(
        role1_name=user_role_name,
        chat_messages1=[model.message for model in user_role_messages],
        role2_name=assistant_role_name,
        chat_messages2=[model.message for model in assistant_role_messages],
    )

    # 將資料輸入到 GPT model 並取得結果
    gpt_model_input = [jsonable_encoder(input) for input in raw_gpt_model_input]
    chat_result = get_chat_result(gpt_model_input)

    # 將 model 的結果儲存至資料庫
    _create_chat_message(
        db,
        chat_session_obj=session_db_obj,
        chat_role_obj=assistant_role_db_obj,
        message=chat_result,
    )

    response = ChatTextResponse(
        session_id=session_db_obj.id, question=data.message, answer=chat_result
    )

    return response
