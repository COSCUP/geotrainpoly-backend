from fastapi import Depends, HTTPException, Request, BackgroundTasks
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from app.database import get_session
from app.models.booths import Booth
from app.models.users import User
from app.models.userBooths import UserBooths
from pydantic import BaseModel
from app.background.check_achievement import check_achievement

class RewardRequest(BaseModel):
    user_id: str
    token: str


router = APIRouter(
    prefix="/reward",
    tags=["reward"],
)


@router.post("")
async def collect_point(
    request: Request, body: RewardRequest, session: Session = Depends(get_session)
):

    if body.token != "geotrainpoly":
        raise HTTPException(status_code=403, detail="Invalid token")


    user = session.query(User).filter(User.user_id == body.user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.reward = True
    session.commit()

    return user

