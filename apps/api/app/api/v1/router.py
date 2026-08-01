from fastapi import APIRouter

from app.api.v1 import (
    backtest_api,
    chat_api,
    chat_session_api,
    health_api,
    project_api,
    runtime_api,
    strategy_api,
)

api_router = APIRouter()
api_router.include_router(backtest_api.router, prefix="/backtests", tags=["backtests"])
api_router.include_router(chat_api.router, prefix="/chat", tags=["chat"])
api_router.include_router(chat_session_api.router, prefix="/chat-sessions", tags=["chat-sessions"])
api_router.include_router(health_api.router, tags=["health"])
api_router.include_router(project_api.router, prefix="/projects", tags=["projects"])
api_router.include_router(runtime_api.router, prefix="/runtime", tags=["runtime"])
api_router.include_router(strategy_api.router, tags=["strategies"])
