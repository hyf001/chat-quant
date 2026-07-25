from fastapi import APIRouter

from app.api.routes import backtests, health

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(backtests.router)
api_router.include_router(backtests.strategy_backtests_router)
