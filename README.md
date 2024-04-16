# AI 實戰專案

> 使用 FastAPI 建立 API 來處理 Embedding、Chat 的相關操作。

## Embedding
    功能說明：
    1. 用戶藉由 API 上傳想要 Embedding 的 txt 檔案。
    2. 後端程式將 txt 檔案內容傳入至 Embedding model 計算並取得結果。
    3. 後端程式將 Embedding 結果儲存至向量資料庫。
    4. 後端程式將 txt 檔案上傳至 Azure Blob。
    5. 後端程式將 txt 檔案名稱儲存至資料庫。

## Chat
    功能說明：
    1. 用戶可用藉由 API 傳送一段問句。
    2. 後端程式將問句傳入 Chat model 取得結果。
    3. 後端程式將對話紀錄儲存至資料庫。