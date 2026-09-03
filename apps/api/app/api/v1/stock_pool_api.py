from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Response, status

from app.api.v1.dependencies import DatabaseSession
from app.schema.stock_pool import (
    StockPoolBulkCreateResult,
    StockPoolCandidateListResponse,
    StockPoolCreate,
    StockPoolDetail,
    StockPoolListResponse,
    StockPoolRecord,
    StockPoolSnapshotImportRequest,
    StockPoolSnapshotImportResult,
    StockPoolStockCreate,
    StockPoolStockListResponse,
    StockPoolStockRecord,
    StockPoolStocksBulkCreate,
    StockPoolStockUpdate,
    StockPoolUpdate,
)
from app.service.stock_pool import StockPoolError, StockPoolService

router = APIRouter()


@router.get("", response_model=StockPoolListResponse)
async def list_stock_pools(
    db: DatabaseSession,
    project_id: Annotated[str, Query(min_length=1)],
) -> StockPoolListResponse:
    try:
        return await StockPoolService(db).list_stock_pools(project_id)
    except StockPoolError as error:
        raise _http_error(error) from error


@router.post("", response_model=StockPoolRecord, status_code=status.HTTP_201_CREATED)
async def create_stock_pool(
    payload: StockPoolCreate,
    db: DatabaseSession,
) -> StockPoolRecord:
    try:
        return await StockPoolService(db).create_stock_pool(payload)
    except StockPoolError as error:
        raise _http_error(error) from error


@router.get("/{pool_id}", response_model=StockPoolDetail)
async def get_stock_pool(
    pool_id: str,
    db: DatabaseSession,
    include_stocks: bool = True,
) -> StockPoolDetail:
    try:
        return await StockPoolService(db).get_stock_pool(
            pool_id,
            include_stocks=include_stocks,
        )
    except StockPoolError as error:
        raise _http_error(error) from error


@router.patch("/{pool_id}", response_model=StockPoolRecord)
async def update_stock_pool(
    pool_id: str,
    payload: StockPoolUpdate,
    db: DatabaseSession,
) -> StockPoolRecord:
    try:
        return await StockPoolService(db).update_stock_pool(pool_id, payload)
    except StockPoolError as error:
        raise _http_error(error) from error


@router.delete("/{pool_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_stock_pool(pool_id: str, db: DatabaseSession) -> Response:
    try:
        await StockPoolService(db).delete_stock_pool(pool_id)
    except StockPoolError as error:
        raise _http_error(error) from error
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{pool_id}/stock-candidates", response_model=StockPoolCandidateListResponse)
async def search_stock_candidates(
    pool_id: str,
    db: DatabaseSession,
    query: Annotated[str | None, Query(max_length=120)] = None,
    limit: Annotated[int, Query(ge=1, le=200)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> StockPoolCandidateListResponse:
    try:
        return await StockPoolService(db).search_snapshot_info_candidates(
            pool_id,
            query=query,
            limit=limit,
            offset=offset,
        )
    except StockPoolError as error:
        raise _http_error(error) from error


@router.post(
    "/{pool_id}/stocks/import-snapshot-info",
    response_model=StockPoolSnapshotImportResult,
    status_code=status.HTTP_201_CREATED,
)
async def import_snapshot_info_stocks(
    pool_id: str,
    db: DatabaseSession,
    payload: StockPoolSnapshotImportRequest | None = None,
) -> StockPoolSnapshotImportResult:
    try:
        return await StockPoolService(db).import_snapshot_info_stocks(pool_id, payload)
    except StockPoolError as error:
        raise _http_error(error) from error


@router.get("/{pool_id}/stocks", response_model=StockPoolStockListResponse)
async def list_pool_stocks(
    pool_id: str,
    db: DatabaseSession,
    query: Annotated[str | None, Query(max_length=120)] = None,
    limit: Annotated[int, Query(ge=1, le=500)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> StockPoolStockListResponse:
    try:
        return await StockPoolService(db).list_pool_stocks(
            pool_id,
            query=query,
            limit=limit,
            offset=offset,
        )
    except StockPoolError as error:
        raise _http_error(error) from error


@router.post(
    "/{pool_id}/stocks",
    response_model=StockPoolStockRecord,
    status_code=status.HTTP_201_CREATED,
)
async def add_pool_stock(
    pool_id: str,
    payload: StockPoolStockCreate,
    db: DatabaseSession,
) -> StockPoolStockRecord:
    try:
        return await StockPoolService(db).add_pool_stock(pool_id, payload)
    except StockPoolError as error:
        raise _http_error(error) from error


@router.post(
    "/{pool_id}/stocks/bulk",
    response_model=StockPoolBulkCreateResult,
    status_code=status.HTTP_201_CREATED,
)
async def bulk_add_pool_stocks(
    pool_id: str,
    payload: StockPoolStocksBulkCreate,
    db: DatabaseSession,
) -> StockPoolBulkCreateResult:
    try:
        return await StockPoolService(db).bulk_add_pool_stocks(pool_id, payload)
    except StockPoolError as error:
        raise _http_error(error) from error


@router.patch("/stocks/{stock_id}", response_model=StockPoolStockRecord)
async def update_pool_stock(
    stock_id: str,
    payload: StockPoolStockUpdate,
    db: DatabaseSession,
) -> StockPoolStockRecord:
    try:
        return await StockPoolService(db).update_pool_stock(stock_id, payload)
    except StockPoolError as error:
        raise _http_error(error) from error


@router.delete("/stocks/{stock_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pool_stock(stock_id: str, db: DatabaseSession) -> Response:
    try:
        await StockPoolService(db).delete_pool_stock(stock_id)
    except StockPoolError as error:
        raise _http_error(error) from error
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def _http_error(error: StockPoolError) -> HTTPException:
    detail = {"error_code": error.error_code, "message": error.message}
    if error.detail:
        detail.update(error.detail)
    return HTTPException(status_code=error.status_code, detail=detail)
