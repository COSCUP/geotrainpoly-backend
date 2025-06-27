from fastapi import APIRouter, Security
from typing import Annotated

from app.models import User
from app.auth.jwt import get_current_user

router = APIRouter()

@router.get("/")
async def whoami(
    current_user: Annotated[User, Security(get_current_user, scopes=[""])]
):
    # WIP: Calculate "points"

    return {
        "id": current_user.id, 
        "name": current_user.name, 
        "email": current_user.email, 
        "gender": current_user.gender, 
        "role": current_user.role,
        "created_at": current_user.created_at,
        "points": ""
    }