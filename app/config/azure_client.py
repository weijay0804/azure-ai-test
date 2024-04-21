'''
跟 Azure 連線、設定的操作（像是連線至 Azure OpenAI)
'''

import logging

from openai import AzureOpenAI
from azure.storage.blob import BlobServiceClient

from app.config.settings import get_settings

settings = get_settings()


def get_azure_openai_client() -> AzureOpenAI:

    client = AzureOpenAI(
        api_key=settings.AZURE_OPENAI_API_KEY,
        azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
        api_version=settings.AZURE_OPENAI_API_VERSION,
    )

    return client


def get_azure_blob_service_client(connect_str: str) -> BlobServiceClient:

    try:

        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    except Exception as e:
        logging.error(str(e))

        blob_service_client = None

    return blob_service_client
