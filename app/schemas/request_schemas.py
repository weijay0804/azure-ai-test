from pydantic import BaseModel
from typing import Optional


class ChatTextRequest(BaseModel):

    session_id: Optional[str] = None
    message: str
