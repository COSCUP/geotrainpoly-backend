from fastapi import FastAPI
from fastapi.routing import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app.router import booths_router
from app.middleware.auth import AuthMiddleware


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

app.include_router(api)
