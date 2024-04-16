'''
Embedding 操作相關的程式
'''

from app.config.settings import get_settings
from app.services.ai_model.init import get_azure_openai_client

settings = get_settings()


def get_embedding(text: str) -> list:

    client = get_azure_openai_client(
        api_key=settings.AZURE_OPENAI_EMBEDDING_API_KEY,
        azure_endpoint=settings.AZURE_OPENAI_EMBEDDING_ENDPOINT,
        api_version=settings.AZURE_OPENAI_EMBEDDING_API_VERSION,
    )

    response = client.embeddings.create(
        input=text, model=settings.AZURE_OPENAI_EMBEDDING_MODEL_NAME
    )

    return response.data[0].embedding
