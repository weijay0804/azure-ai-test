'''
跟 Azure 連線、設定的操作（像是連線至 Azure OpenAI)
'''

import logging

from openai import AzureOpenAI
from azure.storage.blob import BlobServiceClient


def get_azure_openai_client(api_key: str, azure_endpoint: str, api_version: str) -> AzureOpenAI:

    client = AzureOpenAI(api_key=api_key, azure_endpoint=azure_endpoint, api_version=api_version)

    return client


def get_azure_blob_service_client(connect_str: str) -> BlobServiceClient:

    try:

        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    except Exception as e:
        logging.error(str(e))

        blob_service_client = None

    return blob_service_client
