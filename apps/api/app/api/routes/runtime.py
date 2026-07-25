from __future__ import annotations

from functools import lru_cache

from fastapi import APIRouter, HTTPException

from app.core.config import get_settings
from app.domain.runtime.services import PythonRuntimeService
from app.schemas.contracts.execution_result import ExecutionResult, ExecutionResultEnvelope
from app.schemas.contracts.runtime_health import RuntimeHealthResponse
from app.schemas.contracts.runtime_specs import BacktestRunSpec, PythonExecutionSpec

router = APIRouter(prefix="/runtime")


@lru_cache
def get_runtime_service() -> PythonRuntimeService:
    return PythonRuntimeService(get_settings())


@router.get("/health", response_model=RuntimeHealthResponse)
async def runtime_health() -> RuntimeHealthResponse:
    return get_runtime_service().get_runtime_health()


@router.post("/execute", response_model=ExecutionResultEnvelope)
async def execute_python_artifact(spec: PythonExecutionSpec) -> ExecutionResultEnvelope:
    result = await get_runtime_service().execute_python_artifact(spec)
    return ExecutionResultEnvelope(execution_result=result)


@router.post("/backtests/execute", response_model=ExecutionResult)
async def execute_backtest_spec(spec: BacktestRunSpec) -> ExecutionResult:
    return await get_runtime_service().execute_backtest_spec(spec)


@router.post("/runs/{run_id}/cancel")
async def cancel_runtime_run(run_id: str) -> dict[str, str]:
    return await get_runtime_service().cancel_runtime_run(run_id)


@router.get("/runs/{run_id}", response_model=ExecutionResult)
async def get_runtime_run(run_id: str) -> ExecutionResult:
    result = get_runtime_service().get_result(run_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Runtime run not found")
    return result
