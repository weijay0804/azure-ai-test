'''
存放跟 Qdrant 操作相關的程式（像是新增向量資料至資料庫、查詢等）
'''

from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, UpdateResult

from app.schemas import data_schemas
from app.config.settings import get_settings

settings = get_settings()


def upsert_data(qsession: QdrantClient, data: data_schemas.EmbeddingDataObj) -> UpdateResult:
    """將資料新增至向量資料庫

    Args:
        qsession: Qdrant session
        data: 要插入的資料物件
    """

    r = qsession.upsert(
        collection_name=settings.QDRANT_EMBEDDING_TEST_COLLECTION_NAME,
        points=[
            PointStruct(
                id=data.id,
                vector=data.vector,
                payload={"id": data.id, "text": data.text},
            )
        ],
    )

    return r
