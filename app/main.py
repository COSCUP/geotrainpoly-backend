from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.register import register

app = FastAPI(title="COSCUP 2025 GeoTrainPoly")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to COSCUP 2025 GeoTrainPoly backend!"}

app.include_router(
    register.router,
    prefix="/api/register",
    tags=["註冊"],
)