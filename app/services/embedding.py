'''
Embedding 操作相關的程式
'''

import uuid

from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct

from app.config.settings import get_settings
from app.config.azure_client import get_azure_openai_client
from app.schemas.embedding import EmbeddingObj

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


def embedding(text: str, qsession: QdrantClient):
    """進行 embedding 操作，並將結果儲存至 Qdrant"""

    embedding_response = get_embedding(text)

    embedding_obj = EmbeddingObj(id=str(uuid.uuid4()), vector=embedding_response, text=text)

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
