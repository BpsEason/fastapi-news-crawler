from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN
from app.core.config import settings

# 假設 API Key 放在 Header 中，名稱為 X-API-Key
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

# 簡單模擬 API Key 驗證
# 實際應用應使用 hash 比較，這裡為了教學簡化
async def get_api_key(api_key: str = Security(api_key_header)):
    """
    驗證 API Key 是否有效
    """
    # 警告: 實際環境中，您應該比較 API Key 的 HASH 值
    if api_key == settings.API_KEY_SECRET:
        return api_key
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="無效的 API Key"
        )
