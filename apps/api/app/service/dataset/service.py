from __future__ import annotations

import math
from datetime import date, datetime
from decimal import Decimal
from uuid import uuid4

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.model.dataset import DatasetRow
from app.schema.dataset import (
    DatasetDetailResponse,
    DatasetListResponse,
    DatasetPayload,
    DatasetQueryColumn,
    DatasetQueryPayload,
    DatasetQueryResponse,
    DatasetResponse,
    DatasetUpdatePayload,
)
from app.schema.dataset.taxonomy import (
    ASSET_CLASS_ENGLISH,
    FREQUENCY_ENGLISH,
    MARKET_ENGLISH,
    DatasetAssetClass,
    DatasetFrequency,
    DatasetMarket,
)
from app.storage import (
    DuckDBViewAlreadyExistsError,
    DuckDBViewNotFoundError,
    DuckDBViewStore,
    DuckDBViewStoreError,
    duckdb_dataset_path,
)


class DatasetService:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db
        self._view_store = DuckDBViewStore(duckdb_dataset_path(get_settings().database_path))

    async def list_datasets(
        self,
        *,
        exposed_to_agent: bool | None = None,
    ) -> DatasetListResponse:
        statement = select(DatasetRow).order_by(DatasetRow.updated_at.desc(), DatasetRow.id)
        if exposed_to_agent is not None:
            statement = statement.where(DatasetRow.exposed_to_agent == exposed_to_agent)
        result = await self._db.execute(statement)
        return DatasetListResponse(
            datasets=[_dataset_response(row) for row in result.scalars()]
        )

    async def create_dataset(self, payload: DatasetPayload) -> DatasetDetailResponse:
        dataset_id = _dataset_id_from_payload(payload)
        view_name = payload.name.strip()
        await self._ensure_dataset_is_available(dataset_id, view_name)
        try:
            self._view_store.create_view(view_name, payload.create_sql)
        except DuckDBViewAlreadyExistsError as error:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="DuckDB view already exists",
            ) from error
        except DuckDBViewStoreError as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(error),
            ) from error

        now = datetime.now()
        row = DatasetRow(
            id=dataset_id,
            name=view_name,
            description=payload.description.strip(),
            category_path_json=list(payload.category_path),
            exposed_to_agent=payload.exposed_to_agent,
            created_at=now,
            updated_at=now,
        )
        self._db.add(row)
        try:
            await self._db.commit()
        except IntegrityError as error:
            await self._db.rollback()
            self._view_store.drop_view(view_name)
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Dataset id or DuckDB view name already exists",
            ) from error
        await self._db.refresh(row)
        return _dataset_detail_response(row, payload.create_sql)

    async def get_dataset(self, dataset_id: str) -> DatasetDetailResponse:
        row = await self._require_dataset(dataset_id)
        try:
            create_sql = self._view_store.get_create_sql(row.name)
        except DuckDBViewNotFoundError as error:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="DuckDB view bound to dataset was not found",
            ) from error
        except DuckDBViewStoreError as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(error),
            ) from error
        return _dataset_detail_response(row, create_sql)

    async def query_dataset_sql(self, payload: DatasetQueryPayload) -> DatasetQueryResponse:
        try:
            columns, rows, total = self._view_store.query(
                payload.sql,
                page=payload.page,
                page_size=payload.page_size,
            )
        except DuckDBViewStoreError as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(error),
            ) from error
        return DatasetQueryResponse(
            page=payload.page,
            page_size=payload.page_size,
            total=total,
            total_pages=math.ceil(total / payload.page_size) if total else 0,
            columns=[
                DatasetQueryColumn(name=name, value_type=_dataset_value_type(raw_type))
                for name, raw_type in columns
            ],
            rows=[
                {key: _json_value(value) for key, value in row.items()}
                for row in rows
            ],
        )

    async def update_dataset(
        self,
        dataset_id: str,
        payload: DatasetUpdatePayload,
    ) -> DatasetResponse:
        row = await self._require_dataset(dataset_id)
        if payload.description is not None:
            row.description = payload.description.strip()
        if payload.category_path is not None:
            row.category_path_json = list(payload.category_path)
        if payload.exposed_to_agent is not None:
            row.exposed_to_agent = payload.exposed_to_agent
        row.updated_at = datetime.now()
        try:
            await self._db.commit()
        except IntegrityError as error:
            await self._db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Dataset update conflicts with existing data",
            ) from error
        await self._db.refresh(row)
        return _dataset_response(row)

    async def delete_dataset(self, dataset_id: str) -> None:
        row = await self._require_dataset(dataset_id)
        view_name = row.name
        self._view_store.drop_view(view_name)
        await self._db.delete(row)
        await self._db.commit()

    async def _ensure_dataset_is_available(self, dataset_id: str, name: str) -> None:
        if await self._db.get(DatasetRow, dataset_id) is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Dataset id already exists",
            )
        result = await self._db.execute(select(DatasetRow).where(DatasetRow.name == name))
        if result.scalar_one_or_none() is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="DuckDB view name already exists",
            )

    async def _require_dataset(self, dataset_id: str) -> DatasetRow:
        row = await self._db.get(DatasetRow, dataset_id)
        if row is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dataset not found",
            )
        return row


def _dataset_response(row: DatasetRow) -> DatasetResponse:
    category_path = _dataset_category_path(row)
    return DatasetResponse(
        id=row.id,
        name=row.name,
        name_zh=row.description,
        name_en=row.name,
        description=row.description,
        category_path=category_path,
        category_path_en=_category_path_en(category_path, row.name),
        exposed_to_agent=row.exposed_to_agent,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def _dataset_id_from_payload(payload: DatasetPayload) -> str:
    return payload.id.strip() if payload.id else _new_id("ds")


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:16]}"


def _dataset_detail_response(row: DatasetRow, create_sql: str) -> DatasetDetailResponse:
    base = _dataset_response(row)
    return DatasetDetailResponse(**base.model_dump(), create_sql=create_sql)


def _category_path(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if str(item).strip()]


def _dataset_category_path(row: DatasetRow) -> list[str]:
    return _category_path(row.category_path_json)


def _category_path_en(category_path: list[str], name: str) -> list[str]:
    if len(category_path) != 4:
        return []
    try:
        prefix = [
            MARKET_ENGLISH[DatasetMarket(category_path[0])],
            ASSET_CLASS_ENGLISH[DatasetAssetClass(category_path[1])],
            FREQUENCY_ENGLISH[DatasetFrequency(category_path[2])],
        ]
    except ValueError:
        return []
    topic = _topic_en_from_name(name, prefix)
    return [*prefix, topic] if topic else []


def _topic_en_from_name(name: str, prefix: list[str]) -> str:
    prefix_text = "_".join(prefix) + "_"
    if name.startswith(prefix_text):
        return name[len(prefix_text):]
    return ""


def _dataset_value_type(raw_type: str) -> str:
    normalized = raw_type.upper()
    if "BOOL" in normalized:
        return "boolean"
    if any(token in normalized for token in ("INT", "HUGEINT", "UBIGINT")):
        return "integer"
    if any(token in normalized for token in ("DOUBLE", "FLOAT", "REAL", "DECIMAL", "NUMERIC")):
        return "number"
    if "DATE" in normalized or "TIME" in normalized:
        return "date"
    return "string"


def _json_value(value: object) -> object:
    if value is None or isinstance(value, str | int | float | bool):
        return value
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, date | datetime):
        return value.isoformat()
    if isinstance(value, list):
        return [_json_value(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _json_value(item) for key, item in value.items()}
    return str(value)
