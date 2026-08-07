from fastapi import FastAPI
from fastapi.routing import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app.middleware.logBooth import LogBoothMiddleware
from app.router import (
    booths_router,
    profiles_router,
    collect_router,
    send_router,
    hextiles_router,
    msg_router,
    reward_router,
    coffee_router,
)
from app.database import Base, engine

app = FastAPI(title="COSCUP 2025 GeoTrainPoly")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LogBoothMiddleware)

api = APIRouter(prefix="/api")
api.include_router(booths_router)
api.include_router(profiles_router)
api.include_router(collect_router)
api.include_router(send_router)
api.include_router(hextiles_router)
api.include_router(msg_router)
api.include_router(reward_router)
api.include_router(coffee_router)

app.include_router(api)

@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)
