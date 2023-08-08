# 應用Open AI API 的PDF翻譯工具
## 使用GPT3.5 turbo 進行翻譯
### 本專案需要預先下載下列套件

- python-dotenv
- PyPDF2
- nltk
- requests

## 請依照下列步驟進行設定

### Step 1:
請到 [Open AI API-Keys](https://platform.openai.com/account/api-keys) 取得 **API金鑰**

### Step 1.1:
如果尚未設定信用卡,須先到GPT網站自行設定。
(路徑於 ORGANIZATION > Billing > Payment methods)
### Step 2:
將要翻譯的 **檔案(pdf)** 放到 **SourceFile** 資料夾底下

### Step 3:
到 **.env** 檔案中設定下列資料
```text
OPENAI_API_KEY=API_KEY  OPEN_AI_API金鑰
FILE_NAME=file.pdf      PDF檔案名稱
PDF_START_PAGE=0        開始讀取頁數(預設為0)
PDF_END_PAGE=0          結束讀取頁面(預設為0,表檔案最後一頁,不包含該頁)
```
### Step 4:
執行 **main.py** 檔案開始翻譯

### Step 5:
翻譯結束後到 **result** 資料夾取得翻譯好的文件(.txt)

---
#### 其他
1. 在logger資料夾內可以查看每次送出的API回傳資料
2. 於檔案尾部可以查看本次翻譯所使用的Token數量及估價