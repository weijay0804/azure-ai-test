# AI 實戰專案

> 使用 FastAPI 建立 API 來處理 Embedding、Chat 的相關操作。

## Embedding
    功能說明：
    1. 用戶藉由 API 上傳想要 Embedding 的 txt 檔案。
    2. 後端程式將 txt 檔案內容傳入至 Embedding model 計算並取得結果。
    3. 後端程式將 Embedding 結果儲存至向量資料庫 (Qdrant)。
    4. 後端程式將 txt 檔案上傳至 Azure Blob。
    5. 後端程式將 txt 檔案名稱儲存至資料庫。

## Chat
    功能說明：
    1. 用戶可用藉由 API 傳送一段問句。
    2. 後端程式將問句傳入 Chat model 取得結果。
    3. 後端程式將對話紀錄儲存至資料庫。

# Useage

> 確認服務運行狀態

1. 先確認 docker-compose 服務是否有正常啟動
   ```bash
   $ docker-compose ls -a
   ```

   如果沒有，就進入專案目錄
   ```bash
   $ cd /home/interviewee/azure-ai-test
   ```

   啟動 docker-compose
   ```
   $ docker-compose up
   ```

2. 使用 curl 測試 fastapi 服務
   ```bash
   $ curl -X 'GET' 'http://127.0.0.1:8000/'
   ```

   如果收到這個回傳值表示服務正常
   ```json
    {
        "message" : "test"
    }
    ```

## Embedding

> 進行 embedding 操作

1. 先建立一個 txt 檔案用來測試，或是可以用已經建立好的檔案

2. 先查看 Qdrant 的資料
    ```bash
    $ curl -X 'GET' 'http://127.0.0.1:6333/collections/embedding_test' 
    ```

    查看回傳值中的 `points_count` ，代表目前資料庫中的資料數量

4. 使用 curl 呼叫 embedding api
   ```bash
   $ curl -X 'POST' \
    'http://127.0.0.1:8000/embedding/file' \
    -H 'Content-Type: multipart/form-data' \
    -F 'file=@/home/interviewee/test.txt;type=text/plain'
   ```

   如果收到以下回傳值表示成功
   ```json
   {
    "file_id":"1e29ac52-5431-4c97-9510-a2b5e36513d8","azure_blob_url":"https://...."
    }
   ```

5. 查看資料是否新增至 Qdrant
    ```bash
    $ curl -X 'GET' 'http://127.0.0.1:6333/collections/embedding_test' 
    ```

    查看回傳值中的 `points_count` ，應該會是之前的數量 +1，代表資料成功新增至資料庫中

6. 使用 `file_id` 查看 MySQL 中的資料
   
    使用第 4 步驟中回傳值的 `file_id`

    *注意：要把其中的 `file_id` 值替換掉*

    ```bash
    $ curl -X 'GET' 'http://127.0.0.1:8000/embedding/file/1e29ac52-5431-4c97-9510-a2b5e36513d8' # 要替換成正確的 file_id
    ```

    然後得到 file 在資料庫中的資訊
    ```json
    {
        "file_id": "1e29ac52-5431-4c97-9510-a2b5e36513d8",
        "raw_filename": "test.txt",
        "azure_blob_url": "https:....",
        "create_at": "2024-04-21T12:59:07"
    }
    ```

## Chat

> 進行對話聊天操作

1. 新增一個 message

    ```bash
    $ curl -X 'POST' \
    'http://127.0.0.1:8000/chat/messages' \
    -H 'Content-Type: application/json' \
    -d '{"message" : "你好"}'
    ```

    會得到以下回傳值
    ```json
    {
        "session_id" : "8dca73df-4db3-4aa7-aa56-4880cd2b73af",
        "question" : "你好",
        "answer" : "你好，有什么可以帮助你的吗？"
    }
    ```

2. 在對話 session 中繼續對話

    如果在呼叫 API 時帶入上一步取得的 `session_id`，程式會根據之前的對話紀錄繼續接下去

    例如：

    * 先再繼續一段對話

        *注意：這邊的 `session_id` 要替換掉*

        *注意：這個操作可能會需要一點時間，所以如果 console 卡住是正常的*

        ```bash
        $ curl -X 'POST' \
        'http://127.0.0.1:8000/chat/messages' \
        -H 'Content-Type: application/json' \
        -d '{"session_id" : "8dca73df-4db3-4aa7-aa56-4880cd2b73af", "message" : "什麼是 python"}'
        ```

        會得到類似以下的回傳
        ```json
        {
            "session_id":"8dca73df-4db3-4aa7-aa56-4880cd2b73af","question":"什麼是 python",
            "answer":"Python 是一种高级的编程语言，具有清晰、直观的结构。它的特点是易读性强，语法清晰，..."
        }
        ```
    
    * 然後繼續詢問

        ```bash
        curl -X 'POST' \
        'http://127.0.0.1:8000/chat/messages' \
        -H 'Content-Type: application/json' \
        -d '{"session_id" : "8dca73df-4db3-4aa7-aa56-4880cd2b73af", "message" : "他能幹嘛？"}'
        ```

        會得到類似以下的回傳
        ```json
        {
            "session_id":"8dca73df-4db3-4aa7-aa56-4880cd2b73af","question":"他能幹嘛？",
            "answer":"Python 的应用范围非常广泛，以下是一些主要的应用领域：..."
        }
        ```

3. 使用 `session_id` 取得對話紀錄

    *注意： 這邊的 `session_id` 要替換掉*

    ```bash
    $ curl -X 'GET' 'http://127.0.0.1:8000/chat/8dca73df-4db3-4aa7-aa56-4880cd2b73af/messages'
    ```

    然後會得到類似以下的回傳
    ```json
    {
        "session_id":"8dca73df-4db3-4aa7-aa56-4880cd2b73af",
        "messages":[
            {
                "role":"user",
                "message":"你好",
                "create_at":"2024-04-21T13:18:16"
            },
            {
                "role":"assistant",
                "message":"你好！有什么可以帮助你的吗？",
                "create_at":"2024-04-21T13:18:18"
            },
            {
                "role":"user",
                "message":"什麼是 python",
                "create_at":"2024-04-21T13:23:09"
            },
        ]
    }
    ```