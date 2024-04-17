'''
存放跟 embedding 操作相關的資料型態
'''

from pydantic import BaseModel


class EmbeddingObj(BaseModel):
    '''將 embedding 操作後得到的資料包裝成一個物件

    `id`: 物件唯一識別值，只是方便將資料加入至 `qdrant` (自動生成)
    `vector`: 經過 embedding 後得到的值
    `text`: 拿去 embedding 的文字
    '''

    id: str
    vector: list
    text: str
