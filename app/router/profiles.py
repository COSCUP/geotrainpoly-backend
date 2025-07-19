from fastapi import Depends, Request, HTTPException
from fastapi.routing import APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_session
from app.models.achievements import Achievement


router = APIRouter(
    prefix="/profiles",
    tags=["profiles"],
)


@router.get("")
async def get_profiles(request: Request, session: Session = Depends(get_session)):
    achievements = (
        session.query(Achievement)
        .filter(Achievement.user_id == request.state.user.user_id)
        .all()
    )

    user_dict = request.state.user.__dict__.copy()
    user_dict["achievements"] = achievements

    return user_dict


class UpdateTitlePayload(BaseModel):
    title: str


@router.put("")
async def update_title(
    request: Request,
    payload: UpdateTitlePayload,
    session: Session = Depends(get_session),
):
    achievements = (
        session.query(Achievement)
        .filter(Achievement.user_id == request.state.user.user_id)
        .all()
    )

    if payload.title not in [achievement.title for achievement in achievements]:
        raise HTTPException(status_code=403, detail="You don't have this title")

    user = session.merge(request.state.user)
    user.title = payload.title
    session.commit()

    return user
