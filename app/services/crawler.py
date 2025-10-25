import httpx
from bs4 import BeautifulSoup
from app.database.models import Article

# 爬蟲模擬函數
async def fetch_news_titles(url: str) -> list[Article]:
    """
    非同步爬蟲邏輯：使用 httpx 抓取並解析資料。
    注意：此處的 URL 解析邏輯仍為模擬。
    """
    print(f"Async fetching from: {url}")
    
    # 模擬實際的非同步 HTTP 請求
    async with httpx.AsyncClient(timeout=10.0) as client:
        # 由於是教學，我們直接返回模擬內容，避免外部網站依賴
        if url == "https://example.com/news":
            # 模擬更豐富的內容，包含標題和網址
            mock_html = """
            <html><body>
                <article><a href="/post/1"><h2 class="title">非同步爬蟲優勢分析</h2></a></article>
                <article><a href="/post/2"><h2 class="title">PostgreSQL 與 SQLModel 實戰</h2></a></article>
                <article><a href="/post/3"><h2 class="title">FastAPI 速率限制與部署</h2></a></article>
            </body></html>
            """
            response_text = mock_html
        else:
            try:
                # 實際請求 (若要測試請替換成真實網址)
                response = await client.get(url)
                response.raise_for_status()
                response_text = response.text
            except httpx.RequestError as e:
                print(f"HTTP Request Error: {e}")
                return []

    soup = BeautifulSoup(response_text, "html.parser")
    articles: list[Article] = []
    
    # 假設文章結構：<article><a href="URL"><h2 class="title">TITLE</h2></a></article>
    for article_tag in soup.select("article"):
        link = article_tag.select_one("a")
        title_tag = article_tag.select_one("h2.title")
        
        if link and title_tag:
            title = title_tag.text.strip()
            # 確保網址是絕對路徑 (這裡仍是相對路徑的模擬)
            url = f"https://example.com{link['href']}"
            articles.append(Article(title=title, url=url))
            
    return articles

# 儲存邏輯 (為了模組化，將其移至 service 層)
async def save_articles(session: AsyncSession, articles: list[Article]) -> int:
    """
    將文章存入資料庫，包含 URL 唯一性去重檢查。
    """
    inserted_count = 0
    from sqlalchemy import select
    
    for article in articles:
        # 檢查 URL 是否已存在 (去重邏輯)
        statement = select(Article).where(Article.url == article.url)
        existing_article = (await session.exec(statement)).first()

        if not existing_article:
            session.add(article)
            inserted_count += 1
            
    await session.commit()
    return inserted_count
