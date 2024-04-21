from typing import List
from pydantic import BaseModel
from datetime import datetime


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
