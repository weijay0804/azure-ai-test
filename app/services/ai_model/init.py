'''
處理進行 AI 處理時需要遇到的共同操作（像是連線至 Azure OpenAI)
'''

from openai import AzureOpenAI


def get_azure_openai_client(api_key: str, azure_endpoint: str, api_version: str) -> AzureOpenAI:

    client = AzureOpenAI(api_key=api_key, azure_endpoint=azure_endpoint, api_version=api_version)

    return client
