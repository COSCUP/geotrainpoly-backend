from fastapi import APIRouter, Depends, Response, Response, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid

from app.models import User
from app.schemas import UserRead, UserCreate
from app.database import get_db
from app.auth.jwt import create_access_token, get_current_user

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

router = APIRouter()

@router.post("/")
async def register(user_in: UserCreate, response: Response, db: AsyncSession = Depends(get_db)):
    q = select(User).where(User.name == user_in.name or User.email == user_in.email)
    result = await db.execute(q)
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="The user is already registered.")

    # Save User data to DB
    new_user = User(
        id=str(uuid.uuid4()),
        name=user_in.name,
        email=user_in.email,
        gender=user_in.gender.value,
        role=user_in.role.value
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    # Generate token (no expired)
    access_token = create_access_token(data={"sub": str(new_user.id)})

    # HTTP Only Cookie: max_age=30 days（允許不設定）
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=60 * 60 * 24 * 30,
        secure=False,
        samesite="lax",
        path="/"
    )

    return {"message": "User registered and logged in", "user_id": str(new_user.id)}

# 驗證 HTTP Only Cookie 方式，是否有將 token 存在手機中
@router.get("/protected")
async def protected_route(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello user {current_user}, you are authenticated"}
