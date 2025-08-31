from .auth import router as auth_router
from .users import router as users_router
from .transactions import router as transactions_router
from .goals import router as goals_router
from .analytics import router as analytics_router
from .ai import router as ai_router

__all__ = ["auth_router", "users_router", "transactions_router", "goals_router", "analytics_router", "ai_router"] 