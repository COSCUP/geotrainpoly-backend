from fastapi import FastAPI
from fastapi.routing import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app.router import booths_router, profiles_router, collect_router
from app.middleware.auth import AuthMiddleware
from app.database import Base, engine

app = FastAPI(title="COSCUP 2025 GeoTrainPoly")

app.add_middleware(AuthMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

api = APIRouter(prefix="/api")
api.include_router(booths_router)
api.include_router(profiles_router)
api.include_router(collect_router)

app.include_router(api)
