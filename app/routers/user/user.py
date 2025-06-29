from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import Optional
from datetime import datetime

from app.auth.jwt import get_current_user
from app.models import User, Booth, Visit
from app.schemas import VisitTypeEnum
from app.database import get_db

router = APIRouter()

@router.post("/scan-info")
async def scan_info(booth_id: str, message: Optional[str] = None, current_user: str = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    q = select(Visit).where(
        and_(
            Visit.user_id == current_user.id,
            Visit.booth_id == booth_id
        )
    )
    result = await db.execute(q)
    existing_visit = result.scalar_one_or_none()
    if existing_visit:
        existing_visit.message = message
        existing_visit.visit_at = datetime.utcnow()
        await db.commit()
        await db.refresh(existing_visit)
        return {"response": "Visit updated", "visit": existing_visit}

    new_visit = Visit(
        user_id=current_user.id,
        type=VisitTypeEnum.OTHER,  # 使用者主動掃
        booth_id=booth_id,
        message=message
    )
    db.add(new_visit)
    await db.commit()
    await db.refresh(new_visit)

    return {"response": "New visit recorded", "visit": new_visit}
