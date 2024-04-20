from pydantic import BaseModel


class CreateEmbeddingFile(BaseModel):
    id: str
    raw_filename: str
    azure_blob_url: str


class CreateChatSession(BaseModel):
    """要建立 chat_session table 資料的 schema"""

    id: str


class CreateChatRole(BaseModel):
    """要建立 chat_role table 資料的 schema"""

    role: str


class CreateChatMessage(BaseModel):
    """要建立 chat_message table 資料的 schema"""

    message: str
