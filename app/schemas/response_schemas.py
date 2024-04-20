from pydantic import BaseModel


class ChatTextResponse(BaseModel):

    session_id: str
    question: str
    answer: str
