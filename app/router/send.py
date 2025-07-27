from fastapi import Depends, HTTPException, Request
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from app.database import get_session
from app.models.booths import Booth
from app.models.users import User
from app.models.userBooths import UserBooths
from pydantic import BaseModel


class SendRequest(BaseModel):
    user_id: str
    booth_id: str


router = APIRouter(
    prefix="/send",
    tags=["send"],
)


@router.post("")
async def collect_point(
    request: Request, body: SendRequest, session: Session = Depends(get_session)
):
    user = session.query(User).filter(User.user_id == body.user_id).first()
    booth = session.query(Booth).filter(Booth.booth_id == body.booth_id).first()

    if not booth:
        raise HTTPException(status_code=404, detail="Booth not found")

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    point_to_add = 0
    if booth.type == "BOOTHS":
        point_to_add = 50
    elif booth.type == "ROOMS":
        point_to_add = 10

    user.points += point_to_add

    user_booth = UserBooths(
        user_id=body.user_id,
        booth_id=body.booth_id,
    )

    session.add(user_booth)
    session.commit()

    return {"message": "Send successfully"}
