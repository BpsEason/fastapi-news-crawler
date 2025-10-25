from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.database.models import Article
from app.database import get_db_session
from app.core.security import get_api_key

router = APIRouter()

@router.get(
    "/articles", 
    response_model=list[Article], 
    tags=["News Data"],
    # 加入 API Key 驗證，所有請求必須帶上 X-API-Key
    dependencies=[Depends(get_api_key)]
)
async def read_articles(
    # 加入分頁參數 (用於教學延伸)
    offset: int = 0, 
    limit: int = 10,
    session: AsyncSession = Depends(get_db_session)
):
    """
    安全地從資料庫中獲取文章列表 (含分頁)
    """
    # 異步查詢，帶有分頁
    statement = select(Article).offset(offset).limit(limit)
    result = await session.exec(statement)
    articles = result.all()
    return articles
