from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # 資料庫連線字串 (使用 PostgreSQL 範例)
    DATABASE_URL: str = "postgresql+asyncpg://user:password@db:5432/news_db"
    
    # API 驗證用的 Secret Key
    API_KEY_SECRET: str = "your-api-key-secret-placeholder"
    
    # 爬蟲設定
    CRAWL_TARGET_URL: str = "https://example.com/news"
    CRAWL_INTERVAL_HOURS: int = 6

    # FastAPI 設定
    PROJECT_NAME: str = "FastAPI News Crawler API"
    
    class Config:
        env_file = ".env" # 支援 .env 檔案

settings = Settings()
