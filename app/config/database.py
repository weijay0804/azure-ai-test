'''
放跟 DB 設定、連線有關的程式
'''

from typing import Generator

from qdrant_client import QdrantClient, models

from app.config.settings import get_settings

settings = get_settings()


# Qdrant 設定
def init_qdrant(qsession: QdrantClient):

    # 先檢查 collection 存不存在，如果不存在，就建立
    try:
        qsession.get_collection(settings.QDRANT_EMBEDDING_TEST_COLLECTION_NAME)

    except Exception:

        # 因為 openai embedding model 的維度是 1536 ，所以建立 size = 1536
        qsession.create_collection(
            settings.QDRANT_EMBEDDING_TEST_COLLECTION_NAME,
            vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
        )


def get_qdrant_session() -> Generator:

    session = QdrantClient("http://host.docker.internal:6333")

    try:
        init_qdrant(session)
        yield session

    finally:
        session.close()
