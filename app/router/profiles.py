from fastapi import Depends, Request
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from app.database import get_session
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
    return user.__dict__
