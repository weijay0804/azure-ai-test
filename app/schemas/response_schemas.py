from typing import List
from pydantic import BaseModel
from datetime import datetime


class EmbeddingResultResponse(BaseModel):

    file_id: str
    azure_blob_url: str


class EmbeddingFileResponse(BaseModel):

    file_id: str
    raw_filename: str
    azure_blob_url: str
    create_at: datetime


class ChatTextResponse(BaseModel):

    session_id: str
    question: str
    answer: str


class ChatMessage(BaseModel):

    role: str
    message: str
    create_at: datetime


class ChatMessagesResponse(BaseModel):

    session_id: str
    messages: List[ChatMessage]
