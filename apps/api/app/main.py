from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.agent_runtime.custom_tools.chatq_visualization import (
    VISUALIZATION_ASSET_ROUTE,
    VISUALIZATION_STATIC_DIR,
)
from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.logging import RequestLoggingMiddleware, configure_logging, get_logger
from app.service.job_runtime import JobRuntimeWorker, register_default_job_runtime_events

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    register_default_job_runtime_events()
    settings = get_settings()
    worker = JobRuntimeWorker(
        creation_tick_minutes=settings.job_runtime_creation_tick_minutes,
        dispatch_interval_seconds=settings.job_runtime_dispatch_interval_seconds,
        dispatch_limit=settings.job_runtime_dispatch_limit,
        max_concurrent_instances=settings.job_runtime_max_concurrent_instances,
    )
    worker.start()
    app.state.job_runtime_worker = worker
    try:
        yield
    finally:
        await worker.stop()


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings)
    app = FastAPI(title=settings.app_name, 
                  docs_url=None,
                  redoc_url=None,
                  openapi_url=None,
                  lifespan=lifespan)
    logger.info(
        "creating FastAPI app",
        extra={"app_name": settings.app_name, "environment": settings.environment},
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
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
    api_visualization_asset_route = (
        f"{settings.api_prefix.rstrip('/')}{VISUALIZATION_ASSET_ROUTE}"
        if settings.api_prefix.rstrip("/")
        else VISUALIZATION_ASSET_ROUTE
    )
    if api_visualization_asset_route != VISUALIZATION_ASSET_ROUTE:
        app.mount(
            api_visualization_asset_route,
            StaticFiles(directory=VISUALIZATION_STATIC_DIR),
            name="api-visualization-assets",
        )
    app.mount(
        VISUALIZATION_ASSET_ROUTE,
        StaticFiles(directory=VISUALIZATION_STATIC_DIR),
        name="visualization-assets",
    )
    return app


app = create_app()
