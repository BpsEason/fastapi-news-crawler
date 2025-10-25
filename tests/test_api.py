import pytest
from httpx import AsyncClient
from app.main import app
from app.core.config import settings

# 注意: 實際專案應使用獨立的測試資料庫

@pytest.mark.asyncio
async def test_api_key_protected_endpoint():
    """測試 API Key 驗證是否生效 (無 Key 應被拒絕)"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/articles")
        assert response.status_code == 403
        assert "無效的 API Key" in response.json()["detail"]

@pytest.mark.asyncio
async def test_manual_crawl_protected():
    """測試手動爬蟲端點是否需要 API Key"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/crawl/now")
        assert response.status_code == 403

@pytest.mark.asyncio
async def test_full_crawl_and_read_flow():
    """測試整個流程: 帶 Key 觸發爬蟲 -> 帶 Key 讀取資料"""
    
    # 1. 觸發爬蟲 (POST /crawl/now)
    secret_key = settings.API_KEY_SECRET
    headers = {"X-API-Key": secret_key}
    
    async with AsyncClient(app=app, base_url="http://test", headers=headers) as client:
        
        # 觸發爬蟲
        crawl_response = await client.post("/crawl/now")
        assert crawl_response.status_code == 200
        assert crawl_response.json()["inserted"] > 0
        
        # 2. 讀取資料 (GET /api/v1/articles)
        read_response = await client.get("/api/v1/articles")
        assert read_response.status_code == 200
        data = read_response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        
        # 3. 檢查資料結構
        if data:
            article = data[0]
            assert "id" in article
            assert "title" in article
            assert "url" in article
            assert "crawled_at" in article

# 測試爬蟲服務邏輯 (不需要 API 即可測試)
@pytest.mark.asyncio
async def test_crawler_service_logic():
    from app.services.crawler import fetch_news_titles
    articles = await fetch_news_titles("https://example.com/news")
    assert len(articles) == 3
    assert articles[0].title == "非同步爬蟲優勢分析"
