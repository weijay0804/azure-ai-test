from pydantic import BaseModel


class CreateEmbeddingFile(BaseModel):
    id: str
    raw_filename: str
    azure_blob_url: str
