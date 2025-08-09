from fastapi import Depends, HTTPException, Request, BackgroundTasks
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from app.database import get_session
from app.models.booths import Booth
from app.models.users import User
from app.models.userBooths import UserBooths
from app.models.userAchievement import UserAchievement
from pydantic import BaseModel
from app.background.check_achievement import check_achievement
from httpx import get


class SendRequest(BaseModel):
    user_id: str
    booth_id: str


router = APIRouter(
    prefix="/send",
    tags=["send"],
)


@router.post("")
async def collect_point(
    request: Request, body: SendRequest, background_tasks: BackgroundTasks, session: Session = Depends(get_session)
):
    user = session.query(User).filter(User.user_id == body.user_id).first()
    booth = session.query(Booth).filter(Booth.booth_id == body.booth_id).first()

    if not booth:
        raise HTTPException(status_code=404, detail="Booth not found")

    if not user:
        response = get(f"https://ccip.opass.app/status?token={body.user_id}")

        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="User not found")

        response = response.json()

        user = User(user_id=body.user_id, name=response["user_id"], points=0)
        achievement = UserAchievement(user_id=body.user_id, achievement_id=2025)

        session.add(user)
        session.add(achievement)
        session.commit()


    user_booth = (
        session.query(UserBooths)
        .filter(
            UserBooths.user_id == body.user_id, UserBooths.booth_id == body.booth_id
        )
        .first()
    )

    if user_booth:
        raise HTTPException(status_code=400, detail="Point already collected")

    user.points += booth.points

    user_booth = UserBooths(
        user_id=body.user_id,
        booth_id=body.booth_id,
    )

    session.add(user_booth)
    session.commit()

    background_tasks.add_task(check_achievement, user.user_id, None)

    return {"detail": f"Send to {user.name} successfully"}

