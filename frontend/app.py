import streamlit as st
import pandas as pd
import requests

# 這裡填寫你的 FastAP API 服務地址 (Docker 內或 Render/Fly.io 部署後)
API_BASE_URL = "http://127.0.0.1:8000"
ARTICLES_URL = f"{API_BASE_URL}/api/v1/articles"
CRAWL_URL = f"{API_BASE_URL}/crawl/now"

st.set_page_config(layout="wide")

st.title("新聞爬蟲數據儀表板 (Streamlit)")

# 取得 API Key
api_key = st.sidebar.text_input("輸入 API Key (預設值: your-your-api-key-secret-placeholder)", type="password")

if not api_key:
    st.error("請在側邊欄輸入 API Key 以繼續。")
else:
    headers = {"X-API-Key": api_key}
    
    # --- 數據抓取與展示 ---
    st.header("最新文章列表")

    @st.cache_data(ttl=600) # 緩存 10 分鐘
    def load_data(url, headers):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            st.error(f"API 連線錯誤: {e}. 請確認 FastAPI 服務是否運行在 {API_BASE_URL}")
            return []

    articles = load_data(ARTICLES_URL, headers)
    
    if articles:
        # 轉換為 DataFrame 進行美化
        df = pd.DataFrame(articles)
        df['crawled_at'] = pd.to_datetime(df['crawled_at']).dt.strftime('%Y-%m-%d %H:%M:%S')
        df = df[['title', 'url', 'category', 'crawled_at']]
        
        # 顯示資料表
        st.dataframe(df, use_container_width=True)

        # 簡單統計
        st.subheader("文章數量統計")
        col1, col2 = st.columns(2)
        col1.metric("總文章數", len(df))
        col2.metric("文章類別數量", df['category'].nunique())
        
        # 視覺化 (簡單長條圖)
        st.subheader("文章類別分佈")
        category_counts = df['category'].value_counts().reset_index()
        category_counts.columns = ['Category', 'Count']
        st.bar_chart(category_counts.set_index('Category'))
    else:
        st.warning("資料庫中沒有文章，請先手動觸發爬蟲或等待排程執行。")
        
    # --- 手動觸發爬蟲按鈕 ---
    st.sidebar.markdown("---")
    st.sidebar.subheader("手動任務觸發")
    if st.sidebar.button("立即執行爬蟲 (需 API Key)"):
        with st.spinner('正在執行爬蟲並寫入資料庫...'):
            try:
                crawl_response = requests.post(CRAWL_URL, headers=headers, timeout=30)
                crawl_response.raise_for_status()
                result = crawl_response.json()
                st.sidebar.success(f"爬蟲成功！新增了 {result['inserted']} 篇文章。")
                # 清除緩存，強制重新載入數據
                load_data.clear() 
            except requests.exceptions.RequestException as e:
                st.sidebar.error(f"手動爬蟲失敗: {e}. 請檢查 API Key 或服務狀態。")

st.markdown("---")
st.markdown("API Documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)")
