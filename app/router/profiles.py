from fastapi import Depends, Request, HTTPException
from fastapi.routing import APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_session
from app.models.achievements import Achievement
from app.models.users import User
from app.middleware.getUser import get_user


router = APIRouter(
    prefix="/profiles",
    tags=["profiles"],
    dependencies=[Depends(get_user)],
)


@router.get("")
async def get_profiles(
    request: Request,
    session: Session = Depends(get_session),
    user: User = Depends(get_user),
):
    achievements = (
        session.query(Achievement).filter(Achievement.user_id == user.user_id).all()
    )

    user_dict = user.__dict__
    user_dict["achievements"] = achievements

    return user_dict


class UpdateTitlePayload(BaseModel):
    title: str


@router.put("")
async def update_title(
    request: Request,
    payload: UpdateTitlePayload,
    session: Session = Depends(get_session),
    user: User = Depends(get_user),
):
    achievements = (
        session.query(Achievement).filter(Achievement.user_id == user.user_id).all()
    )

    if payload.title not in [achievement.title for achievement in achievements]:
        raise HTTPException(status_code=403, detail="You don't have this title")

    user.title = payload.title
    session.commit()

    return user.__dict__
