from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid

from app.models import Booth
from app.schemas import BoothRead, BoothCreate
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

@router.get("/", response_model=BoothRead)
async def booth(qrcode_token: str, db: AsyncSession = Depends(get_db)):
    q = select(Booth).where(Booth.id == qrcode_token)
    result = await db.execute(q)
    existing_booth = result.scalar_one_or_none()
    if not existing_booth:
        raise HTTPException(status_code=400, detail="The booth isn't registered.")

    return {
        "id": existing_booth.id, 
        "name": existing_booth.name, 
        "description": existing_booth.description,
        "points": existing_booth.points,
        "created_at": existing_booth.created_at
    }