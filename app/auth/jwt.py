from fastapi import HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import httpx
from httpx import ReadTimeout, HTTPError

from app.models import User
from app.database import get_db

# JWT 設定
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30
OPASS_API_URL = "https://ccip.opass.app/status"

role_map = {
    "audience": "ATTENDEE",
    "volunteer": "STAFF",
    "staff": "STAFF",
    "admin": "ADMIN",
}

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: AsyncSession = Depends(get_db)
):
    token = credentials.credentials

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{OPASS_API_URL}?token={token}")
    except ReadTimeout:
        raise HTTPException(status_code=504, detail="OPASS API timeout")
    except HTTPError as e:
        raise HTTPException(status_code=502, detail=f"OPASS API error: {str(e)}")

    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Token verification failed")

    try:
        data = response.json()
        user_id = data["token"]
        name = data["user_id"]
        role = role_map.get(data.get("role", "ATTENDEE"))
    except (KeyError, ValueError) as e:
        raise HTTPException(status_code=500, detail="Invalid response from OPASS")

    # 查詢或新增使用者
    q = select(User).where(User.id == user_id)
    result = await db.execute(q)
    user = result.scalar_one_or_none()

    if not user:
        user = User(id=user_id, name=name, role=role)
        db.add(user)
        await db.commit()
        await db.refresh(user)

    return user
