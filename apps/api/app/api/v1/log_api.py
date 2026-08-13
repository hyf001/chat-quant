from typing import Literal

from fastapi import APIRouter, Depends, Query

from app.schema.logs import LogListResponse
from app.service.log import LogService, log_service

router = APIRouter()
LogServiceDependency = Depends(log_service)


@router.get("", response_model=LogListResponse)
async def list_logs(
    limit: int = Query(default=100, ge=1, le=500),
    category: Literal["access", "business"] | None = None,
    logs: LogService = LogServiceDependency,
) -> LogListResponse:
    return logs.list_logs(limit=limit, category=category)
