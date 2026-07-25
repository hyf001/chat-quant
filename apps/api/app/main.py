from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import get_settings
from app.core.logging import RequestLoggingMiddleware, configure_logging, get_logger

logger = get_logger(__name__)


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings)
    app = FastAPI(title=settings.app_name)
    logger.info(
        "creating FastAPI app",
        extra={"app_name": settings.app_name, "environment": settings.environment},
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(
        RequestLoggingMiddleware,
        enabled=settings.access_log_enabled,
        slow_threshold_ms=settings.access_log_slow_threshold_ms,
    )

    app.include_router(api_router, prefix=settings.api_prefix)
    return app


app = create_app()
