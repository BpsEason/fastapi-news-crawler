# FastAPI 新聞爬蟲 API — 非同步爬取 + 自動排程 + 視覺化分析

> **現代化作品集範例：** 自動爬取科技新聞 → 儲存至 PostgreSQL → 提供帶有 API Key 驗證的 API → Streamlit 顯示趨勢。

| 元素 | 技術棧 | 描述 |
| :--- | :--- | :--- |
| **後端框架** | `FastAPI` | 高效能非同步 API 服務。 |
| **爬蟲** | `httpx` + `BeautifulSoup` | 非同步 HTTP 請求，增強效率。 |
| **資料庫** | `PostgreSQL` + `SQLModel` | 穩定可靠的關聯式資料庫，使用異步連線 (AsyncPG)。 |
| **排程** | `APScheduler` | 定時自動執行爬蟲任務。 |
| **驗證** | `API Key Header` | 所有 API 端點皆受保護。 |
| **部署** | `Docker Compose` | 一鍵啟動 Web 服務與 PostgreSQL 資料庫。 |
| **前端** | `Streamlit` | 輕量級儀表板，即時展示數據。 |
| **CI/CD** | `GitHub Actions` | 自動化測試流程。 |

## 專案架構 (模組化設計)

```
fastapi-news-crawler/
├── app/
│   ├── core/            ← 設定與安全 (config.py, security.py)
│   ├── database/        ← 資料庫模型與連線 (models.py, __init__.py)
│   ├── services/        ← 核心業務邏輯 (crawler.py, scheduler.py)
│   ├── api/v1/          ← API 路由 (news.py)
│   └── main.py          ← 應用程式啟動點
├── frontend/app.py      ← Streamlit 儀表板
├── tests/               ← pytest 異步測試
├── docker-compose.yml   ← Docker 部署配置
├── .github/workflows/ci.yml ← GitHub Actions
└── README.md
```

## 安裝與啟動 (Docker Compose 推薦)

此專案設計用於 Docker 環境，以提供 PostgreSQL 數據庫服務。

### 1. 本地啟動 (Docker 推薦)

確保您已安裝 Docker 和 Docker Compose。

```bash
# 1. 執行此腳本 (setup_portfolio.sh) 以生成所有檔案

# 2. 使用 Docker Compose 一鍵啟動服務與資料庫
# 首次啟動可能需要幾分鐘來下載 PostgreSQL 映像和安裝依賴
docker compose up --build -d
```

### 2. 存取服務

服務啟動後：

- **FastAPI API 文件 (Swagger UI):** `http://localhost:8000/docs`
- **Streamlit 儀表板:** `http://localhost:8501` (需要額外啟動，見下一步驟)

### 3. 啟動 Streamlit 前端 (選用)

在專案根目錄下，虛擬環境已啟動：

```bash
# 安裝 streamlit (若 requirements.txt 中未包含)
pip install streamlit pandas

# 運行前端儀表板 (Streamlit 預設運行在 8501 Port)
streamlit run frontend/app.py
```

## API 驗證與測試

- **預設 API Key:** `your-api-key-secret-placeholder`
- **手動觸發爬蟲 (需 Key):** `POST http://localhost:8000/crawl/now`
- **查詢數據 (需 Key):** `GET http://localhost:8000/api/v1/articles`

### 執行單元測試

使用 `pytest-asyncio` 測試異步邏輯和 API 驗證：

```bash
pytest tests/
```

## 延伸練習題 (作品集升級點)

1.  **Alembic Migration:** 導入 Alembic 進行資料庫 Schema 版本控制。
2.  **真實爬蟲:** 將 `app/services/crawler.py` 替換為使用 Playwright 抓取真實 JS 渲染網站。
3.  **異步排程:** 調整 `app/services/scheduler.py` 以使用 Celery 處理更複雜、分佈式的排程任務。
4.  **數據清洗:** 在爬蟲服務中加入 NLTK 或 spaCy 進行關鍵字提取和情緒分析。
