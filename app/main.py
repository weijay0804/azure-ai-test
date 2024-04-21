'''
API 主入口
'''

from fastapi import FastAPI

from app.routes import embedding, chat
from app.config.settings import get_settings


def create_app():
    settings = get_settings()
    app = FastAPI(title=settings.APP_NAME)

    # 註冊路由
    app.include_router(embedding.embedding_router)
    app.include_router(chat.chat_router)

    return app


app = create_app()


@app.get("/")
def root():
    return {"message": "test"}
