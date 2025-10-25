from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.database.models import SQLModel, settings

# 創建異步引擎
# 注意：這裡的 engine 必須替換為非同步版本
async_engine = create_async_engine(
    settings.DATABASE_URL, 
    echo=False, 
    future=True
)

# 異步 Session 建立器
AsyncSessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=async_engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

async def init_db():
    """初始化資料庫：建立資料表 (僅用於教學快速啟動)"""
    async with async_engine.begin() as conn:
        # 在這裡，我們模擬了 migration 的行為
        await conn.run_sync(SQLModel.metadata.create_all)
    print("Async Database initialized.")

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI 依賴注入：取得異步資料庫 Session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
