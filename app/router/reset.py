from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from app.database import get_session
from app.models.userBooths import UserBooths
from app.models.userAchievement import UserAchievement
from pydantic import BaseModel


class ResetRequest(BaseModel):
    token: str


router = APIRouter(
    prefix="/reset",
    tags=["reset"],
)


@router.post("")
async def reset(body: ResetRequest, session: Session = Depends(get_session)):
    if body.token != "geotrainpoly":
        raise HTTPException(status_code=403, detail="Invalid token")

    deleted_booths = session.query(UserBooths).delete()
    deleted_achievements = session.query(UserAchievement).delete()
    session.commit()

    return {
        "deleted_user_booths": deleted_booths,
        "deleted_user_achievements": deleted_achievements,
    }
