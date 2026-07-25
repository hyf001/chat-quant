from fastapi import APIRouter

from app.api.routes import artifacts, health
from app.api.routes import conversations

api_router = APIRouter()
api_router.include_router(artifacts.router)
api_router.include_router(health.router, tags=["health"])
api_router.include_router(conversations.router)
