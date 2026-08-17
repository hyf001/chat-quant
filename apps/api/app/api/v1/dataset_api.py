from typing import Annotated

from fastapi import APIRouter, Query, Response, status

from app.api.v1.dependencies import DatabaseSession
from app.schema.dataset import (
    DatasetDetailResponse,
    DatasetListResponse,
    DatasetPayload,
    DatasetQueryPayload,
    DatasetQueryResponse,
    DatasetResponse,
    DatasetUpdatePayload,
)
from app.service.dataset import DatasetService

router = APIRouter()


@router.get("", response_model=DatasetListResponse)
async def list_datasets(
    db: DatabaseSession,
    exposed_to_agent: Annotated[bool | None, Query()] = None,
) -> DatasetListResponse:
    return await DatasetService(db).list_datasets(exposed_to_agent=exposed_to_agent)


@router.post("", response_model=DatasetDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_dataset(
    payload: DatasetPayload,
    db: DatabaseSession,
) -> DatasetDetailResponse:
    return await DatasetService(db).create_dataset(payload)


@router.post("/query", response_model=DatasetQueryResponse)
async def query_datasets(
    payload: DatasetQueryPayload,
    db: DatabaseSession,
) -> DatasetQueryResponse:
    return await DatasetService(db).query_dataset_sql(payload)


@router.get("/{dataset_id}", response_model=DatasetDetailResponse)
async def get_dataset(dataset_id: str, db: DatabaseSession) -> DatasetDetailResponse:
    return await DatasetService(db).get_dataset(dataset_id)


@router.put("/{dataset_id}", response_model=DatasetResponse)
async def update_dataset(
    dataset_id: str,
    payload: DatasetUpdatePayload,
    db: DatabaseSession,
) -> DatasetResponse:
    return await DatasetService(db).update_dataset(dataset_id, payload)


@router.delete("/{dataset_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dataset(dataset_id: str, db: DatabaseSession) -> Response:
    await DatasetService(db).delete_dataset(dataset_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
