from typing import Any, List

from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.crud.base import CRUDBase
from app.schemas import db_schemas
from app.models.chat import ChatMessage, ChatRole, ChatSession


class CRUDChatSession(CRUDBase[ChatSession, db_schemas.CreateChatSession]):
    """針對 chat_session table 的 CRUD 操作"""

    def create(self, db: Session, *, obj_in: db_schemas.CreateChatSession) -> ChatSession:
        return super().create(db, obj_in=obj_in)

    def get(self, db: Session, id: Any) -> ChatSession | None:
        return super().get(db, id)

    def get_chat_messages_filter_with_role(
        self, db: Session, *, id: Any, role: ChatRole
    ) -> List[ChatMessage]:
        """根據 `session_id` 和 `role_name` 取得符和的 messages

        像是取得 session_id = "xxxx", role_name = "user" 的所有 message 資料

        Args:
            db: ORM Session
            id: session_id
            role: `ChatRole` ORM model 實例

        Returns:
            回傳所有符合的 message 資料，會依照建立時間由舊到新排序
        """

        chat_session = self.get(db, id=id)

        chat_messages = (
            chat_session.chat_messages.filter(ChatMessage.role_id == role.id)
            .order_by(ChatMessage.create_at)
            .all()
        )

        return chat_messages


class CRUDChatRole(CRUDBase[ChatRole, db_schemas.CreateChatRole]):
    """針對 chat_role table 的 CRUD 操作"""

    def create(self, db: Session, *, obj_in: db_schemas.CreateChatRole) -> ChatRole:
        return super().create(db, obj_in=obj_in)

    def get(self, db: Session, id: Any) -> ChatRole | None:
        return super().get(db, id)

    def get_by_role_name(self, db: Session, name: str) -> ChatRole | None:
        return db.query(ChatRole).filter(ChatRole.role == name).first()


class CRUDChatMessage(CRUDBase[ChatMessage, db_schemas.CreateChatMessage]):
    """針對 chat_message table 的 CURD 操作"""

    def create(
        self,
        db: Session,
        *,
        chat_session_obj: ChatSession,
        chat_role_obj: ChatRole,
        obj_in: db_schemas.CreateChatMessage
    ) -> ChatMessage:
        """在 chat_message table 新增一筆資料

        Args:
            db: ORM Session
            chat_session_obj: 這個 message 資料對應的 `ChatSession` 實例（一對多關係）
            chat_role_obj: 這個 message 資料對應的 `ChatRole` 實例 （一對多關係）
            obj_in: `CreateChatMessage` schemas 實例

        Returns:
            回傳建立完成的 `ChatMessage` 實例
        """

        db_obj = ChatMessage(**jsonable_encoder(obj_in))

        chat_session_obj.chat_messages.append(db_obj)
        chat_role_obj.chat_messages.append(db_obj)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def get(self, db: Session, id: Any) -> ChatMessage | None:
        return super().get(db, id)


crud_chat_session = CRUDChatSession(ChatSession)
crud_chat_role = CRUDChatRole(ChatRole)
crud_chat_message = CRUDChatMessage(ChatMessage)
