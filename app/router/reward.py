from fastapi import Depends, HTTPException, Request
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from app.database import get_session
from app.models.users import User
from pydantic import BaseModel

class RewardRequest(BaseModel):
    user_id: str
    token: str


router = APIRouter(
    prefix="/reward",
    tags=["reward"],
)


@router.get("")
async def get_points(
    request: Request, body: RewardRequest, session: Session = Depends(get_session)
):

    if body.token != "geotrainpoly":
        raise HTTPException(status_code=403, detail="Invalid token")


    user = session.query(User).filter(User.user_id == body.user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    resp = {
        "name": user.name,
        "points": user.points,
        "reward": user.reward
    }

    return resp


@router.put("")
async def collect_point(
    request: Request, body: RewardRequest, session: Session = Depends(get_session)
):

    if body.token != "geotrainpoly":
        raise HTTPException(status_code=403, detail="Invalid token")


    user = session.query(User).filter(User.user_id == body.user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    resp = {
        "name": user.name,
        "points": user.points,
        "reward": user.reward
    }

    user.reward = True
    session.commit()


    return resp

