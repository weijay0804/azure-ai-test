'''
存放依賴項目 (像是 get_db_session 等)
'''

from typing import Generator

from qdrant_client import QdrantClient

from app.config.settings import get_settings
from app.config.database import init_db_session

settings = get_settings()


def get_db_session() -> Generator:

    session_local = init_db_session()
    session = session_local()

    try:
        yield session

    finally:
        session.close()


def get_qsession() -> Generator:

    session = QdrantClient(settings.QDRANT_HOST)

    try:
        yield session

    finally:
        session.close()
