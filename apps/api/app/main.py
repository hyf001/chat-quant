from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
    app = FastAPI(title=settings.app_name, lifespan=lifespan)
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
    return app


app = create_app()
