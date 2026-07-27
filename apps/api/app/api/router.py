from fastapi import APIRouter

from app.api.routes import (
    artifacts,
    backtests,
    chat,
    chat_sessions,
    health,
    projects,
    runtime,
    strategies,
)

api_router = APIRouter()
api_router.include_router(artifacts.router)
api_router.include_router(backtests.router)
api_router.include_router(chat.router)
api_router.include_router(chat_sessions.router)
api_router.include_router(health.router, tags=["health"])
api_router.include_router(projects.router)
api_router.include_router(runtime.router)
api_router.include_router(strategies.router, tags=["strategies"])
