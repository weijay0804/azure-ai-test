'''
app 運行前的初始化檔
'''

from qdrant_client import QdrantClient, models

from app.config.settings import get_settings
from app.config.database import init_db_session
from app.crud.crud_chat import crud_chat_role
from app.schemas.db_schemas import CreateChatRole

settings = get_settings()


def init_qdrant():
    '''初始化 qdrant'''

    print("init Qdrant...")

    session = QdrantClient(settings.QDRANT_HOST)

    # 先檢查 collection 存不存在，如果不存在，就建立
    try:
        session.get_collection(settings.QDRANT_EMBEDDING_TEST_COLLECTION_NAME)

    except Exception:

        # 因為 openai embedding model 的維度是 1536 ，所以建立 size = 1536
        session.create_collection(
            settings.QDRANT_EMBEDDING_TEST_COLLECTION_NAME,
            vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
        )

    finally:
        session.close()

    print("Qdrant init successful.")


def init_chat_role_table():
    '''初始化 chat_role table 的資料

    先給 table 新增 `user` 和 `assistant`
    '''

    print("chat_role table init...")

    session_local = init_db_session()
    session = session_local()

    user_role = crud_chat_role.get_by_role_name(session, name="user")

    if user_role is None:

        crud_chat_role.create(session, obj_in=CreateChatRole(role="user"))

    assistant_role = crud_chat_role.get_by_role_name(session, name="assistant")

    if assistant_role is None:

        crud_chat_role.create(session, obj_in=CreateChatRole(role="assistant"))

    session.close()

    print("init successful.")


if __name__ == "__main__":
    init_qdrant()
    init_chat_role_table()
