from fastapi import APIRouter

from app.api.routes import conversations, health

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(conversations.router)
