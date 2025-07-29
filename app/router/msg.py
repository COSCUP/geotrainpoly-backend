from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from app.database import get_session
from app.models.booths import Booth
from app.models.users import User
from app.models.msg import Msg
from app.middleware.getUser import get_user
from pydantic import BaseModel


router = APIRouter(
    prefix="/msg",
    tags=["msg"],
    dependencies=[Depends(get_user)],
)


class CreateMsgPayload(BaseModel):
    booth_id: str
    content: str


@router.post("")
async def create_msg(
    body: CreateMsgPayload,
    session: Session = Depends(get_session),
    user: User = Depends(get_user),
):
    msg = Msg(
        user_id=user.user_id,
        booth_id=body.booth_id,
        content=body.content,
    )

    session.add(msg)
    session.commit()

    return msg.__dict__
