'''
放跟 `embedding` 操作相關的 API
'''

from fastapi import APIRouter, UploadFile, HTTPException

embedding_router = APIRouter(
    prefix="/embedding", tags=["Embedding"], responses={404: {"description": "Not found."}}
)


@embedding_router.post("/file")
def upload_embedding_txt_file(file: UploadFile):
    """上傳 txt 檔案並進行 embedding"""

    if file.content_type != "text/plain":
        raise HTTPException(status_code=400, detail="File type must be txt.")

    raw_content = file.file.read()

    # 因為 read() 回傳的是 bytes 類型，所以要轉成 str
    # 最後將結尾的空白去除
    content = raw_content.decode("utf-8").rstrip()

    return {"message": "file upload success."}
