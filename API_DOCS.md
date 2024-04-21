# API 說明文件

## Embedding

* [POST] `/embedding/file`

  > 上傳 `txt` 文字檔，並進行 embedding 處理，最後將資料儲存到資料庫。

  * Request schemas:

    * Header: 
      - `Content-Type: multipart/form-data`
    * Body: 
      - `txt file` *required*

  * Response schemas:

    * Status Code:
      - 200
      - 404
      - 422
    * Body:
      - `file_id` (str): 上傳的檔案唯辨識符，在 `Qdarnt` 和 `Azure blob` 也是使用這個辨識符。
      - `azure_blob_url` (str): 檔案在 Azure blob 的 url。

  * Example:

    ```
    Response:
        {
            "file_id" : "91294f28-ba05-4dc5-ae0e-28b3d0f56567",
            "azure_blob_url" : "https://....."
        }
    ```
    
* [GET] `/embedding/file/{file_id}`
  
  > 取得 `file_id` 的資料

  * Request schemas:

    * Parameters:

      - `file_id` (str) *required*: file 的唯一辨識符。

  * Response schemas:

    * Status Code:
      - 200
      - 404: 傳入的 `file_id` 不存在。
      - 422
    * Body:
      - `file_id` (str): 檔案的唯一辨識符。
      - `raw_filename` (str): 使用者上傳的檔案名稱。
      - `azure_blob_url` (str): 檔案在 Azure blob 的 url。
      - `create_at` (str): 資料建立時間。 (UTC0)

  * Example:
    ```
    Response:
        {
            "file_id" : "91294f28-ba05-4dc5-ae0e-28b3d0f56567",
            "raw_filename" : "test.txt",
            "azure_blob_url" : "https://....",
            "create_at" : "2024-04-21T09:45:03"
        }
    ```

## Chat

* [POST] `/chat/messages`

  > 接收輸入的文字並給 GTP model 運算，取得結果再儲存到資料庫。  
  *如果有傳入 `session_id` 就會把歷史的對話紀錄也傳送給 GPT model*

  * Request schemas:

    * Body:
      - `message` (str) *required*: 使用者的問題文字。
      - `session_id` (str): 對話的 session 唯一辨識符。 (如果有傳入的話，就會將歷史對話紀錄也傳入 GTP model，如果沒有傳入就會自動建立一個) 

  * Response schemas:

    * Status Code:
      - 200
      - 404: 傳入的 `session_id` 不存在。
      - 422
    * Body:
      - `session_id` (str): 對話的 session 唯一辨識符。
      - `question` (str): 傳入的問題文字。
      - `answer` (str): GPT model 回傳的答案文字

  * Example:

    ```
    Request:
        {
            "message" : "你好",
            "session_id" : "f9b2e23e-2b8d-40d8-aa07-f5f4789b531a"
        }

    Response:
        {
            "session_id" : "f9b2e23e-2b8d-40d8-aa07-f5f4789b531a",
            "question" : "你好",
            "answer" : "你好，有什么可以帮助您的吗?"
        }
    ```
    
* [GET] `/chat/{session_id}/messages`
  
  > 取得 `session_id` 的歷史對話資料

  * Request schemas:

    * Parameters:

      - `session_id` (str) *required*: 對話 session 的唯一辨識符。

  * Response schemas:

    * Status Code:
      - 200
      - 404: `session_id` 不存在。
      - 422
    * Body:
      - `session_id` (str): 對話 session 的唯一辨識符。
      - `messages` (list): 對話紀錄物件的列表。
      - 對話紀錄物件：
        - `role` (str): 對話角色名稱。
        - `message` (str): 對話訊息文字。
        - `create_at` (str): 對話資料建立時間 (UTC0)


  * Example:
    ```
    Response:
        {
            "session_id" : "f9b2e23e-2b8d-40d8-aa07-f5f4789b531a",
            "messages" : [
                {
                    "role" : "user",
                    "message" : "你好",
                    "create_at" : "2024-04-21T10:48:44"
                },
                {
                    "role" : "assistant",
                    "message" : "你好，有什么可以帮助您的吗?",
                    "create_at" : "2024-04-21T10:48:46"
                }
            ]
        }
    ```