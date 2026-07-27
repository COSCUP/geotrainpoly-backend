from app.router.booths import router as booths_router
from app.router.profiles import router as profiles_router
from app.router.collect import router as collect_router
from app.router.send import router as send_router
from app.router.hextiles import router as hextiles_router
from app.router.msg import router as msg_router
from app.router.reward import router as reward_router
from app.router.reset import router as reset_router

__all__ = [
    booths_router,
    profiles_router,
    collect_router,
    send_router,
    hextiles_router,
    msg_router,
    reward_router,
    reset_router,
]
