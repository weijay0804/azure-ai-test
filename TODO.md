* 上傳 txt 檔案，並進行 embedding 功能
  1. 用戶使用 API 上傳 txt 檔案
  2. 後端程式通過 AI models 進行 embedding
  3. 將 embedding 的結果儲存至向量資料庫
  4. 將 txt 檔案上傳至 Azure Blob 中
  5. 將 txt 檔名和 Blob URL 儲存至資料庫
   
  >待辦事項
  * - [X] 建立 FastAPI Docker Compose
  * - [X] 使用 FastAPI 建立 EndPoint (`/embedding/file`) [POST]
  * - [X] 建立 Azure AI models
  * - [X] 將 txt 中的文字傳給 AI models 計算並回傳結果
  * - [X] 建立 Qdrant 的 Docker Compose
  * - [X] 將 AI models 回傳的結果儲存至 Qdrant
  * - [X] 將 txt 檔案上傳至 Azure Blob (這邊的檔名應該要用流水號)
  * - [X] 建立 MySQL 的 Docker Compose
  * - [X] 將 txt 檔名和 Azure Blob URL 儲存至資料庫
  * - [ ] 傳入 file_id 並取得對應的資料 API

* 用戶上傳一段問句，使用 GPT model 計算並取得問句的回答
  1. 用戶使用 API POST 一段問句
  2. 後端將問句上傳至 GPT model 並取得回答
  3. 將對話內容紀錄至資料庫

  > 代辦事項
  * - [X] 使用 FastAPI 建立 EndPoint (`/chat/text`) [POST]
  * - [X] 建立 Azure AI models
  * - [X] 要根據傳入的 session id 去資料庫取得歷史的對話紀錄，並將紀錄整理成可以上傳的格式
  * - [X] 將問句經由 model 計算並取得結果
  * - [X] 建例資料庫的資料表 (chat_role, chat_messages)
  * - [X] 將對話資料儲存到資料庫
  * - [ ] 傳入 sesion_id 並取得對話紀錄 API