'''
存放跟 AZURE 服務操作相關的程式 (像是使用 OpenAI Embedding Model等)
'''

from typing import List

from fastapi import UploadFile

from app.config.settings import get_settings
from app.config.azure_client import get_azure_openai_client, get_azure_blob_service_client

settings = get_settings()


def get_chat_result(messages: List[dict]) -> str:
    """取得經由 gpt model 計算後的對話結果

    Args:
        messages: 歷史對話紀錄
        ```
        [
            {"role" : "user", "content" : "q1"},
            ...
        ]
        ```

    Returns:
        對話結果
    """

    client = get_azure_openai_client(
        api_key=settings.AZURE_OPENAI_EMBEDDING_API_KEY,
        azure_endpoint=settings.AZURE_OPENAI_EMBEDDING_ENDPOINT,
        api_version=settings.AZURE_OPENAI_EMBEDDING_API_VERSION,
    )

    response = client.chat.completions.create(
        model="interviewee-gtp-4-model", max_tokens=50, messages=messages
    )

    return response.choices[0].message.content


def get_embedding_result(text: str) -> List[float]:
    """將文字經由 OpenAI Embedding model 計算，並取得結果

    Args:
        text: 要進行 embedding 的文字

    Returns:
        計算後的向量 (1536 維)
    """

    client = get_azure_openai_client(
        api_key=settings.AZURE_OPENAI_EMBEDDING_API_KEY,
        azure_endpoint=settings.AZURE_OPENAI_EMBEDDING_ENDPOINT,
        api_version=settings.AZURE_OPENAI_EMBEDDING_API_VERSION,
    )

    response = client.embeddings.create(
        input=text, model=settings.AZURE_OPENAI_EMBEDDING_MODEL_NAME
    )

    return response.data[0].embedding


def upload_to_azure_blob(file: UploadFile, file_name: str) -> str:
    """將檔案上傳至 Azure blob 中

    Args:
        file: 要上傳的檔案
        file_name: 顯示在 blob 上的檔案名稱

    Returns:
        檔案在 blob 的 url
    """

    blob_service_client = get_azure_blob_service_client(settings.AZURE_BLOB_SERVICE_CONNECT_STR)
    blob_client = blob_service_client.get_blob_client(
        container=settings.AZURE_BLOB_EMBEDDING_CONTAINER_NAME, blob=file_name
    )

    f = file.file.read()

    blob_client.upload_blob(f)

    return blob_client.url
