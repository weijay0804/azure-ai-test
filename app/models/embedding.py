from datetime import datetime

from sqlalchemy import Column, String, Text, func, DateTime

from app.config.database import Base


class EmbeddingFile(Base):
    '''存放使用者上傳的 txt 檔案相關資訊'''

    __tablename__ = "embedding_file"

    id = Column(String(36), primary_key=True)
    raw_filename = Column(String(20), nullable=False)
    azure_blob_url = Column(Text, nullable=False)
    update_at = Column(DateTime, nullable=True, default=None, onupdate=datetime.now())
    create_at = Column(DateTime, nullable=False, server_default=func.now())
