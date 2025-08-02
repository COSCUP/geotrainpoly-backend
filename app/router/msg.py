from fastapi import Depends, BackgroundTasks
from fastapi.routing import APIRouter
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import Session
from app.database import get_session
from app.models.booths import Booth
from app.models.users import User
from app.models.msg import Msg
from app.middleware.getUser import get_user
from pydantic import BaseModel
from app.background.check_achievement import check_achievement


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
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
    user: User = Depends(get_user),
):
    stmt = insert(Msg).values(
        user_id=user.user_id,
        booth_id=body.booth_id,
        content=body.content,
    )
    update_stmt = stmt.on_duplicate_key_update(content=stmt.inserted.content)

    session.execute(update_stmt)
    session.commit()

    background_tasks.add_task(check_achievement, user.user_id)

    return {"message": "success"}
