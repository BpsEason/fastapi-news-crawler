from fastapi import FastAPI, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings
from app.database import init_db, get_db_session
from app.services.crawler import fetch_news_titles, save_articles
from app.services.scheduler import start_scheduler, shutdown_scheduler
from app.api.v1.endpoints import news
from app.core.security import get_api_key

# 創建 FastAPI 實例
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="作品集級別：非同步爬蟲、PostgreSQL、排程、API Key 驗證",
    version="1.0.0"
)

# 啟動時執行：初始化資料庫與啟動排程
@app.on_event("startup")
async def startup_event():
    # 確保資料庫已連線並有資料表 (請在 Docker Compose 啟動後執行)
    # await init_db() # 實際運行時，建議在 Docker Compose 或啟動腳本中執行 migration/init_db
    
    # 啟動排程器，自動執行爬蟲
    start_scheduler()
    print("FastAPI 應用程式啟動。排程器已啟動。")

# 關閉時執行：關閉排程
@app.on_event("shutdown")
def shutdown_event():
    shutdown_scheduler()

# 包含 API 路由 (前綴 /api/v1)
app.include_router(
    news.router, 
    prefix="/api/v1", 
    tags=["API v1 - Secured"]
)

# 手動觸發爬蟲 (僅供測試或即時更新)
@app.post(
    "/crawl/now", 
    tags=["Crawler"],
    # 這裡的爬蟲觸發也需要 API Key 驗證
    dependencies=[Depends(get_api_key)] 
)
async def run_crawler_now(session: AsyncSession = Depends(get_db_session)):
    """
    手動觸發一次非同步爬蟲並存入 DB (需 API Key)
    """
    print(f"Manual crawling: {settings.CRAWL_TARGET_URL}")
    articles = await fetch_news_titles(settings.CRAWL_TARGET_URL)
    
    if not articles:
        raise HTTPException(status_code=500, detail="爬蟲失敗或未抓取到任何新資料")

    inserted_count = await save_articles(session, articles)
    
    return {
        "message": "手動爬蟲完成並已存入資料庫", 
        "inserted": inserted_count, 
        "total_articles_found": len(articles)
    }

@app.get("/", include_in_schema=False)
def read_root():
    return {"message": "歡迎使用 FastAPI 新聞爬蟲作品集專案", "docs": "/docs"}
