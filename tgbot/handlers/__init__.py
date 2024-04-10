from .admin import admin_router
from .echo import echo_router
from .user import user_router


routers_list = [
    admin_router,
    user_router,

    echo_router
]

__all__ = [
    "routers_list",
]
