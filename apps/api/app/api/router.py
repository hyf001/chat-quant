from fastapi import APIRouter

from app.api.routes import (
    artifacts,
    backtests,
    chat,
    conversations,
    health,
    strategies,
)

api_router = APIRouter()
api_router.include_router(artifacts.router)
api_router.include_router(backtests.router)
api_router.include_router(chat.router)
api_router.include_router(conversations.router)
api_router.include_router(health.router, tags=["health"])
api_router.include_router(strategies.router, tags=["strategies"])
