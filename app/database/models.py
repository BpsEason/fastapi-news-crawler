from datetime import datetime
from sqlmodel import SQLModel, Field, create_engine, Session
from app.core.config import settings

# 為了教學簡化，這裡省略 Alembic 設定，直接在 init_db 中建立
# 實際專案應使用 Alembic 進行 Migration

class Article(SQLModel, table=True):
    # 表名
    __tablename__ = "articles"
    
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    url: str = Field(index=True, unique=True) # 網址唯一性，用於去重
    crawled_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    
    # 類別（用於教學延伸）
    category: str = Field(default="Tech")

# 假設的異步引擎
engine = create_engine(
    settings.DATABASE_URL, 
    echo=True, 
    pool_size=10, 
    max_overflow=20
)
