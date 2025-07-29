from app.router.booths import router as booths_router
from app.router.profiles import router as profiles_router
from app.router.collect import router as collect_router
from app.router.send import router as send_router
from app.router.hextiles import router as hextiles_router

__all__ = [booths_router, profiles_router, collect_router, send_router, hextiles_router]
