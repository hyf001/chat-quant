from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from datetime import timedelta
from typing import Any
from uuid import uuid4

import pandas as pd
from sqlalchemy import create_engine, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.schema import ensure_database_schema
from app.db.session import sync_database_url
from app.model.stock_pool import StockPoolRow, StockPoolStockRow
from app.schema.stock_pool import local_now, normalize_symbol, normalize_tags, split_symbols
from app.service.datasource.mindgo.stock_a_snapshot_info.constants import (
    STOCK_A_SNAPSHOT_INFO_SOURCE_ID,
)
from app.storage import DuckDBViewStore, DuckDBViewStoreError, duckdb_dataset_path


class StockPoolPythonApiError(RuntimeError):
    def __init__(
        self,
        error_code: str,
        message: str,
        *,
        detail: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.error_code = error_code
        self.message = message
        self.detail = detail or {}

    def __str__(self) -> str:
        if not self.detail:
            return f"{self.error_code}: {self.message}"
        return f"{self.error_code}: {self.message} ({self.detail})"


def list_stock_pools(*, project_id: str | None = None) -> pd.DataFrame:
    """Return stock pools available to Python code."""

    statement = select(StockPoolRow).order_by(StockPoolRow.updated_at.desc(), StockPoolRow.id)
    if project_id:
        statement = statement.where(StockPoolRow.project_id == project_id)
    with _session() as session:
        rows = list(session.scalars(statement))
        counts = _stock_counts(session, [row.id for row in rows])
        records = [_pool_record(row, stock_count=counts.get(row.id, 0)) for row in rows]
    return pd.DataFrame(
        records,
        columns=[
            "id",
            "project_id",
            "name",
            "description",
            "stock_count",
            "created_at",
            "updated_at",
        ],
    )


def get_stock_pool(
    pool: str,
    *,
    project_id: str | None = None,
    limit: int | None = None,
) -> dict[str, Any]:
    """Return one stock pool with its stocks and symbol list."""

    with _session() as session:
        row = _require_pool(session, pool, project_id=project_id)
        stocks = _stock_records(session, row.id, limit=limit)
        return {
            **_pool_record(row, stock_count=_stock_count(session, row.id)),
            "symbols": [stock["symbol"] for stock in stocks],
            "stocks": stocks,
        }


def list_pool_stocks(
    pool: str,
    *,
    project_id: str | None = None,
    limit: int | None = None,
) -> pd.DataFrame:
    """Return stocks from one stock pool."""

    with _session() as session:
        row = _require_pool(session, pool, project_id=project_id)
        stocks = _stock_records(session, row.id, limit=limit)
    return pd.DataFrame(
        stocks,
        columns=[
            "id",
            "pool_id",
            "symbol",
            "name",
            "tags",
            "note",
            "created_at",
            "updated_at",
        ],
    )


def stock_pool_symbols(
    pool: str,
    *,
    project_id: str | None = None,
    limit: int | None = None,
) -> list[str]:
    """Return the symbol list for one stock pool."""

    return list(get_stock_pool(pool, project_id=project_id, limit=limit)["symbols"])


def stock_pool_tags(
    pool: str,
    symbol: str,
    *,
    project_id: str | None = None,
) -> list[str]:
    """Return tags assigned to one symbol inside a stock pool."""

    target = symbol.strip().upper()
    for stock in get_stock_pool(pool, project_id=project_id)["stocks"]:
        if stock["symbol"] == target:
            return list(stock["tags"])
    raise StockPoolPythonApiError(
        "STOCK_POOL_SYMBOL_NOT_FOUND",
        "Symbol was not found in stock pool",
        detail={"pool": pool, "symbol": target},
    )


def stock_pool_symbols_by_tag(
    pool: str,
    tag: str,
    *,
    project_id: str | None = None,
    limit: int | None = None,
) -> list[str]:
    """Return symbols carrying a tag in one stock pool."""

    target = tag.strip()
    if not target:
        raise StockPoolPythonApiError("STOCK_POOL_TAG_EMPTY", "tag must not be empty")
    symbols = [
        stock["symbol"]
        for stock in get_stock_pool(pool, project_id=project_id)["stocks"]
        if target in stock["tags"]
    ]
    if limit is None:
        return symbols
    return symbols[:_validate_limit(limit)]


def add_pool_stocks(
    pool: str,
    symbols: str | list[str],
    *,
    project_id: str | None = None,
    tags: list[str] | None = None,
    note: str | None = None,
) -> dict[str, Any]:
    """Add symbols to a stock pool and fill stock names from a_stock_snapshot_info."""

    normalized_symbols = _normalize_symbols(symbols)
    if not normalized_symbols:
        raise StockPoolPythonApiError("STOCK_POOL_SYMBOLS_EMPTY", "No valid symbols found")
    normalized_tags = normalize_tags(tags or [])
    normalized_note = _blank_to_none(note)
    snapshot_names = _snapshot_info_names(normalized_symbols)
    now = local_now()

    with _session() as session:
        pool_row = _require_pool(session, pool, project_id=project_id)
        existing = set(
            session.scalars(
                select(StockPoolStockRow.symbol).where(
                    StockPoolStockRow.pool_id == pool_row.id,
                    StockPoolStockRow.symbol.in_(normalized_symbols),
                )
            )
        )
        rows: list[StockPoolStockRow] = []
        for index, symbol in enumerate(normalized_symbols):
            if symbol in existing or symbol not in snapshot_names:
                continue
            timestamp = now + timedelta(microseconds=index)
            rows.append(
                StockPoolStockRow(
                    id=_new_id("sps"),
                    pool_id=pool_row.id,
                    symbol=symbol,
                    name=snapshot_names.get(symbol),
                    tags_json=list(normalized_tags),
                    note=normalized_note,
                    created_at=timestamp,
                    updated_at=timestamp,
                )
            )
        session.add_all(rows)
        pool_row.updated_at = local_now()
        try:
            session.commit()
        except IntegrityError as exc:
            session.rollback()
            raise StockPoolPythonApiError(
                "STOCK_POOL_STOCK_CONFLICT",
                "One or more stocks already exist in this pool",
                detail={"pool": pool, "symbols": normalized_symbols},
            ) from exc
        for row in rows:
            session.refresh(row)
        return {
            "items": [_stock_record(row) for row in rows],
            "created": len(rows),
            "skipped": len(normalized_symbols) - len(rows),
            "missing_from_dataset": [
                symbol for symbol in normalized_symbols if symbol not in snapshot_names
            ],
            "source_dataset": STOCK_A_SNAPSHOT_INFO_SOURCE_ID,
        }


@contextmanager
def _session() -> Iterator[Session]:
    settings = get_settings()
    ensure_database_schema(settings)
    engine = create_engine(sync_database_url(settings))
    try:
        with Session(engine) as session:
            yield session
    finally:
        engine.dispose()


def _require_pool(
    session: Session,
    pool: str,
    *,
    project_id: str | None,
) -> StockPoolRow:
    key = pool.strip()
    if not key:
        raise StockPoolPythonApiError("STOCK_POOL_EMPTY", "pool must not be empty")
    row = session.get(StockPoolRow, key)
    if row is not None:
        return row
    statement = select(StockPoolRow).where(StockPoolRow.name == key)
    if project_id:
        statement = statement.where(StockPoolRow.project_id == project_id)
    rows = list(session.scalars(statement))
    if not rows:
        raise StockPoolPythonApiError(
            "STOCK_POOL_NOT_FOUND",
            "Stock pool was not found",
            detail={"pool": pool, "project_id": project_id},
        )
    if len(rows) > 1:
        raise StockPoolPythonApiError(
            "STOCK_POOL_AMBIGUOUS",
            "Stock pool name exists in multiple projects; pass project_id",
            detail={"pool": pool, "project_ids": [row.project_id for row in rows]},
        )
    return rows[0]


def _stock_counts(session: Session, pool_ids: list[str]) -> dict[str, int]:
    if not pool_ids:
        return {}
    rows = session.execute(
        select(StockPoolStockRow.pool_id, StockPoolStockRow.id).where(
            StockPoolStockRow.pool_id.in_(pool_ids)
        )
    )
    counts: dict[str, int] = {}
    for pool_id, _ in rows:
        counts[str(pool_id)] = counts.get(str(pool_id), 0) + 1
    return counts


def _stock_count(session: Session, pool_id: str) -> int:
    return int(
        session.scalar(
            select(func.count(StockPoolStockRow.id)).where(StockPoolStockRow.pool_id == pool_id)
        )
        or 0
    )


def _stock_records(
    session: Session,
    pool_id: str,
    *,
    limit: int | None = None,
) -> list[dict[str, Any]]:
    statement = (
        select(StockPoolStockRow)
        .where(StockPoolStockRow.pool_id == pool_id)
        .order_by(StockPoolStockRow.created_at.asc(), StockPoolStockRow.id)
    )
    if limit is not None:
        statement = statement.limit(_validate_limit(limit))
    rows = session.scalars(statement)
    return [_stock_record(row) for row in rows]


def _pool_record(row: StockPoolRow, *, stock_count: int) -> dict[str, Any]:
    return {
        "id": row.id,
        "project_id": row.project_id,
        "name": row.name,
        "description": row.description,
        "stock_count": stock_count,
        "created_at": row.created_at,
        "updated_at": row.updated_at,
    }


def _stock_record(row: StockPoolStockRow) -> dict[str, Any]:
    return {
        "id": row.id,
        "pool_id": row.pool_id,
        "symbol": row.symbol,
        "name": row.name,
        "tags": normalize_tags(list(row.tags_json) if isinstance(row.tags_json, list) else []),
        "note": row.note,
        "created_at": row.created_at,
        "updated_at": row.updated_at,
    }


def _blank_to_none(value: object) -> str | None:
    if value is None or pd.isna(value):
        return None
    stripped = str(value).strip()
    return stripped or None


def _normalize_symbols(symbols: str | list[str]) -> list[str]:
    if isinstance(symbols, str):
        return split_symbols(symbols)
    normalized: list[str] = []
    for symbol in symbols:
        value = normalize_symbol(str(symbol))
        if value and value not in normalized:
            normalized.append(value)
    return normalized


def _validate_limit(limit: int) -> int:
    if limit < 1:
        raise StockPoolPythonApiError("STOCK_POOL_LIMIT_INVALID", "limit must be greater than 0")
    return limit


def _snapshot_info_names(symbols: list[str]) -> dict[str, str | None]:
    values = ", ".join(_sql_string_literal(symbol) for symbol in symbols)
    sql = f"""
        SELECT symbol, name
        FROM a_stock_snapshot_info
        WHERE upper(CAST(symbol AS VARCHAR)) IN ({values})
    """
    try:
        frame = DuckDBViewStore(
            duckdb_dataset_path(get_settings().database_path)
        ).query_frame(sql)
    except DuckDBViewStoreError as exc:
        raise StockPoolPythonApiError(
            "STOCK_POOL_SNAPSHOT_INFO_UNAVAILABLE",
            "a_stock_snapshot_info dataset is unavailable",
            detail={"dataset": STOCK_A_SNAPSHOT_INFO_SOURCE_ID, "error": str(exc)},
        ) from exc
    names: dict[str, str | None] = {}
    for record in frame.to_dict(orient="records"):
        symbol = normalize_symbol(str(record.get("symbol") or ""))
        if symbol:
            names[symbol] = _blank_to_none(record.get("name"))
    return names


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


def _sql_string_literal(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"
