from .user import router as user_router
from .objects import router as objects_router

routers_list = [
    user_router,
    objects_router,
]

__all__ = [
    'routers_list',
]
