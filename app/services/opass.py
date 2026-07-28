from datetime import datetime, timedelta, timezone
from httpx import get

TZ_TAIPEI = timezone(timedelta(hours=8))

OPASS_URL = "https://coscup.org/2026/api/opass.json"
CACHE_TTL = timedelta(minutes=5)

_cache: list = []
_last_fetched: datetime | None = None


def _fetch():
    global _cache, _last_fetched
    response = get(OPASS_URL, timeout=10)
    response.raise_for_status()
    _cache = response.json().get("sessions", [])
    _last_fetched = datetime.utcnow()


def get_sessions() -> list:
    if _last_fetched is None or datetime.utcnow() - _last_fetched > CACHE_TTL:
        _fetch()
    return _cache


def get_current_session_id(room: str) -> str | None:
    now = datetime.now(TZ_TAIPEI)
    for session in get_sessions():
        if str(session.get("room")) != str(room):
            continue
        try:
            start = datetime.fromisoformat(session["start"])
            end = datetime.fromisoformat(session["end"])
            if start.tzinfo is None:
                start = start.replace(tzinfo=TZ_TAIPEI)
            if end.tzinfo is None:
                end = end.replace(tzinfo=TZ_TAIPEI)
            if start <= now <= end:
                return session["id"]
        except (KeyError, ValueError):
            continue
    return None
