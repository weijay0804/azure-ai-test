'''
app 運行前的初始化檔
'''

from qdrant_client import QdrantClient, models

from app.config.settings import get_settings

settings = get_settings()


def init_qdrant():
    '''初始化 qdrant'''

    session = QdrantClient(settings.QDRANT_HOST)

    # 先檢查 collection 存不存在，如果不存在，就建立
    try:
        session.get_collection(settings.QDRANT_EMBEDDING_TEST_COLLECTION_NAME)

    except Exception:

        # 因為 openai embedding model 的維度是 1536 ，所以建立 size = 1536
        session.create_collection(
            settings.QDRANT_EMBEDDING_TEST_COLLECTION_NAME,
            vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
        )

    finally:
        session.close()


if __name__ == "__main__":
    init_qdrant()
