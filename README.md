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

用瀏覽器開啟 [Api 說明文檔](http://20.92.160.233:8000/docs)

## Embedding

> 進行 embedding 操作

1. 先建立一個測試用的 txt 文檔

2. 先查看 Qdrant 資料庫內的資料
    
    使用瀏覽器開啟 [Qdrant dashboard](http://20.92.160.233:6333/dashboard#/collections/embedding_test)

    目前裡面是沒有資料的
    ![](/demo/images/qdrant1.png)

3. 調用 `/embedding/file` API

    在 `file` 欄位選擇你剛剛建立的文檔
    ![](/demo/images/embedding_file1.png)

    送出後會得到以下的回傳結果
    ![](/demo/images/embedding_file2.png)

    其中的 `file_id` 為這個檔案的唯一辨識符

    到此已經完成了 embedding 操作

4. 查看 Qdrant 資料庫資料

    一樣到先到 [Qdrant dashboard](http://20.92.160.233:6333/dashboard#/collections/embedding_test)

    此時可以看到多了一筆資料，然後其中的 id 值則是之前 API 回傳的 `file_id` 值
    ![](/demo/images/qdarnt2.png)

5. 查看 Azure Blob

    用瀏覽器開啟 [Azure Blob 控制面板](https://portal.azure.com/#view/Microsoft_Azure_Storage/ContainerMenuBlade/~/overview/storageAccountId/%2Fsubscriptions%2F8f2d86bc-5e16-472c-9819-b84b989bc28c%2FresourceGroups%2Finterviewee_min%2Fproviders%2FMicrosoft.Storage%2FstorageAccounts%2Finterviewdemo/path/embedding-container/etag/%220x8DC5EDF698C3989%22/defaultEncryptionScope/%24account-encryption-key/denyEncryptionScopeOverride~/false/defaultId//publicAccessVal/None)

    可以看到檔案文件已經成功上傳至 Blob 上，並且檔案名稱是 API 回傳的 `file_id` 值
    ![](/demo/images/azure_blob.png)

6. 查看 MySQL 中的資料

    在 API 說明文檔頁面中調用 `embedding/file/{file_id}` API

    *注意：其中的 `file_id` 要替換成你在使用時 API 回傳的值*

    ![](/demo/images/get_embedding_file_data1.png)

    送出後會得到以下的回傳值
    ![](/demo/images/get_embedding_file_data2.png)

    可以看到 API 回傳了資料在資料庫的內容，代表資料成功新增資料庫

## Chat

> 進行對話聊天操作

1. 調用 `/chat/messages` 建立一個對話

    *注意：第一次建立對話時不需要傳入 `session_id`*

    ![](/demo/images/chat1.png)

    送出後會得到以下的回傳值
    ![](/demo/images/chat2.png)

    其中的 `session_id` 為這個對話的 session 辨識符

2. 使用 `session_id` 繼續對話

    如果我們在調用 API 時傳入 `session_id` 的值，系統會找出歷史的聊天記錄，並繼續下去

    這裡我們將剛剛的 `session_id` 傳入，並繼續問問題
    ![](/demo/images/chat3.png)

    會得到以下回傳

    *注意：這個操作可能會需要一點時間*
    ![](/demo/images/chat4.png)

    我們在繼續問他問題，這次我們問一個缺乏上下文無法回答的問題
    ![](/demo/images/chat5.png)

    會得到以下回傳

    *注意：這個操作可能會需要一點時間*
    ![](/demo/images/chat6.png)

    可以看到他的回答依舊跟我們之前問的問題有關

3. 根據 `session_id` 取得歷史對話紀錄

    調用 `/chat/{session_id}/messages`

    *注意：其中的 `session_id` 要換成你實際在收到 API 回傳的值*
    ![](/demo/images/get_chat_messages1.png)

    會收到以下的回傳值
    ![](/demo/images/get_chat_messages2.png)