from pydantic import BaseModel
from typing import Generic, TypeVar, Type, Any, Optional

from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.config.database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType]):

    def __init__(self, model: Type[ModelType]):
        """

        Args:
            * `model`:  SQLAlchemy 的 model class
            * `schema`: Pydantic 的 model class
        """

        self.mode = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """取得一筆資料"""

        return db.get(self.mode, id)

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:

        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.mode(**obj_in_data)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj
