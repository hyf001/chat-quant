from __future__ import annotations

from uuid import uuid4

import pandas as pd
from sqlalchemy import delete, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.model.stock_pool import StockPoolRow, StockPoolStockRow
from app.schema.stock_pool import (
    StockPoolBulkCreateResult,
    StockPoolCandidate,
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
    local_now,
    normalize_symbol,
    normalize_tags,
    split_symbols,
)
from app.service import project as project_service
from app.service.datasource.mindgo.stock_a_snapshot_info.constants import (
    STOCK_A_SNAPSHOT_INFO_SOURCE_ID,
)
from app.service.project import ProjectNotFoundError
from app.storage import DuckDBViewStore, DuckDBViewStoreError, duckdb_dataset_path


class StockPoolError(Exception):
    def __init__(
        self,
        error_code: str,
        message: str,
        status_code: int = 400,
        *,
        detail: dict[str, object] | None = None,
    ) -> None:
        super().__init__(message)
        self.error_code = error_code
        self.message = message
        self.status_code = status_code
        self.detail = detail or {}


class StockPoolService:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def list_stock_pools(self, project_id: str) -> StockPoolListResponse:
        await self._require_project(project_id)
        rows = (
            await self._db.scalars(
                select(StockPoolRow)
                .where(StockPoolRow.project_id == project_id)
                .order_by(StockPoolRow.updated_at.desc(), StockPoolRow.id)
            )
        ).all()
        counts = await self._stock_counts([row.id for row in rows])
        return StockPoolListResponse(
            items=[_pool_from_row(row, stock_count=counts.get(row.id, 0)) for row in rows],
            total=len(rows),
        )

    async def create_stock_pool(self, payload: StockPoolCreate) -> StockPoolRecord:
        await self._require_project(payload.project_id)
        row = StockPoolRow(
            id=_new_id("sp"),
            project_id=payload.project_id,
            name=payload.name.strip(),
            description=_blank_to_none(payload.description),
            created_at=local_now(),
            updated_at=local_now(),
        )
        self._db.add(row)
        try:
            await self._db.commit()
        except IntegrityError as exc:
            await self._db.rollback()
            raise StockPoolError(
                "STOCK_POOL_NAME_CONFLICT",
                "Stock pool name already exists in this project",
                409,
            ) from exc
        await self._db.refresh(row)
        return _pool_from_row(row)

    async def get_stock_pool(self, pool_id: str, *, include_stocks: bool = True) -> StockPoolDetail:
        pool = await self._require_pool(pool_id)
        if not include_stocks:
            return _pool_detail_from_row(
                pool,
                [],
                stock_count=await self._stock_count(pool_id),
            )
        stocks = await self._stock_records(pool_id)
        return _pool_detail_from_row(pool, stocks, stock_count=len(stocks))

    async def update_stock_pool(
        self,
        pool_id: str,
        payload: StockPoolUpdate,
    ) -> StockPoolRecord:
        row = await self._require_pool(pool_id)
        fields = payload.model_fields_set
        if "name" in fields and payload.name is not None:
            row.name = payload.name.strip()
        if "description" in fields:
            row.description = _blank_to_none(payload.description)
        row.updated_at = local_now()
        try:
            await self._db.commit()
        except IntegrityError as exc:
            await self._db.rollback()
            raise StockPoolError(
                "STOCK_POOL_NAME_CONFLICT",
                "Stock pool name already exists in this project",
                409,
            ) from exc
        await self._db.refresh(row)
        return _pool_from_row(row, stock_count=await self._stock_count(row.id))

    async def delete_stock_pool(self, pool_id: str) -> None:
        row = await self._require_pool(pool_id)
        await self._db.execute(delete(StockPoolStockRow).where(StockPoolStockRow.pool_id == row.id))
        await self._db.delete(row)
        await self._db.commit()

    async def list_pool_stocks(
        self,
        pool_id: str,
        *,
        query: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> StockPoolStockListResponse:
        await self._require_pool(pool_id)
        keyword = (query or "").strip().lower()
        if keyword:
            rows = (
                await self._db.scalars(
                    select(StockPoolStockRow)
                    .where(StockPoolStockRow.pool_id == pool_id)
                    .order_by(StockPoolStockRow.created_at.asc(), StockPoolStockRow.id)
                )
            ).all()
            matched = [_stock_from_row(row) for row in rows if _stock_matches(row, keyword)]
            checked_limit = max(1, min(limit, 500))
            checked_offset = max(0, offset)
            return StockPoolStockListResponse(
                items=matched[checked_offset : checked_offset + checked_limit],
                total=len(matched),
            )
        total = int(
            await self._db.scalar(
                select(func.count(StockPoolStockRow.id)).where(
                    StockPoolStockRow.pool_id == pool_id
                )
            )
            or 0
        )
        result = await self._db.scalars(
            select(StockPoolStockRow)
            .where(StockPoolStockRow.pool_id == pool_id)
            .order_by(StockPoolStockRow.created_at.asc(), StockPoolStockRow.id)
            .limit(max(1, min(limit, 500)))
            .offset(max(0, offset))
        )
        stocks = [_stock_from_row(row) for row in result.all()]
        return StockPoolStockListResponse(items=stocks, total=total)

    async def add_pool_stock(
        self,
        pool_id: str,
        payload: StockPoolStockCreate,
    ) -> StockPoolStockRecord:
        await self._require_pool(pool_id)
        row = StockPoolStockRow(
            id=_new_id("sps"),
            pool_id=pool_id,
            symbol=payload.symbol,
            name=payload.name,
            tags_json=list(payload.tags),
            note=payload.note,
            created_at=local_now(),
            updated_at=local_now(),
        )
        self._db.add(row)
        try:
            await self._db.commit()
        except IntegrityError as exc:
            await self._db.rollback()
            raise StockPoolError(
                "STOCK_POOL_STOCK_CONFLICT",
                "Stock already exists in this pool",
                409,
                detail={"pool_id": pool_id, "symbol": payload.symbol},
            ) from exc
        await self._touch_pool(pool_id)
        await self._db.refresh(row)
        return _stock_from_row(row)

    async def bulk_add_pool_stocks(
        self,
        pool_id: str,
        payload: StockPoolStocksBulkCreate,
    ) -> StockPoolBulkCreateResult:
        await self._require_pool(pool_id)
        symbols = split_symbols(payload.symbols)
        if not symbols:
            raise StockPoolError("STOCK_POOL_SYMBOLS_EMPTY", "No valid symbols found", 422)
        existing = set(await self._symbols(pool_id))
        rows = [
            StockPoolStockRow(
                id=_new_id("sps"),
                pool_id=pool_id,
                symbol=symbol,
                name=None,
                tags_json=[],
                note=None,
                created_at=local_now(),
                updated_at=local_now(),
            )
            for symbol in symbols
            if symbol not in existing
        ]
        self._db.add_all(rows)
        try:
            await self._db.commit()
        except IntegrityError as exc:
            await self._db.rollback()
            raise StockPoolError(
                "STOCK_POOL_STOCK_CONFLICT",
                "One or more stocks already exist in this pool",
                409,
            ) from exc
        await self._touch_pool(pool_id)
        for row in rows:
            await self._db.refresh(row)
        return StockPoolBulkCreateResult(
            items=[_stock_from_row(row) for row in rows],
            created=len(rows),
            skipped=len(symbols) - len(rows),
        )

    async def search_snapshot_info_candidates(
        self,
        pool_id: str,
        *,
        query: str | None,
        limit: int,
        offset: int,
    ) -> StockPoolCandidateListResponse:
        await self._require_pool(pool_id)
        keyword = (query or "").strip()
        total_frame = _query_snapshot_info(_snapshot_info_count_sql(keyword))
        total = int(total_frame.iloc[0]["total"]) if not total_frame.empty else 0
        frame = _query_snapshot_info(_snapshot_info_search_sql(keyword, limit, offset))
        existing = set(await self._symbols(pool_id))
        candidates = [
            StockPoolCandidate(
                symbol=normalize_symbol(str(row["symbol"])),
                name=_string_or_none(row.get("name")),
                in_pool=normalize_symbol(str(row["symbol"])) in existing,
            )
            for row in frame.to_dict(orient="records")
            if _blank_to_none(str(row.get("symbol") or ""))
        ]
        return StockPoolCandidateListResponse(items=candidates, total=total)

    async def import_snapshot_info_stocks(
        self,
        pool_id: str,
        payload: StockPoolSnapshotImportRequest | None = None,
    ) -> StockPoolSnapshotImportResult:
        await self._require_pool(pool_id)
        requested_symbols = payload.symbols if payload is not None else []
        if payload is not None and not requested_symbols:
            raise StockPoolError("STOCK_POOL_SYMBOLS_EMPTY", "No valid symbols found", 422)
        frame = _query_snapshot_info(
            _snapshot_info_by_symbols_sql(requested_symbols)
            if requested_symbols
            else _snapshot_info_all_sql()
        )
        existing = set(await self._symbols(pool_id))
        rows = []
        seen: set[str] = set()
        for record in frame.to_dict(orient="records"):
            symbol = normalize_symbol(str(record.get("symbol") or ""))
            if not symbol or symbol in existing or symbol in seen:
                continue
            seen.add(symbol)
            rows.append(
                StockPoolStockRow(
                    id=_new_id("sps"),
                    pool_id=pool_id,
                    symbol=symbol,
                    name=_string_or_none(record.get("name")),
                    tags_json=[],
                    note=None,
                    created_at=local_now(),
                    updated_at=local_now(),
                )
            )
        self._db.add_all(rows)
        try:
            await self._db.commit()
        except IntegrityError as exc:
            await self._db.rollback()
            raise StockPoolError(
                "STOCK_POOL_STOCK_CONFLICT",
                "One or more stocks already exist in this pool",
                409,
            ) from exc
        await self._touch_pool(pool_id)
        for row in rows:
            await self._db.refresh(row)
        return StockPoolSnapshotImportResult(
            items=[_stock_from_row(row) for row in rows],
            created=len(rows),
            skipped=max(
                (len(requested_symbols) if requested_symbols else len(frame.index)) - len(rows),
                0,
            ),
        )

    async def update_pool_stock(
        self,
        stock_id: str,
        payload: StockPoolStockUpdate,
    ) -> StockPoolStockRecord:
        row = await self._require_stock(stock_id)
        fields = payload.model_fields_set
        if "symbol" in fields and payload.symbol is not None:
            row.symbol = normalize_symbol(payload.symbol)
        if "name" in fields:
            row.name = _blank_to_none(payload.name)
        if "tags" in fields and payload.tags is not None:
            row.tags_json = normalize_tags(payload.tags)
        if "note" in fields:
            row.note = _blank_to_none(payload.note)
        row.updated_at = local_now()
        try:
            await self._db.commit()
        except IntegrityError as exc:
            await self._db.rollback()
            raise StockPoolError(
                "STOCK_POOL_STOCK_CONFLICT",
                "Stock already exists in this pool",
                409,
                detail={"pool_id": row.pool_id, "symbol": row.symbol},
            ) from exc
        await self._touch_pool(row.pool_id)
        await self._db.refresh(row)
        return _stock_from_row(row)

    async def delete_pool_stock(self, stock_id: str) -> None:
        row = await self._require_stock(stock_id)
        pool_id = row.pool_id
        await self._db.delete(row)
        await self._db.commit()
        await self._touch_pool(pool_id)

    async def _require_project(self, project_id: str) -> None:
        try:
            await project_service.require_project(self._db, project_id)
        except ProjectNotFoundError as exc:
            raise StockPoolError("PROJECT_NOT_FOUND", "Project not found", 404) from exc

    async def _require_pool(self, pool_id: str) -> StockPoolRow:
        row = await self._db.get(StockPoolRow, pool_id)
        if row is None:
            raise StockPoolError("STOCK_POOL_NOT_FOUND", "Stock pool not found", 404)
        return row

    async def _require_stock(self, stock_id: str) -> StockPoolStockRow:
        row = await self._db.get(StockPoolStockRow, stock_id)
        if row is None:
            raise StockPoolError("STOCK_POOL_STOCK_NOT_FOUND", "Stock pool stock not found", 404)
        return row

    async def _stock_records(self, pool_id: str) -> list[StockPoolStockRecord]:
        result = await self._db.scalars(
            select(StockPoolStockRow)
            .where(StockPoolStockRow.pool_id == pool_id)
            .order_by(StockPoolStockRow.created_at.asc(), StockPoolStockRow.id)
        )
        return [_stock_from_row(row) for row in result.all()]

    async def _stock_counts(self, pool_ids: list[str]) -> dict[str, int]:
        if not pool_ids:
            return {}
        result = await self._db.execute(
            select(StockPoolStockRow.pool_id, func.count(StockPoolStockRow.id))
            .where(StockPoolStockRow.pool_id.in_(pool_ids))
            .group_by(StockPoolStockRow.pool_id)
        )
        return {str(pool_id): int(count) for pool_id, count in result.all()}

    async def _stock_count(self, pool_id: str) -> int:
        return int(
            await self._db.scalar(
                select(func.count(StockPoolStockRow.id)).where(
                    StockPoolStockRow.pool_id == pool_id
                )
            )
            or 0
        )

    async def _symbols(self, pool_id: str) -> list[str]:
        result = await self._db.scalars(
            select(StockPoolStockRow.symbol)
            .where(StockPoolStockRow.pool_id == pool_id)
            .order_by(StockPoolStockRow.created_at.asc(), StockPoolStockRow.id)
        )
        return list(result.all())

    async def _touch_pool(self, pool_id: str) -> None:
        pool = await self._require_pool(pool_id)
        pool.updated_at = local_now()
        await self._db.commit()


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


def _pool_from_row(row: StockPoolRow, *, stock_count: int = 0) -> StockPoolRecord:
    return StockPoolRecord(
        id=row.id,
        project_id=row.project_id,
        name=row.name,
        description=row.description,
        stock_count=stock_count,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def _pool_detail_from_row(
    row: StockPoolRow,
    stocks: list[StockPoolStockRecord],
    *,
    stock_count: int,
) -> StockPoolDetail:
    return StockPoolDetail(
        **_pool_from_row(row, stock_count=stock_count).model_dump(),
        stocks=stocks,
        symbols=[stock.symbol for stock in stocks],
    )


def _stock_from_row(row: StockPoolStockRow) -> StockPoolStockRecord:
    return StockPoolStockRecord(
        id=row.id,
        pool_id=row.pool_id,
        symbol=row.symbol,
        name=row.name,
        tags=normalize_tags(list(row.tags_json) if isinstance(row.tags_json, list) else []),
        note=row.note,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def _stock_matches(row: StockPoolStockRow, keyword: str) -> bool:
    tags = normalize_tags(list(row.tags_json) if isinstance(row.tags_json, list) else [])
    values = [row.symbol, row.name, row.note, *tags]
    return any(keyword in str(value).lower() for value in values if value is not None)


def _blank_to_none(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None


def _string_or_none(value: object) -> str | None:
    if value is None or pd.isna(value):
        return None
    return _blank_to_none(str(value))


def _query_snapshot_info(sql: str) -> pd.DataFrame:
    view_store = DuckDBViewStore(duckdb_dataset_path(get_settings().database_path))
    try:
        return view_store.query_frame(sql)
    except DuckDBViewStoreError as exc:
        raise StockPoolError(
            "STOCK_POOL_SNAPSHOT_INFO_UNAVAILABLE",
            "a_stock_snapshot_info dataset is unavailable",
            422,
            detail={"dataset": STOCK_A_SNAPSHOT_INFO_SOURCE_ID, "error": str(exc)},
        ) from exc


def _snapshot_info_all_sql() -> str:
    return """
        SELECT symbol, name
        FROM a_stock_snapshot_info
        WHERE symbol IS NOT NULL AND trim(CAST(symbol AS VARCHAR)) <> ''
        ORDER BY symbol
    """


def _snapshot_info_search_sql(query: str, limit: int, offset: int) -> str:
    checked_limit = max(1, min(limit, 200))
    checked_offset = max(0, offset)
    if not query:
        return f"""
            SELECT symbol, name
            FROM a_stock_snapshot_info
            WHERE symbol IS NOT NULL AND trim(CAST(symbol AS VARCHAR)) <> ''
            ORDER BY symbol
            LIMIT {checked_limit}
            OFFSET {checked_offset}
        """
    pattern = _sql_string_literal(f"%{query.lower()}%")
    return f"""
        SELECT symbol, name
        FROM a_stock_snapshot_info
        WHERE symbol IS NOT NULL
          AND trim(CAST(symbol AS VARCHAR)) <> ''
          AND (
            lower(CAST(symbol AS VARCHAR)) LIKE {pattern}
            OR lower(CAST(name AS VARCHAR)) LIKE {pattern}
          )
        ORDER BY symbol
        LIMIT {checked_limit}
        OFFSET {checked_offset}
    """


def _snapshot_info_count_sql(query: str) -> str:
    if not query:
        return """
            SELECT COUNT(*) AS total
            FROM a_stock_snapshot_info
            WHERE symbol IS NOT NULL AND trim(CAST(symbol AS VARCHAR)) <> ''
        """
    pattern = _sql_string_literal(f"%{query.lower()}%")
    return f"""
        SELECT COUNT(*) AS total
        FROM a_stock_snapshot_info
        WHERE symbol IS NOT NULL
          AND trim(CAST(symbol AS VARCHAR)) <> ''
          AND (
            lower(CAST(symbol AS VARCHAR)) LIKE {pattern}
            OR lower(CAST(name AS VARCHAR)) LIKE {pattern}
          )
    """


def _snapshot_info_by_symbols_sql(symbols: list[str]) -> str:
    if not symbols:
        return _snapshot_info_all_sql()
    values = ", ".join(_sql_string_literal(symbol) for symbol in symbols)
    return f"""
        SELECT symbol, name
        FROM a_stock_snapshot_info
        WHERE upper(CAST(symbol AS VARCHAR)) IN ({values})
        ORDER BY symbol
    """


def _sql_string_literal(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"
