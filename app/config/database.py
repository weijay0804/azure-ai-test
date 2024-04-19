'''
放跟 DB 設定、連線有關的程式
'''

from sqlalchemy import create_engine
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
