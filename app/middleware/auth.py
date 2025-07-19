from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from app.database import get_session


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        authorization = request.headers.get("Authorization")

        if not authorization:
            return JSONResponse(status_code=403, content={"msg": "Token Invalid"})

        term, token = authorization.split(" ")

        if term != "Bearer":
            return JSONResponse(status_code=403, content={"msg": "Token Invalid"})

        # TODO: check in database or opass

        request.state.token = token
        response = await call_next(request)
        return response
