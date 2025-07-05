from fastapi import APIRouter, Depends

from app.models import User
from app.auth.jwt import get_current_user

router = APIRouter()

@router.get("/")
async def whoami(current_user=Depends(get_current_user)):
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
