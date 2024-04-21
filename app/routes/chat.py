from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.services import chat
from app.common.deps import get_db_session
from app.schemas import request_schemas, response_schemas


chat_router = APIRouter(
    prefix="/chat", tags=["Chat"], responses={404: {"description": "Not found."}}
)


@chat_router.post("/messages", response_model=response_schemas.ChatTextResponse)
def get_chat(data: request_schemas.ChatTextRequest, db: Session = Depends(get_db_session)):

    response = chat.chat(data=data, db=db)

    return response


@chat_router.get("/{session_id}/messages")
def get_chat_messages(session_id: str, db: Session = Depends(get_db_session)):

    messages = chat.get_chat_messages(db, session_id)

    chat_message_list = []

    # 整理成方便查看的格式
    for message in messages:
        tmp = response_schemas.ChatMessage(
            role=message.chat_role.role, message=message.message, create_at=message.create_at
        )

        chat_message_list.append(tmp)

    response = response_schemas.ChatMessagesResponse(
        session_id=session_id, messages=chat_message_list
    )

    return response
