from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from app.database import SessionLocal
from app.models.users import User


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        authorization = request.headers.get("Authorization")

        if not authorization:
            return JSONResponse(status_code=403, content={"msg": "Token Invalid"})

        term, token = authorization.split(" ")

        if term != "Bearer":
            return JSONResponse(status_code=403, content={"msg": "Token Invalid"})

        with SessionLocal() as session:
            user = session.query(User).filter(User.user_id == token).first()
            session.close()

            if not user:
                return JSONResponse(status_code=403, content={"msg": "Token Invalid"})

            else:
                request.state.user = user
                response = await call_next(request)
                return response
