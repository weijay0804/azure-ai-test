'''
放跟 `embedding` 操作相關的 API
'''

from sqlalchemy.orm import Session
from qdrant_client import QdrantClient
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, UploadFile, HTTPException, Depends

from app.common import deps
from app.services import embedding
from app.schemas import response_schemas


embedding_router = APIRouter(
    prefix="/embedding", tags=["Embedding"], responses={404: {"description": "Not found."}}
)


@embedding_router.post("/file", response_model=response_schemas.EmbeddingResultResponse)
def upload_embedding_txt_file(
    file: UploadFile,
    qsession: QdrantClient = Depends(deps.get_qsession),
    db_session: Session = Depends(deps.get_db_session),
):
    """上傳 txt 檔案並進行 embedding"""

    if file.content_type != "text/plain":
        raise HTTPException(status_code=400, detail="File type must be txt.")

    raw_content = file.file.read()

    # 因為 read() 回傳的是 bytes 類型，所以要轉成 str
    # 最後將結尾的空白去除
    content = raw_content.decode("utf-8").rstrip()

    # 進行 embedding 操作
    db_obj = embedding.embedding(text=content, qsession=qsession, file=file, db_session=db_session)

    return response_schemas.EmbeddingResultResponse(file_id=db_obj.id, **jsonable_encoder(db_obj))


@embedding_router.get("/file/{file_id}", response_model=response_schemas.EmbeddingFileResponse)
def get_file_data(file_id: str, db_sesion: Session = Depends(deps.get_db_session)):

    db_obj = embedding.get_embedding_file_data(file_id, db_sesion)

    return response_schemas.EmbeddingFileResponse(file_id=db_obj.id, **jsonable_encoder(db_obj))
