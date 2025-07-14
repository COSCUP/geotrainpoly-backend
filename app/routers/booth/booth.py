from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from datetime import datetime
import uuid

from app.models import User, Booth, Visit
from app.schemas import BoothRead, BoothCreate, VisitTypeEnum
from app.database import get_db

router = APIRouter()

@router.post("/register", response_model=BoothRead)
async def register(booth_in: BoothCreate, db: AsyncSession = Depends(get_db)):
    q = select(Booth).where(Booth.name == booth_in.name)
    result = await db.execute(q)
    existing_booth = result.scalar_one_or_none()
    if existing_booth:
        raise HTTPException(status_code=400, detail="The booth is already registered.")

    # Save Booth data to DB
    new_booth = Booth(
        id=str(uuid.uuid4()),
        name=booth_in.name,
        description=booth_in.description,
        points=booth_in.points
    )
    db.add(new_booth)
    await db.commit()
    await db.refresh(new_booth)

    return new_booth

@router.get("/")
async def booth(qrcode_token: str, db: AsyncSession = Depends(get_db)):
    q = select(Booth).where(Booth.id == qrcode_token)
    result = await db.execute(q)
    existing_booth = result.scalar_one_or_none()

    if not existing_booth:
        raise HTTPException(status_code=404, detail="Booth not found.")

    q = select(Visit).where(Visit.booth_id == qrcode_token)
    result = await db.execute(q)
    visit_count = len(result.scalars().all())

    # TBD: show what kind of messages?
    return {
        "id": existing_booth.id, 
        "name": existing_booth.name, 
        "description": existing_booth.description,
        "points": existing_booth.points,
        "visit_count": visit_count,
        "message": "",
        "created_at": existing_booth.created_at
    }

@router.post("/scan-user")
async def scan_user(user_id: str, booth_id: str, db: AsyncSession = Depends(get_db)):
    q = select(Visit).where(
        and_(
            Visit.user_id == user_id,
            Visit.booth_id == booth_id,
            Visit.type == VisitTypeEnum.BOOTH
        )
    )
    result = await db.execute(q)
    booth_scan_record = result.scalar_one_or_none()
    if booth_scan_record:
        booth_scan_record.visit_at = datetime.utcnow()
        await db.commit()
        await db.refresh(booth_scan_record)
        message = "Visit updated"
    else:
        booth_scan_record = Visit(
            user_id=user_id,
            type=VisitTypeEnum.BOOTH,  # 使用者被掃
            booth_id=booth_id,
            message=""
        )
        db.add(booth_scan_record)
        await db.commit()
        await db.refresh(booth_scan_record)
        message = "Visit created"

    # 計算總訪問數
    q = select(Visit).where(
        and_(
            Visit.booth_id == booth_id,
            Visit.user_id == user_id,
            Visit.type == VisitTypeEnum.OTHER
        )
    )
    result = await db.execute(q)
    user_existing_visits = result.scalars().all()

    return {
        "message": message,
        "user_id": user_id,
        "booth_id": booth_id,
        "user_visit_count": len(user_existing_visits),
        "latest_booth_visit": booth_scan_record,
        "user_other_type_visits": user_existing_visits
    }
