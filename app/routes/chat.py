from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.services import chat
from app.common.deps import get_db_session
from app.schemas import request_schemas, response_schemas


chat_router = APIRouter(
    prefix="/chat", tags=["Chat"], responses={404: {"description": "Not found."}}
)


@chat_router.post("/text", response_model=response_schemas.ChatTextResponse)
def get_chat(data: request_schemas.ChatTextRequest, db: Session = Depends(get_db_session)):

    response = chat.chat(data=data, db=db)

    return response
