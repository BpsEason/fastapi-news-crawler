# FastAPI 新聞爬蟲 API — 非同步爬取 + 自動排程 + 視覺化分析

> **作品集級後端系統**：自動化爬取科技新聞 → PostgreSQL 儲存 → 安全 API 提供 → Streamlit 即時儀表板  
> 完整模組化設計，支援 Docker 部署、異步測試與 CI/CD。

---

## 專案動機與背景

本專案展示如何以 **FastAPI** 為核心，建構一個 **可生產、易擴充、具備完整生命週期** 的資料處理系統。

適用場景：
- 技術作品集展示
- 面試技術挑戰
- 教學範例專案
- 真實新聞資料 API 後端

---

## 技術棧總覽

| 功能 | 技術 | 說明 |
|------|------|------|
| **後端框架** | `FastAPI` | 非同步、高效能、自動產生 Swagger UI |
| **爬蟲** | `httpx` + `BeautifulSoup` | 非同步請求 + HTML 解析 |
| **資料庫** | `PostgreSQL` + `SQLModel` + `asyncpg` | ORM + 索引 + 去重機制 |
| **驗證** | `X-API-Key` Header | 集中式安全管理 |
| **排程** | `APScheduler` | 定時自動執行爬蟲 |
| **前端** | `Streamlit` | 互動式資料視覺化 |
| **部署** | `Docker Compose` | 一鍵啟動 FastAPI + DB |
| **測試** | `pytest-asyncio` | 完整異步流程測試 |
| **CI/CD** | `GitHub Actions` | 自動化測試與覆蓋率 |

---

## 專案結構

```
fastapi-news-crawler/
├── app/
│   ├── core/            ← 設定與安全 (config.py, security.py)
│   ├── database/        ← 模型與異步連線
│   ├── services/        ← 爬蟲與排程邏輯
│   ├── api/v1/endpoints/← API 路由
│   └── main.py          ← 應用啟動與生命週期
├── frontend/app.py      ← Streamlit 儀表板
├── tests/               ← 異步測試
├── docker-compose.yml   ← Docker 部署
├── .github/workflows/ci.yml ← CI/CD
├── .env.example         ← 環境變數範本
├── requirements.txt
└── README.md
```

---

## 快速啟動

### 1. 複製環境變數範本

```bash
cp .env.example .env
```

編輯 `.env`：
```env
DATABASE_URL=postgresql+asyncpg://user:password@db:5432/news_db
API_KEY_SECRET=your-super-secret-key-here
CRAWL_TARGET_URL=https://example.com/news
CRAWL_INTERVAL_HOURS=6
```

### 2. Docker 一鍵啟動

```bash
docker compose up --build -d
```

### 3. 啟動 Streamlit 前端

```bash
pip install streamlit pandas
streamlit run frontend/app.py
```

---

## 服務入口

| 服務 | 網址 | 備註 |
|------|------|------|
| **API 文件** | [http://localhost:8000/docs](http://localhost:8000/docs) | Swagger UI |
| **首頁** | [http://localhost:8000](http://localhost:8000) | 歡迎訊息 |
| **儀表板** | [http://localhost:8501](http://localhost:8501) | Streamlit 前端 |

---

## API 使用範例

所有請求 **必須包含 `X-API-Key` header**

### 手動觸發爬蟲

```bash
curl -X POST http://localhost:8000/crawl/now \
  -H "X-API-Key: your-super-secret-key-here"
```

### 取得文章（分頁）

```bash
curl "http://localhost:8000/api/v1/articles?offset=0&limit=10" \
  -H "X-API-Key: your-super-secret-key-here"
```

回應範例：
```json
[
  {
    "id": 1,
    "title": "非同步爬蟲優勢分析",
    "url": "https://example.com/post/1",
    "category": "Tech",
    "crawled_at": "2025-04-05T12:00:00Z"
  }
]
```

---

## Streamlit 前端功能

- 即時文章列表（標題、網址、時間）
- 類別分佈長條圖
- 總文章數與類別數統計
- 手動觸發爬蟲按鈕（需 API Key）
- 自動緩存與錯誤處理

> 建議截圖展示於 GitHub 首頁

---

## 測試與 CI/CD

### 本地測試

```bash
pytest tests/ --cov=app
```

涵蓋：
- API Key 驗證
- 爬蟲 → 儲存 → 讀取完整流程
- 資料結構正確性

### GitHub Actions

自動執行：
- Python 依賴安裝
- 使用 SQLite 模擬 PostgreSQL
- 執行所有測試
- 產生覆蓋率報告

---

## 延伸練習（作品集升級）

| 難度 | 功能 | 建議技術 |
|------|------|----------|
| 中 | 資料庫遷移 | `Alembic` |
| 中 | 動態網頁爬蟲 | `Playwright` |
| 高 | 分佈式排程 | `Celery + Redis` |
| 高 | 文字分析 | `spaCy` / `NLTK` |
| 高 | 進階驗證 | `OAuth2` / `JWT` |
| 高 | 快取與限流 | `Redis` + `slowapi` |

---

## 雲端部署建議

### Render（免費）

1. 推到 GitHub
2. 建立 Web Service
3. 設定環境變數
4. 自動部署

### Fly.io

```bash
fly launch
fly deploy
```

---

## 安全提示

- `.env` 已加入 `.gitignore`
- 建議生產環境使用 `bcrypt` 加密 API Key
- 資料庫密碼請定期輪替

---

## 授權

[MIT License](LICENSE)  
可自由使用、修改、商業應用，請保留原始作者資訊。

---
