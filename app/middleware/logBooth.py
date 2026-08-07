import json
import re
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.types import ASGIApp
from app.database import get_session
from app.models.log import Log

# (method, pattern) -> how to get booth_id: "path" or "body"
WHITELIST = [
    ("GET",  re.compile(r"^/api/booths/(?P<booth_id>[^/]+)$"), "path"),
    ("GET",  re.compile(r"^/api/hextiles/(?P<booth_id>[^/]+)$"), "path"),
    ("POST", re.compile(r"^/api/send$"), "body"),
    ("POST", re.compile(r"^/api/collect$"), "body"),
]


class LogBoothMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        booth_id, request = await self._match(request)

        response = await call_next(request)

        if booth_id:
            user_id = self._extract_user_id(request)
            action = f"{request.method} {request.url.path}"
            self._record(user_id, booth_id, action)

        return response

    def _extract_user_id(self, request: Request) -> str:
        auth = request.headers.get("Authorization", "")
        parts = auth.split(" ")
        if len(parts) == 2 and parts[0] == "Bearer":
            return parts[1]
        return "anonymous"

    async def _match(self, request: Request) -> tuple[str | None, Request]:
        path = request.url.path

        for method, pattern, source in WHITELIST:
            if request.method != method:
                continue
            m = pattern.match(path)
            if not m:
                continue

            if source == "path":
                return m.group("booth_id"), request

            if source == "body":
                body = await request.body()
                try:
                    data = json.loads(body)
                    booth_id = data.get("booth_id")
                    if booth_id:
                        async def receive(b=body) -> dict:
                            return {"type": "http.request", "body": b, "more_body": False}
                        return booth_id, Request(request.scope, receive)
                except (json.JSONDecodeError, AttributeError):
                    pass

        return None, request

    def _record(self, user_id: str, booth_id: str, action: str):
        db = next(get_session())
        try:
            db.add(Log(user_id=user_id, booth_id=booth_id, action=action))
            db.commit()
        except Exception:
            db.rollback()
        finally:
            db.close()
