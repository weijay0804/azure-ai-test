'''
API 主入口
'''

from fastapi import FastAPI

from app.config.settings import get_settings


def create_app():
    settings = get_settings()
    app = FastAPI(title=settings.APP_NAME)

    return app


app = create_app()


@app.get("/")
def root():
    return {"message": "test"}
