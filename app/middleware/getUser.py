from fastapi import Depends, Request, HTTPException
from sqlalchemy.orm import Session
from app.database import get_session
from app.models.users import User
from app.models.userAchievement import UserAchievement
from httpx import get


def get_user(request: Request, session: Session = Depends(get_session)) -> User:
    authorization = request.headers.get("Authorization")

    if not authorization:
        raise HTTPException(status_code=403, detail="Token Invalid")

    authorization = authorization.split(" ")

    if len(authorization) != 2:
        raise HTTPException(status_code=403, detail="Token Invalid")

    term, token = authorization

    if term != "Bearer":
        raise HTTPException(status_code=403, detail="Token Invalid")

    user = session.query(User).filter(User.user_id == token).first()

    if not user:
        response = get(f"https://ccip.opass.app/status?token={token}")

        if response.status_code != 200:
            raise HTTPException(status_code=403, detail="Token Invalid")

        response = response.json()

        user = User(user_id=token, name=response["user_id"], points=0)
        achievement = UserAchievement(user_id=token, achievement_id=2025)

        session.add(user)
        session.add(achievement)
        session.commit()

        return user

    return user
