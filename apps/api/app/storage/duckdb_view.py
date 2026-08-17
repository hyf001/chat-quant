from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import duckdb
import pandas as pd

_RELATION_NAME_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


class DuckDBViewStoreError(RuntimeError):
    pass


class DuckDBViewAlreadyExistsError(DuckDBViewStoreError):
    pass


class DuckDBViewNotFoundError(DuckDBViewStoreError):
    pass


class DuckDBViewStore:
    def __init__(self, database_path: Path | str) -> None:
        self._database_path = Path(database_path)

    def create_view(self, name: str, create_sql: str) -> None:
        _validate_relation_name(name)
        if self.view_exists(name):
            raise DuckDBViewAlreadyExistsError(f"DuckDB view already exists: {name}")
        _validate_create_view_sql(name, create_sql)
        connection = self._connect()
        try:
            connection.execute(create_sql)
            if not self._view_exists(connection, name):
                raise DuckDBViewStoreError(
                    f"CREATE VIEW statement did not create expected view: {name}"
                )
        except DuckDBViewStoreError:
            raise
        except duckdb.Error as error:
            raise DuckDBViewStoreError(str(error)) from error
        finally:
            connection.close()

    def get_create_sql(self, name: str) -> str:
        _validate_relation_name(name)
        connection = self._connect()
        try:
            row = connection.execute(
                """
                SELECT sql
                FROM duckdb_views()
                WHERE database_name = current_database()
                  AND schema_name = 'main'
                  AND view_name = ?
                  AND internal = false
                """,
                [name],
            ).fetchone()
        except duckdb.Error as error:
            raise DuckDBViewStoreError(str(error)) from error
        finally:
            connection.close()
        if row is None:
            raise DuckDBViewNotFoundError(f"DuckDB view not found: {name}")
        return str(row[0])

    def query(
        self,
        sql: str,
        *,
        page: int,
        page_size: int,
    ) -> tuple[list[tuple[str, str]], list[dict[str, Any]], int]:
        query_sql = _normalize_select_sql(sql)
        offset = (page - 1) * page_size
        connection = self._connect()
        try:
            total = int(
                connection.execute(
                    f"SELECT COUNT(*) FROM ({query_sql}) AS __dataset_query_count"
                ).fetchone()[0]
            )
            result = connection.execute(
                f"SELECT * FROM ({query_sql}) AS __dataset_query LIMIT ? OFFSET ?",
                [page_size, offset],
            )
            columns = [(str(column[0]), str(column[1])) for column in result.description]
            rows = [
                {columns[index][0]: value for index, value in enumerate(row)}
                for row in result.fetchall()
            ]
        except duckdb.Error as error:
            raise DuckDBViewStoreError(str(error)) from error
        finally:
            connection.close()
        return columns, rows, total

    def query_frame(self, sql: str) -> pd.DataFrame:
        query_sql = _normalize_select_sql(sql)
        connection = self._connect()
        try:
            return connection.execute(query_sql).df()
        except duckdb.Error as error:
            raise DuckDBViewStoreError(str(error)) from error
        finally:
            connection.close()

    def drop_view(self, name: str) -> None:
        _validate_relation_name(name)
        connection = self._connect()
        try:
            connection.execute(f"DROP VIEW IF EXISTS {_quote_identifier(name)}")
        except duckdb.Error as error:
            raise DuckDBViewStoreError(str(error)) from error
        finally:
            connection.close()

    def view_exists(self, name: str) -> bool:
        _validate_relation_name(name)
        connection = self._connect()
        try:
            return self._view_exists(connection, name)
        except duckdb.Error as error:
            raise DuckDBViewStoreError(str(error)) from error
        finally:
            connection.close()

    def _connect(self) -> duckdb.DuckDBPyConnection:
        self._database_path.parent.mkdir(parents=True, exist_ok=True)
        return duckdb.connect(str(self._database_path))

    def _view_exists(self, connection: duckdb.DuckDBPyConnection, name: str) -> bool:
        row = connection.execute(
            """
            SELECT 1
            FROM duckdb_views()
            WHERE database_name = current_database()
              AND schema_name = 'main'
              AND view_name = ?
              AND internal = false
            LIMIT 1
            """,
            [name],
        ).fetchone()
        return row is not None


def duckdb_dataset_path(sqlite_database_path: Path | str) -> Path:
    return Path(sqlite_database_path).with_name("datasets.duckdb")


def _validate_create_view_sql(name: str, create_sql: str) -> None:
    stripped = create_sql.strip()
    if not stripped:
        raise DuckDBViewStoreError("CREATE VIEW SQL must not be empty")
    try:
        statements = duckdb.extract_statements(stripped)
    except duckdb.Error as error:
        raise DuckDBViewStoreError(str(error)) from error
    if len(statements) != 1 or statements[0].type != duckdb.StatementType.CREATE:
        raise DuckDBViewStoreError("create_sql must contain exactly one CREATE VIEW statement")
    match = re.match(
        r'^\s*CREATE\s+VIEW\s+(?:(?:main\.)?(?:"(?P<quoted>(?:[^"]|"")*)"|(?P<bare>[A-Za-z_][A-Za-z0-9_]*)))\s+AS\s+',
        stripped,
        re.IGNORECASE | re.DOTALL,
    )
    if match is None:
        raise DuckDBViewStoreError(
            "create_sql must start with CREATE VIEW <dataset name> AS"
        )
    target_name = (match.group("quoted") or match.group("bare") or "").replace('""', '"')
    if target_name != name:
        raise DuckDBViewStoreError(
            f"CREATE VIEW target '{target_name}' does not match dataset name '{name}'"
        )


def _normalize_select_sql(sql: str) -> str:
    stripped = sql.strip()
    if not stripped:
        raise DuckDBViewStoreError("SQL must not be empty")
    try:
        statements = duckdb.extract_statements(stripped)
    except duckdb.Error as error:
        raise DuckDBViewStoreError(str(error)) from error
    if len(statements) != 1 or statements[0].type != duckdb.StatementType.SELECT:
        raise DuckDBViewStoreError("SQL query must contain exactly one SELECT statement")
    return stripped[:-1].strip() if stripped.endswith(";") else stripped


def _validate_relation_name(name: str) -> None:
    if not _RELATION_NAME_PATTERN.match(name):
        raise DuckDBViewStoreError(f"invalid DuckDB view name: {name}")


def _quote_identifier(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'
