* 上傳 txt 檔案，並進行 embedding 功能
  1. 用戶使用 API 上傳 txt 檔案
  2. 後端程式通過 AI models 進行 embedding
  3. 將 embedding 的結果儲存至向量資料庫
  4. 將 txt 檔案上傳至 Azure Blob 中
  5. 將 txt 檔名和 Blob URL 儲存至資料庫
   
  >待辦事項
  * - [ ] 建立 FastAPI Docker Compose
  * - [ ] 使用 FastAPI 建立 EndPoint (`/embedding/file`) [POST]
  * - [ ] 建立 Azure AI models
  * - [ ] 將 txt 中的文字傳給 AI models 計算並回傳結果
  * - [ ] 建立 Qdrant 的 Docker Compose
  * - [ ] 將 AI models 回傳的結果儲存至 Qdrant
  * - [ ] 將 txt 檔案上傳至 Azure Blob (這邊的檔名應該要用流水號)
  * - [ ] 建立 MySQL 的 Docker Compose
  * - [ ] 將 txt 檔名和 Azure Blob URL 儲存至資料庫