'''
Embedding 操作相關的程式
'''

import uuid

from fastapi import UploadFile
from sqlalchemy.orm import Session
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct

from app.schemas import data_schemas
from app.schemas import db_schemas
from app.config.settings import get_settings
from app.models.embedding import EmbeddingFileModel
from app.crud.crud_embedding import embedding_file_crud
from app.config.azure_client import get_azure_openai_client, get_azure_blob_service_client


settings = get_settings()


def get_embedding(text: str) -> list:
    """將文字經由 OpenAI Embedding model 計算，並取得結果"""

    client = get_azure_openai_client(
        api_key=settings.AZURE_OPENAI_EMBEDDING_API_KEY,
        azure_endpoint=settings.AZURE_OPENAI_EMBEDDING_ENDPOINT,
        api_version=settings.AZURE_OPENAI_EMBEDDING_API_VERSION,
    )

    response = client.embeddings.create(
        input=text, model=settings.AZURE_OPENAI_EMBEDDING_MODEL_NAME
    )

    return response.data[0].embedding


def embedding(
    text: str, qsession: QdrantClient, file: UploadFile, db_session: Session
) -> EmbeddingFileModel:
    """進行 embedding 操作，並將結果儲存至 Qdrant"""

    uid = str(uuid.uuid4())

    embedding_response = get_embedding(text)

    embedding_obj = data_schemas.EmbeddingDataObj(id=uid, vector=embedding_response, text=text)

    # TODO 這邊的操作應該包成 func
    qsession.upsert(
        collection_name=settings.QDRANT_EMBEDDING_TEST_COLLECTION_NAME,
        points=[
            PointStruct(
                id=embedding_obj.id,
                vector=embedding_obj.vector,
                payload={"id": embedding_obj.id, "text": embedding_obj.text},
            )
        ],
    )

    # NOTE 這邊先寫死成 .txt，因為目前只支援 txt 類型
    url = upload_to_azure_blob(file, f"{uid}.txt")

    db_obj_in = db_schemas.CreateEmbeddingFile(
        id=uid, raw_filename=file.filename, azure_blob_url=url
    )

    db_obj = embedding_file_crud.create(db_session, obj_in=db_obj_in)

    return db_obj


# TODO 這個 func 應該移到別的地方
def upload_to_azure_blob(file: UploadFile, file_name: str):
    """上傳檔案至 Azure Blob"""

    blob_service_client = get_azure_blob_service_client(settings.AZURE_BLOB_SERVICE_CONNECT_STR)
    blob_client = blob_service_client.get_blob_client(
        container=settings.AZURE_BLOB_EMBEDDING_CONTAINER_NAME, blob=file_name
    )

    f = file.file.read()

    blob_client.upload_blob(f)

    return blob_client.url
