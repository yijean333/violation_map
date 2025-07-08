
# 違規偵測與地圖系統

這是一個結合 YOLO 模型與 Flask API 的違規偵測系統。當攝影機畫面中出現指定車種（如 oloo 或 bike），系統會自動上傳違規紀錄到伺服器，並可在地圖網頁中查詢最新違規資訊。

---

## 🧠 功能說明

- 使用 Ultralytics YOLO 模型進行影片偵測
- 將違規紀錄（時間、車種、攝影機名稱）自動以 JSON 格式送至後端 API
- Flask 提供 `/upload` 與 `/violations/<camera_name>` API 路由
- Leaflet 地圖網頁呈現攝影機位置與即時違規紀錄
- 適用於校園、自動化監控等場景

---

## 📁 專案結構

```

📦 violation\_map/
├── api.py              # Flask API 後端主程式
├── webhook\_json.py     # YOLO 偵測並上傳違規資料
├── map.html            # 地圖網頁（可用 Chrome 開啟）
├── violations.json     # 儲存違規資料（測試用）
├── requirements.txt    # Python 套件清單
├── .gitignore          # 忽略上傳的檔案或資料夾

````

---

## 🚀 安裝與執行方式

### 1. 安裝套件

```bash
pip install -r requirements.txt
````

### 2. 啟動 Flask API（後端）

```bash
python api.py
```

API 路徑範例如下：

* 上傳違規紀錄：`POST /upload`
* 查詢違規紀錄：`GET /violations/<camera_name>`

### 3. 執行 YOLO 偵測程式

```bash
python webhook_json.py
```

此程式會每 30 幀分析一次影像，若出現「oloo」或「bike」，會自動將資訊傳送到後端 API。

### 4. 開啟地圖網頁（map.html）

直接在瀏覽器中開啟 `map.html` 檔案，即可看到地圖與攝影機位置。

---

## 🌐 部署建議（Render）

若你部署 API 到 Render，請將 `webhook_json.py` 中的 API URL 改為你的 Render 網址，例如：

```python
API_UPLOAD_URL = "https://oloobijiang.onrender.com/upload"
```



## 📄 授權 License

本專案採用 MIT 授權，你可自由使用、修改與發佈。

