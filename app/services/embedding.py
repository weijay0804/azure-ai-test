'''
Embedding 操作相關的程式
'''

import uuid
import logging

from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from qdrant_client import QdrantClient

from app.schemas import db_schemas
from app.schemas import data_schemas
from app.common.qdrant import upsert_data
from app.config.settings import get_settings
from app.models.embedding import EmbeddingFileModel
from app.crud.crud_embedding import embedding_file_crud
from app.common.azure import get_embedding_result, upload_to_azure_blob


settings = get_settings()


def embedding(
    text: str, qsession: QdrantClient, file: UploadFile, db_session: Session
) -> EmbeddingFileModel:
    """進行 embedding 操作，並將結果儲存至 Qdrant"""

    uid = str(uuid.uuid4())

    embedding_response = get_embedding_result(text)

    embedding_obj = data_schemas.EmbeddingDataObj(id=uid, vector=embedding_response, text=text)

    qdrant_upsert_response = upsert_data(qsession, embedding_obj)

    if qdrant_upsert_response.status != "completed":
        logging.exception(f"Qdrant upsert data fail. status: {qdrant_upsert_response.status}")

        raise HTTPException(status_code=500, detail="Qdrant upsert data fail.")

    # NOTE 這邊先寫死成 .txt，因為目前只支援 txt 類型
    url = upload_to_azure_blob(file, f"{uid}.txt")

    db_obj_in = db_schemas.CreateEmbeddingFile(
        id=uid, raw_filename=file.filename, azure_blob_url=url
    )

    db_obj = embedding_file_crud.create(db_session, obj_in=db_obj_in)

    return db_obj
