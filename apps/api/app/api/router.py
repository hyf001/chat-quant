from fastapi import APIRouter

from app.api.routes import health, runtime

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(runtime.router, tags=["runtime"])
