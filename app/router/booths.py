from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from app.database import get_session
from app.models.booths import Booth


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
