from fastapi import APIRouter

from app.api.routes import health, runtime
from app.api.routes import artifacts, conversations

api_router = APIRouter()
api_router.include_router(artifacts.router)
api_router.include_router(health.router, tags=["health"])
api_router.include_router(conversations.router)
api_router.include_router(runtime.router, tags=["runtime"])
