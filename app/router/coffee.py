import random
from datetime import datetime, timezone, timedelta
from fastapi import Depends, HTTPException, Request
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from app.database import get_session
from app.models.users import User
from app.models.coffee import Coffee
from app.middleware.getUser import get_user

TZ_TAIPEI = timezone(timedelta(hours=8))
START = datetime(2026, 8, 8, 9, 0, 0, tzinfo=TZ_TAIPEI)
DEADLINE = datetime(2026, 8, 9, 16, 0, 0, tzinfo=TZ_TAIPEI)

router = APIRouter(
    prefix="/coffee",
    tags=["coffee"],
    dependencies=[Depends(get_user)],
)

AD = """\
This Grafana & Friends meetup group hosts events focused on open source monitoring and observability using Grafana and related technologies. Some meetups feature formal presentations, while others are more relaxed and discussion-driven. Every event is designed to encourage learning, connection, and community. Snacks and stickers included!
https://www.meetup.com/grafana-friends-taipei/?src=event&camp=coscup-2026
"""


@router.get("")
async def get_coffee(
    request: Request,
    session: Session = Depends(get_session),
    user: User = Depends(get_user),
):
    coffee = session.query(Coffee).filter(Coffee.user_id == user.user_id).first()

    if not coffee:
        coffee = Coffee(user_id=user.user_id)
        session.add(coffee)
        session.commit()

    return AD


@router.post("")
async def post_coffee(
    request: Request,
    session: Session = Depends(get_session),
    user: User = Depends(get_user),
):
    if datetime.now(tz=TZ_TAIPEI) < START:
        raise HTTPException(status_code=403, detail="Lottery not started yet")

    if datetime.now(tz=TZ_TAIPEI) > DEADLINE:
        raise HTTPException(status_code=403, detail="Lottery end")

    coffee = session.query(Coffee).filter(Coffee.user_id == user.user_id).first()

    if not coffee:
        raise HTTPException(status_code=403, detail="Not allowed")

    if coffee.win is not None:
        raise HTTPException(status_code=400, detail="Already drawn")

    count = session.query(Coffee).filter(Coffee.win == True).count()
    win = count < 70 and random.random() < 0.5

    coffee.win = win
    session.commit()

    return {"win": coffee.win, "reward": coffee.reward}
