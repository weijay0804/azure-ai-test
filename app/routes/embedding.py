'''
放跟 `embedding` 操作相關的 API
'''

from sqlalchemy.orm import Session
from qdrant_client import QdrantClient
from fastapi import APIRouter, UploadFile, HTTPException, Depends

from app.services import embedding
from app.config.database import get_qdrant_session, get_db_session

embedding_router = APIRouter(
    prefix="/embedding", tags=["Embedding"], responses={404: {"description": "Not found."}}
)


@embedding_router.post("/file")
def upload_embedding_txt_file(
    file: UploadFile,
    qsession: QdrantClient = Depends(get_qdrant_session),
    db_session: Session = Depends(get_db_session),
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

    return {"message": "file upload success.", "azure_url": db_obj.azure_blob_url, "id": db_obj.id}
