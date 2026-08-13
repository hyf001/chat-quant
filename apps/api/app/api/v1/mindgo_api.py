from __future__ import annotations

from importlib import import_module
from typing import Any

from fastapi import APIRouter, HTTPException, status

from app.schema.mindgo import (
    MindgoConnectionTestRequest,
    MindgoConnectionTestResponse,
    MindgoDatasetListResponse,
    MindgoDatasetQueryRequest,
    MindgoDatasetQueryResponse,
    MindgoDatasetSchema,
    MindgoDatasetSyncRequest,
    MindgoDatasetSyncResult,
)

router = APIRouter()


@router.get("/datasets", response_model=MindgoDatasetListResponse)
async def list_mindgo_datasets() -> MindgoDatasetListResponse:
    service = _mindgo_service()
    return await service.list_datasets()


@router.post("/test", response_model=MindgoConnectionTestResponse)
async def test_mindgo_connection(
    payload: MindgoConnectionTestRequest,
) -> MindgoConnectionTestResponse:
    service = _mindgo_service()
    return await service.test_connection(payload)


@router.get("/datasets/{dataset_id}/schema", response_model=MindgoDatasetSchema)
async def get_mindgo_dataset_schema(dataset_id: str) -> MindgoDatasetSchema:
    service = _mindgo_service()
    try:
        return await service.get_schema(dataset_id)
    except service.MindgoDatasetNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"MindGo 数据集不存在：{error.dataset_id}",
        ) from error


@router.post("/datasets/{dataset_id}/query", response_model=MindgoDatasetQueryResponse)
async def query_mindgo_dataset(
    dataset_id: str,
    payload: MindgoDatasetQueryRequest,
) -> MindgoDatasetQueryResponse:
    service = _mindgo_service()
    try:
        return await service.query_dataset(dataset_id, payload)
    except service.MindgoDatasetNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"MindGo 数据集不存在：{error.dataset_id}",
        ) from error
    except RuntimeError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(error),
        ) from error


@router.post("/datasets/{dataset_id}/sync", response_model=MindgoDatasetSyncResult)
async def sync_mindgo_dataset(
    dataset_id: str,
    payload: MindgoDatasetSyncRequest,
) -> MindgoDatasetSyncResult:
    service = _mindgo_service()
    try:
        return await service.sync_dataset(dataset_id, payload)
    except service.MindgoDatasetNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"MindGo 数据集不存在：{error.dataset_id}",
        ) from error
    except RuntimeError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(error),
        ) from error


def _mindgo_service() -> Any:
    return import_module("app.service.mindgo.service")
