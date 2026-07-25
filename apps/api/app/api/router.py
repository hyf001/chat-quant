from fastapi import APIRouter

from app.api.routes import artifacts, health

api_router = APIRouter()
api_router.include_router(artifacts.router)
api_router.include_router(health.router, tags=["health"])
