from fastapi import Depends, HTTPException, Request
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from app.database import get_session
from app.models.booths import Booth
from app.models.users import User
from app.models.userBooths import UserBooths
from pydantic import BaseModel
from app.middleware.getUser import get_user


class CollectRequest(BaseModel):
    booth_id: str
    x: int


router = APIRouter(
    prefix="/collect",
    tags=["collect"],
    dependencies=[Depends(get_user)],
)


@router.post("")
async def collect_point(
    request: Request,
    body: CollectRequest,
    session: Session = Depends(get_session),
    user: User = Depends(get_user),
):
    user_id = user.user_id
    booth = session.query(Booth).filter(Booth.booth_id == body.booth_id).first()

    if not booth:
        raise HTTPException(status_code=404, detail="Booth not found")

    user_booth = (
        session.query(UserBooths)
        .filter(UserBooths.user_id == user_id, UserBooths.booth_id == body.booth_id)
        .first()
    )

    if user_booth:
        raise HTTPException(status_code=400, detail="Point already collected")

    point_to_add = 0
    if booth.type == "BOOTHS":
        point_to_add = 50
    elif booth.type == "ROOMS":
        point_to_add = 10

    user.points += point_to_add

    user_booth = UserBooths(
        user_id=user_id,
        booth_id=body.booth_id,
        x=body.x,
    )

    session.add(user_booth)
    session.commit()

    return {"message": "Point collected successfully"}
