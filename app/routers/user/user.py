from fastapi import APIRouter, Depends, HTTPException
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
async def scan_info(booth_id: str, message: Optional[str] = None, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    booth_query = select(Booth).where(Booth.id == booth_id)
    booth_result = await db.execute(booth_query)
    booth = booth_result.scalar_one_or_none()
    if booth is None:
        raise HTTPException(status_code=404, detail="Booth not found.")

    q = select(Visit).where(
        and_(
            Visit.user_id == current_user.id,
            Visit.booth_id == booth_id,
            Visit.type == VisitTypeEnum.OTHER
        )
    )
    result = await db.execute(q)
    existing_visit = result.scalar_one_or_none()
    if existing_visit:
        if message is not None:
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
    try:
        db.add(new_visit)
        await db.commit()
        await db.refresh(new_visit)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to save visit record")

    return {"response": "New visit recorded", "visit": new_visit}
