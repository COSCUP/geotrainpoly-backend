from fastapi import Depends, HTTPException, Request
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session, joinedload
from app.database import get_session
from app.models.userBooths import UserBooths


router = APIRouter(
    prefix="/hextiles",
    tags=["hexttiles"],
)


@router.get("")
async def get_hextiles(request: Request, session: Session = Depends(get_session)):
    user = session.merge(request.state.user)

    return (
        session.query(UserBooths)
        .options(joinedload(UserBooths.booth))
        .filter(UserBooths.user_id == user.user_id)
        .all()
    )
