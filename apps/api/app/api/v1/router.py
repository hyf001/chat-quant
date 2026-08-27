from fastapi import APIRouter

from app.api.v1 import (
    backtest_api,
    chat_api,
    chat_session_api,
    config_api,
    dataset_api,
    health_api,
    job_runtime_api,
    log_api,
    mindgo_api,
    model_provider_api,
    notebook_api,
    project_api,
    runtime_api,
    strategy_api,
)

api_router = APIRouter()
api_router.include_router(backtest_api.router, prefix="/backtests", tags=["backtests"])
api_router.include_router(chat_api.router, prefix="/chat", tags=["chat"])
api_router.include_router(chat_session_api.router, prefix="/chat-sessions", tags=["chat-sessions"])
api_router.include_router(config_api.router, prefix="/config", tags=["config"])
api_router.include_router(dataset_api.router, prefix="/datasets", tags=["datasets"])
api_router.include_router(health_api.router, tags=["health"])
api_router.include_router(job_runtime_api.router, prefix="/job-runtime", tags=["job-runtime"])
api_router.include_router(log_api.router, prefix="/logs", tags=["logs"])
api_router.include_router(mindgo_api.router, prefix="/mindgo", tags=["mindgo"])
api_router.include_router(
    model_provider_api.router,
    prefix="/model-providers",
    tags=["model-providers"],
)
api_router.include_router(notebook_api.router, prefix="/notebooks", tags=["notebooks"])
api_router.include_router(project_api.router, prefix="/projects", tags=["projects"])
api_router.include_router(runtime_api.router, prefix="/runtime", tags=["runtime"])
api_router.include_router(strategy_api.router, tags=["strategies"])
