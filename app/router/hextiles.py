from fastapi import Depends, HTTPException, Request
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session, joinedload
from app.database import get_session
from app.models.userBooths import UserBooths
from app.models.booths import Booth
from app.models.users import User
from app.models.msg import Msg
from app.middleware.getUser import get_user
from app.services.opass import get_current_session_id


router = APIRouter(
    prefix="/hextiles",
    tags=["hexttiles"],
    dependencies=[Depends(get_user)],
)


@router.get("")
async def get_hextiles(
    request: Request,
    session: Session = Depends(get_session),
    user: User = Depends(get_user),
):
    return (
        {
            "id": i.id,
            "x": i.x,
            "user_id": i.user_id,
            "booth_id": i.booth_id if i.booth.type == "ROOMS" else None,
            "name": i.booth.name,
            "logo": i.booth.logo,
            "description": i.booth.description,
            "type": i.booth.type
        }
        for i in session.query(UserBooths)
        .options(joinedload(UserBooths.booth))
        .filter(UserBooths.user_id == user.user_id)
        .order_by(UserBooths.id)
        .all()
    )

@router.get("/{booth_name:path}")
async def get_hextile(
    request: Request,
    booth_name: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_user),
):
    booth = (
        session.query(UserBooths)
        .join(Booth)
        .options(joinedload(UserBooths.booth))
        .filter(UserBooths.user_id == user.user_id, Booth.name == booth_name)
        .first()
    )

    if not booth:
        raise HTTPException(status_code=404, detail="Booth not found")

    resp = {
        "booth": booth.booth,
    }

    if booth.booth.type == "ROOMS":
        resp["session"] = get_current_session_id(booth.booth.name)

    return resp
