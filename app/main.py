from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.register import register
from app.routers.whoami import whoami
from app.routers.booth import booth
from app.routers.user import user

# Init DB
from app.database import engine
from app.models import Base

app = FastAPI(title="COSCUP 2025 GeoTrainPoly")

# Init DB – create tables
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Tables created.")

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
    tags=["會眾註冊"],
)

app.include_router(
    whoami.router,
    prefix="/api/whoami",
    tags=["個人資訊"],
)

app.include_router(
    booth.router,
    prefix="/api/booth",
    tags=["攤位"],
)

app.include_router(
    user.router,
    prefix="/api/user",
    tags=["使用者"],
)
