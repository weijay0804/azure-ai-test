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


@lru_cache
def get_settings() -> Settings:
    return Settings()
