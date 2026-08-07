from datetime import datetime, timedelta, timezone
from threading import Thread
from httpx import get

TZ_TAIPEI = timezone(timedelta(hours=8))

OPASS_URL = "https://coscup.org/2026/api/opass.json"
CACHE_TTL = timedelta(minutes=5)

_sessions: list = []
_data_hash: str | None = None
_last_fetched: datetime | None = None


def _fetch():
    global _sessions, _last_fetched, _data_hash

    response = get(OPASS_URL, timeout=10)
    response.raise_for_status()

    data_hash = hash(response.text)

    if _data_hash == data_hash:
        _last_fetched = datetime.utcnow()
        return

    data = response.json()

    room_id_to_name = {room["id"]: room["en"]["name"] for room in data.get("rooms", [])}
    speaker_map = {s["id"]: s for s in data.get("speakers", [])}

    sessions = data.get("sessions", [])
    for session in sessions:
        session["room_name"] = room_id_to_name.get(session.get("room"))
        session["speakers"] = [speaker_map[sid]["en"]["name"] for sid in session.get("speakers", []) if sid in speaker_map]

    _sessions = sessions
    _last_fetched = datetime.utcnow()
    _data_hash = data_hash


def _ensure_fresh():
    if _last_fetched is None:
        _fetch()
    elif datetime.utcnow() - _last_fetched > CACHE_TTL:
        Thread(target=_fetch, daemon=True).start()


def get_current_session_id(room_name: str) -> str | None:
    _ensure_fresh()

    now = datetime.now(TZ_TAIPEI)
    next_session = None
    next_start = None

    for session in _sessions:
        if session.get("room_name") != room_name:
            continue
        try:
            start = datetime.fromisoformat(session["start"])
            end = datetime.fromisoformat(session["end"])
            if start.tzinfo is None:
                start = start.replace(tzinfo=TZ_TAIPEI)
            if end.tzinfo is None:
                end = end.replace(tzinfo=TZ_TAIPEI)
            if start <= now <= end:
                return session
            if start > now and (next_start is None or start < next_start):
                next_start = start
                next_session = session
        except (KeyError, ValueError):
            continue
    return next_session
