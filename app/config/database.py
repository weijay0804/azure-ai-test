'''
放跟 DB 設定、連線有關的程式
'''

from typing import Generator

from sqlalchemy import create_engine
from qdrant_client import QdrantClient, models
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config.settings import get_settings

settings = get_settings()

Base = declarative_base()


# MySQL 設定
def init_db_session():

    engine = create_engine(
        settings.DATABASE_URI, pool_pre_ping=True, pool_recycle=3600, pool_size=20, max_overflow=0
    )

    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

    return SessionLocal


def get_db_session() -> Generator:

    session_local = init_db_session()
    session = session_local()

    try:
        yield session

    finally:
        session.close()


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

    session = QdrantClient(settings.QDRANT_HOST)

    try:
        init_qdrant(session)
        yield session

    finally:
        session.close()
