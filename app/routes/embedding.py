'''
放跟 `embedding` 操作相關的 API
'''

import uuid

from fastapi import APIRouter, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session
from qdrant_client import QdrantClient

from app.services import embedding
from app.models.embedding import EmbeddingFile
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

    uid = str(uuid.uuid4())

    # 進行 embedding 操作
    embedding.embedding(text=content, qsession=qsession, id=uid)

    # 上傳至 Azure Blob
    url = embedding.upload_to_azure_blob(file, f"{uid}.txt")

    # TODO 這邊要重構一下，不要把操作資料庫的動作寫在 router
    embedding_file_obj = EmbeddingFile(id=uid, raw_filename=file.filename, azure_blob_url=url)

    db_session.add(embedding_file_obj)
    db_session.commit()

    return {"message": "file upload success.", "azure_url": url, "id": uid}
