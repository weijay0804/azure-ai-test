'''
API 設定檔
'''

import os
from pathlib import Path
from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# 設定環境變數檔案路徑
# 並讀取環境變數
env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    """APP 設定檔"""

    APP_NAME: str = os.environ.get("APP_NAME", "FastAPI")

    # Azure OpenAI config
    AZURE_OPENAI_EMBEDDING_API_KEY: str = os.environ.get("AZURE_OPENAI_EMBEDDING_API_KEY")
    AZURE_OPENAI_EMBEDDING_ENDPOINT: str = os.environ.get("AZURE_OPENAI_EMBEDDING_ENDPOINT")
    AZURE_OPENAI_EMBEDDING_API_VERSION: str = os.environ.get(
        "AZURE_OPENAI_EMBEDDING_API_VERSION", "2023-07-01-preview"
    )
    AZURE_OPENAI_EMBEDDING_MODEL_NAME: str = os.environ.get("AZURE_OPENAI_EMBEDDING_MODEL_NAME")

    # Azure Blob config
    AZURE_BLOB_SERVICE_CONNECT_STR: str = os.environ.get("AZURE_BLOB_SERVICE_CONNECT_STR")
    AZURE_BLOB_EMBEDDING_CONTAINER_NAME: str = os.environ.get("AZURE_BLOB_EMBEDDING_CONTAINER_NAME")

    # Qdrant config
    QDRANT_HOST: str = os.environ.get("QDRANT_HOST")
    QDRANT_EMBEDDING_TEST_COLLECTION_NAME: str = os.environ.get(
        "QDRANT_EMBEDDING_TEST_COLLECTION_NAME", "embedding_test"
    )

    # MySQL config
    MYSQL_HOST: str = os.environ.get("MYSQL_HOST", "localhost")
    MYSQL_USER: str = os.environ.get("MYSQL_USER", "root")
    MYSQL_PASS: str = os.environ.get("MYSQL_PASSWORD", "secret")
    MYSQL_PORT: int = int(os.environ.get("MYSQL_PORT", 3306))
    MYSQL_DB: str = os.environ.get("MYSQL_DB", "ai_interview")
    DATABASE_URI: str = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASS}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
