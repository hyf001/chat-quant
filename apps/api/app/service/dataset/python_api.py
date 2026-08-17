from __future__ import annotations

import re
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

import pandas as pd
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.schema import ensure_database_schema
from app.db.session import sync_database_url
from app.model.dataset import DatasetRow
from app.storage import DuckDBViewStore, DuckDBViewStoreError, duckdb_dataset_path

DEFAULT_PREVIEW_LIMIT = 20
MAX_PREVIEW_LIMIT = 50_000
_DATASET_NAME_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


class DatasetPythonApiError(RuntimeError):
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


def list_datasets(
    *,
    category: str | list[str] | None = None,
) -> pd.DataFrame:
    """Return datasets exposed to the Python execution environment."""

    rows = _dataset_rows(exposed_only=True, category=category)
    return pd.DataFrame(
        [_dataset_record(row) for row in rows],
        columns=[
            "id",
            "name",
            "description",
            "category_path",
            "exposed_to_agent",
            "created_at",
            "updated_at",
        ],
    )


def describe_dataset(dataset: str) -> dict[str, Any]:
    """Return metadata, CREATE VIEW SQL, and columns for one exposed dataset."""

    row = _require_exposed_dataset(dataset)
    view_store = _view_store()
    try:
        create_sql = view_store.get_create_sql(row.name)
        columns, _, _ = view_store.query(
            f"SELECT * FROM {_quote_identifier(row.name)} LIMIT 0",
            page=1,
            page_size=1,
        )
    except DuckDBViewStoreError as exc:
        raise DatasetPythonApiError(
            "DATASET_VIEW_UNAVAILABLE",
            str(exc),
            detail={"dataset": dataset, "view": row.name},
        ) from exc
    return {
        **_dataset_record(row),
        "create_sql": create_sql,
        "columns": [
            {"name": name, "value_type": _dataset_value_type(raw_type), "raw_type": raw_type}
            for name, raw_type in columns
        ],
        "sample_sql": f"SELECT * FROM {_quote_identifier(row.name)} LIMIT {DEFAULT_PREVIEW_LIMIT}",
    }


def preview_dataset(
    dataset: str,
    *,
    limit: int = DEFAULT_PREVIEW_LIMIT,
) -> pd.DataFrame:
    """Return the first rows from one dataset view."""

    row = _require_exposed_dataset(dataset)
    checked_limit = _validate_limit(limit)
    return query_dataset(
        f"SELECT * FROM {_quote_identifier(row.name)} LIMIT {checked_limit}",
    )


def query_dataset(sql: str) -> pd.DataFrame:
    """Run a read-only SELECT query against exposed dataset views."""

    query_sql = _normalize_sql(sql)
    _ensure_query_does_not_reference_hidden_datasets(query_sql)
    view_store = _view_store()
    try:
        return view_store.query_frame(query_sql)
    except DuckDBViewStoreError as exc:
        raise DatasetPythonApiError("DATASET_QUERY_FAILED", str(exc)) from exc


def _dataset_rows(
    *,
    exposed_only: bool,
    category: str | list[str] | None,
) -> list[DatasetRow]:
    statement = select(DatasetRow).order_by(DatasetRow.updated_at.desc(), DatasetRow.id)
    if exposed_only:
        statement = statement.where(DatasetRow.exposed_to_agent.is_(True))
    prefix = _category_prefix(category)
    with _session() as session:
        rows = list(session.scalars(statement))
    if not prefix:
        return rows
    return [
        row
        for row in rows
        if _category_path(row.category_path_json)[: len(prefix)] == prefix
    ]


def _require_exposed_dataset(dataset: str) -> DatasetRow:
    dataset_id = dataset.strip()
    if not dataset_id:
        raise DatasetPythonApiError("DATASET_ID_EMPTY", "dataset must not be empty")
    with _session() as session:
        row = session.get(DatasetRow, dataset_id)
        if row is None:
            row = session.scalars(
                select(DatasetRow).where(DatasetRow.name == dataset_id)
            ).one_or_none()
        if row is None:
            raise DatasetPythonApiError(
                "DATASET_NOT_FOUND",
                "Dataset was not found",
                detail={"dataset": dataset},
            )
        if not row.exposed_to_agent:
            raise DatasetPythonApiError(
                "DATASET_NOT_EXPOSED",
                "Dataset is not exposed to the Python execution environment",
                detail={"dataset": dataset, "id": row.id, "name": row.name},
            )
        session.expunge(row)
        return row


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


def _view_store() -> DuckDBViewStore:
    return DuckDBViewStore(duckdb_dataset_path(get_settings().database_path))


def _dataset_record(row: DatasetRow) -> dict[str, Any]:
    return {
        "id": row.id,
        "name": row.name,
        "description": row.description,
        "category_path": _category_path(row.category_path_json),
        "exposed_to_agent": row.exposed_to_agent,
        "created_at": row.created_at,
        "updated_at": row.updated_at,
    }


def _category_path(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if str(item).strip()]


def _category_prefix(category: str | list[str] | None) -> list[str]:
    if category is None:
        return []
    if isinstance(category, str):
        return [part.strip() for part in category.split("/") if part.strip()]
    return [str(part).strip() for part in category if str(part).strip()]


def _normalize_sql(sql: str) -> str:
    stripped = sql.strip()
    if not stripped:
        raise DatasetPythonApiError("DATASET_SQL_EMPTY", "SQL must not be empty")
    return stripped


def _validate_limit(limit: int) -> int:
    if not isinstance(limit, int):
        raise DatasetPythonApiError(
            "DATASET_LIMIT_INVALID",
            "limit must be an integer",
            detail={"limit": limit},
        )
    if limit < 1 or limit > MAX_PREVIEW_LIMIT:
        raise DatasetPythonApiError(
            "DATASET_LIMIT_INVALID",
            f"limit must be between 1 and {MAX_PREVIEW_LIMIT}",
            detail={"limit": limit},
        )
    return limit


def _ensure_query_does_not_reference_hidden_datasets(sql: str) -> None:
    hidden_names = {
        row.name
        for row in _dataset_rows(exposed_only=False, category=None)
        if not row.exposed_to_agent
    }
    referenced = [
        name
        for name in hidden_names
        if _query_references_relation(sql, name)
    ]
    if referenced:
        raise DatasetPythonApiError(
            "DATASET_NOT_EXPOSED",
            "SQL references datasets that are not exposed to the Python execution environment",
            detail={"datasets": sorted(referenced)},
        )


def _query_references_relation(sql: str, relation_name: str) -> bool:
    bare = re.escape(relation_name)
    quoted = re.escape('"' + relation_name.replace('"', '""') + '"')
    return bool(
        re.search(rf'(?<![A-Za-z0-9_"]){bare}(?![A-Za-z0-9_"])', sql)
        or re.search(rf"(?<![A-Za-z0-9_]){quoted}(?![A-Za-z0-9_])", sql)
    )


def _quote_identifier(identifier: str) -> str:
    if not _DATASET_NAME_PATTERN.match(identifier):
        raise DatasetPythonApiError(
            "DATASET_NAME_INVALID",
            "dataset view name is not a valid identifier",
            detail={"name": identifier},
        )
    return '"' + identifier.replace('"', '""') + '"'


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
    if isinstance(value, Path):
        return value.as_posix()
    if isinstance(value, list):
        return [_json_value(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _json_value(item) for key, item in value.items()}
    return str(value)
