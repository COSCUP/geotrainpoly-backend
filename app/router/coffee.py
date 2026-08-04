from fastapi import Depends, Request
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from app.database import get_session
from app.models.users import User
from app.models.coffee import Coffee
from app.middleware.getUser import get_user


router = APIRouter(
    prefix="/coffee",
    tags=["coffee"],
    dependencies=[Depends(get_user)],
)


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
        session.refresh(coffee)

        return """
            This Grafana & Friends meetup group hosts events focused on open source monitoring and observability using Grafana and related technologies. Some meetups feature formal presentations, while others are more relaxed and discussion-driven. Every event is designed to encourage learning, connection, and community. Snacks and stickers included!

            https://www.meetup.com/grafana-friends-taipei/?src=event&camp=coscup-2026
        """

    return {
        "win": coffee.win,
        "reward": coffee.reward,
    }
