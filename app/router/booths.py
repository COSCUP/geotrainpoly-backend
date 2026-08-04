from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from app.database import get_session
from app.models.booths import Booth
from app.services.opass import get_current_session_id


router = APIRouter(
    prefix="/booths",
    tags=["booths"],
)


@router.get("")
async def get_booths(session: Session = Depends(get_session)):
    booths = session.query(Booth).all()
    return [
        {
            "name": booth.name,
            "type": booth.type,
            "logo": booth.logo,
            "description": booth.description,
        }
        for booth in booths
    ]

@router.get("/{booth_id}")
async def get_booth(booth_id: str, session: Session = Depends(get_session)):
    booth = session.query(Booth).filter(Booth.booth_id == booth_id).first()

    if not booth:
        raise HTTPException(status_code=404, detail="Booth not found")

    resp = {
        "name": booth.name,
        "type": booth.type,
        "logo": booth.logo,
        "description": booth.description,
    }

    if booth.type == "ROOMS":
        resp["session"] = get_current_session_id(booth.name)

    return resp
