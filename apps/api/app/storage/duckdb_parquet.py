from __future__ import annotations

import os
import re
import uuid
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import duckdb
import pandas as pd

ParquetCompression = Literal["zstd", "snappy", "gzip", "brotli", "uncompressed"]
ExistingDataPolicy = Literal["error", "overwrite"]
_RELATION_NAME_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


@dataclass(frozen=True)
class ParquetWriteOptions:
    compression: ParquetCompression = "zstd"
    order_by: Sequence[str] | None = None
    existing_data: ExistingDataPolicy = "overwrite"


class DuckDBParquetStore:
    """Standard DuckDB-backed Parquet reader and writer.

    This class is intentionally business-agnostic:
    - it does not know about MindGo datasets;
    - it does not manage sync status or metadata tables;
    - it does not create a persistent DuckDB database file;
    - all Parquet reads and writes should flow through this adapter.
    """

    def __init__(self, *, temporary_directory: Path | str | None = None) -> None:
        self.temporary_directory = Path(temporary_directory) if temporary_directory else None

    def query(
        self,
        sql: str,
        *,
        params: Mapping[str, object] | None = None,
        frames: Mapping[str, pd.DataFrame] | None = None,
    ) -> pd.DataFrame:
        """Execute SQL through an in-memory DuckDB connection and return a DataFrame."""
        connection = self._connect()
        try:
            self._register_frames(connection, frames)
            return connection.execute(sql, params or {}).df()
        finally:
            connection.close()

    def write(
        self,
        frame: pd.DataFrame,
        path: Path | str,
        *,
        options: ParquetWriteOptions | None = None,
    ) -> int:
        """Write a DataFrame to one Parquet file through DuckDB and return row count.

        Implementations should write to a temporary file first and replace the target
        only after the DuckDB COPY succeeds.
        """
        options = options or ParquetWriteOptions()
        target_path = Path(path)
        if target_path.exists() and options.existing_data == "error":
            raise FileExistsError(target_path)
        _validate_column_names(options.order_by)
        _validate_frame_columns("order_by", options.order_by, frame.columns)

        query = self._frame_select_sql("__input_frame", order_by=options.order_by)
        self._write_query_to_parquet(
            query,
            target_path,
            frames={"__input_frame": frame},
            compression=options.compression,
        )
        return len(frame)

    def _connect(self) -> duckdb.DuckDBPyConnection:
        connection = duckdb.connect(":memory:")
        if self.temporary_directory is not None:
            self.temporary_directory.mkdir(parents=True, exist_ok=True)
            connection.execute(
                f"SET temp_directory = {_sql_string_literal(self.temporary_directory)}"
            )
        return connection

    def _write_query_to_parquet(
        self,
        query: str,
        path: Path,
        *,
        frames: Mapping[str, pd.DataFrame] | None,
        compression: ParquetCompression,
    ) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
        compression_sql = compression.upper()
        copy_sql = (
            f"COPY ({query}) TO {_sql_string_literal(temporary_path)} "
            f"(FORMAT PARQUET, COMPRESSION {compression_sql})"
        )

        connection = self._connect()
        try:
            self._register_frames(connection, frames)
            connection.execute(copy_sql)
            os.replace(temporary_path, path)
        finally:
            if temporary_path.exists():
                temporary_path.unlink()
            connection.close()

    def _register_frames(
        self,
        connection: duckdb.DuckDBPyConnection,
        frames: Mapping[str, pd.DataFrame] | None,
    ) -> None:
        for name, frame in (frames or {}).items():
            _validate_relation_name(name)
            connection.register(name, frame)

    def _frame_select_sql(
        self,
        relation_name: str,
        *,
        order_by: Sequence[str] | None,
    ) -> str:
        return f"SELECT * FROM {_quote_identifier(relation_name)} {_order_by_sql(order_by)}"


def _order_by_sql(columns: Sequence[str] | None) -> str:
    if not columns:
        return ""
    return "ORDER BY " + ", ".join(_quote_identifier(column) for column in columns)


def _sql_string_literal(value: Path | str) -> str:
    return "'" + str(value).replace("'", "''") + "'"


def _quote_identifier(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def _validate_column_names(columns: Sequence[str] | None) -> None:
    for column in columns or ():
        if not column:
            raise ValueError("column name must not be empty")
        if not isinstance(column, str):
            raise TypeError("column name must be a string")


def _validate_relation_name(name: str) -> None:
    if not _RELATION_NAME_PATTERN.match(name):
        raise ValueError(f"invalid DuckDB relation name: {name}")


def _validate_frame_columns(
    label: str,
    columns: Sequence[str] | None,
    available_columns: Sequence[str],
) -> None:
    available = set(available_columns)
    missing = [column for column in columns or () if column not in available]
    if missing:
        raise ValueError(f"{label} columns not found in frame: {', '.join(missing)}")
