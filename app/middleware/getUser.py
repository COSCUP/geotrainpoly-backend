from fastapi import Depends, Request, HTTPException
from sqlalchemy.orm import Session
from app.database import get_session
from app.models.users import User


def get_user(request: Request, session: Session = Depends(get_session)) -> User:
    authorization = request.headers.get("Authorization")

    if not authorization:
        raise HTTPException(status_code=403, detail="Token Invalid")

    term, token = authorization.split(" ")

    if term != "Bearer":
        raise HTTPException(status_code=403, detail="Token Invalid")

    user = session.query(User).filter(User.user_id == token).first()

    if not user:
        raise HTTPException(status_code=403, detail="Token Invalid")

    # TODO: check opass

    return user
