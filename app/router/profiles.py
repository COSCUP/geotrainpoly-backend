from fastapi import Depends, Request
from fastapi.routing import APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_session


router = APIRouter(
    prefix="/profiles",
    tags=["profiles"],
)


@router.get("")
async def get_profiles(request: Request, session: Session = Depends(get_session)):
    return request.state.user


class UpdateTitlePayload(BaseModel):
    title: str


@router.put("")
async def update_title(
    request: Request,
    payload: UpdateTitlePayload,
    session: Session = Depends(get_session),
):
    # TODO: 判斷是否有稱號

    user = session.merge(request.state.user)
    user.title = payload.title
    session.commit()

    return user
