from typing import Any

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.schemas import db_schemas
from app.models.embedding import EmbeddingFileModel


class CRUDEmbeddingFile(CRUDBase[EmbeddingFileModel, db_schemas.CreateEmbeddingFile]):

    def create(self, db: Session, *, obj_in: db_schemas.CreateEmbeddingFile) -> EmbeddingFileModel:
        return super().create(db, obj_in=obj_in)

    def get(self, db: Session, id: Any) -> EmbeddingFileModel | None:
        return super().get(db, id)


crud_embedding_file = CRUDEmbeddingFile(EmbeddingFileModel)
