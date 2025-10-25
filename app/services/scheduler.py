import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.core.config import settings
from app.services.crawler import fetch_news_titles, save_articles
from app.database import get_db_session

# 使用 AsyncIOScheduler
scheduler = AsyncIOScheduler()

async def scheduled_crawl_task():
    """
    定時執行的爬蟲任務
    """
    # 由於 FastAPI 的 Dependencies 無法直接用於排程，我們手動取得 Session
    # 注意：這裡使用了 next(get_db_session()) 的變通方法，實際部署中需要更嚴謹的 Session 管理
    # 為了教學，我們假設一個簡單的同步/異步轉換
    try:
        # 由於 get_db_session 是 async generator，需要特殊的取用方式
        session_gen = get_db_session()
        # 獲取第一個也是唯一一個 session
        session = await session_gen.__anext__() 
        
        print("Running scheduled crawl task...")
        
        articles = await fetch_news_titles(settings.CRAWL_TARGET_URL)
        if articles:
            inserted_count = await save_articles(session, articles)
            print(f"Scheduled task completed. Inserted {inserted_count} new articles.")
        else:
            print("Scheduled task ran but found no new articles.")

    except Exception as e:
        print(f"Scheduled crawl task failed: {e}")
    finally:
        # 必須確保 session 關閉
        if 'session' in locals() and session:
            await session.close()
            
def start_scheduler():
    """啟動排程器"""
    # 每 X 小時執行一次
    trigger = IntervalTrigger(hours=settings.CRAWL_INTERVAL_HOURS)
    scheduler.add_job(scheduled_crawl_task, trigger)
    scheduler.start()
    print(f"Scheduler started, crawling every {settings.CRAWL_INTERVAL_HOURS} hours.")
    
def shutdown_scheduler():
    """關閉排程器"""
    if scheduler.running:
        scheduler.shutdown()
        print("Scheduler shut down.")
