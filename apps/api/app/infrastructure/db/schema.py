from __future__ import annotations

import json
from threading import Lock

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine

from app.core.config import Settings
from app.infrastructure.db import models  # noqa: F401
from app.infrastructure.db.session import Base, sync_database_url

_SCHEMA_LOCK = Lock()
_INITIALIZED_DATABASE_URLS: set[str] = set()


def ensure_database_schema(settings: Settings) -> None:
    database_url = sync_database_url(settings)
    with _SCHEMA_LOCK:
        if database_url in _INITIALIZED_DATABASE_URLS and settings.database_path.exists():
            return
        settings.database_path.parent.mkdir(parents=True, exist_ok=True)
        engine = create_engine(database_url)
        try:
            Base.metadata.create_all(engine)
            _merge_backtest_payloads(engine)
            _drop_retired_strategy_columns(engine)
            _drop_retired_backtest_result_table(engine)
            _drop_retired_artifact_tables(engine)
        finally:
            engine.dispose()
        _INITIALIZED_DATABASE_URLS.add(database_url)


def _drop_retired_strategy_columns(engine: Engine) -> None:
    inspector = inspect(engine)
    table_names = set(inspector.get_table_names())
    if "strategies" not in table_names:
        return

    retired_columns_by_table = {
        "strategies": {"chat_session_id", "source_sdk_message_uuid", "strategy_type"},
        "strategy_versions": {
            "change_summary",
            "logic_summary",
            "parent_version_id",
            "source_sdk_message_uuid",
            "source_sdk_session_id",
            "source_sdk_tool_use_id",
            "status",
            "version_name",
            "code_artifact_id",
        },
        "strategy_backtests": {"chat_session_id", "config_hash", "result_payload_json", "run_type"},
    }
    with engine.begin() as connection:
        connection.execute(text("DROP INDEX IF EXISTS idx_strategies_chat_session"))
        connection.execute(text("DROP INDEX IF EXISTS idx_strategies_type"))
        connection.execute(text("DROP INDEX IF EXISTS idx_strategy_versions_parent"))
        connection.execute(text("DROP INDEX IF EXISTS idx_strategy_versions_status"))
        connection.execute(text("DROP INDEX IF EXISTS idx_strategy_versions_artifact"))
        for table_name, retired_columns in retired_columns_by_table.items():
            if table_name not in table_names:
                continue
            columns = {column["name"] for column in inspector.get_columns(table_name)}
            for column_name in sorted(columns & retired_columns):
                connection.execute(text(f"ALTER TABLE {table_name} DROP COLUMN {column_name}"))


def _merge_backtest_payloads(engine: Engine) -> None:
    inspector = inspect(engine)
    table_names = set(inspector.get_table_names())
    if "strategy_backtests" not in table_names:
        return

    columns = {column["name"] for column in inspector.get_columns("strategy_backtests")}
    if "payload_json" not in columns:
        return

    with engine.begin() as connection:
        if "result_payload_json" in columns:
            rows = connection.execute(
                text("SELECT id, payload_json, result_payload_json FROM strategy_backtests")
            ).mappings()
            for row in rows:
                result_payload = _json_object(row["result_payload_json"])
                if result_payload is not None:
                    _update_backtest_payload(
                        connection,
                        str(row["id"]),
                        row["payload_json"],
                        result_payload,
                    )

        if "strategy_backtest_results" in table_names:
            rows = connection.execute(
                text(
                    "SELECT strategy_backtest_id, payload_json "
                    "FROM strategy_backtest_results"
                )
            ).mappings()
            for row in rows:
                result_payload = _json_object(row["payload_json"])
                if result_payload is not None:
                    backtest_payload = connection.execute(
                        text(
                            "SELECT payload_json FROM strategy_backtests "
                            "WHERE id = :backtest_id"
                        ),
                        {"backtest_id": row["strategy_backtest_id"]},
                    ).scalar_one_or_none()
                    if backtest_payload is not None:
                        _update_backtest_payload(
                            connection,
                            str(row["strategy_backtest_id"]),
                            backtest_payload,
                            result_payload,
                        )


def _update_backtest_payload(
    connection,
    backtest_id: str,
    current_payload: object,
    result_payload: object,
) -> None:
    payload = _json_object(current_payload)
    if payload is None:
        return
    if "backtest" in payload:
        merged_payload = dict(payload)
    else:
        merged_payload = {"backtest": payload}
    merged_payload.setdefault("schema_version", 1)
    merged_payload["result"] = result_payload
    connection.execute(
        text("UPDATE strategy_backtests SET payload_json = :payload WHERE id = :backtest_id"),
        {
            "backtest_id": backtest_id,
            "payload": json.dumps(merged_payload, separators=(",", ":")),
        },
    )


def _json_object(value: object) -> dict[str, object] | None:
    if value is None:
        return None
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        loaded = json.loads(value)
        return loaded if isinstance(loaded, dict) else None
    return None


def _drop_retired_backtest_result_table(engine: Engine) -> None:
    inspector = inspect(engine)
    if "strategy_backtest_results" not in inspector.get_table_names():
        return
    with engine.begin() as connection:
        connection.execute(text("DROP TABLE strategy_backtest_results"))


def _drop_retired_artifact_tables(engine: Engine) -> None:
    inspector = inspect(engine)
    table_names = set(inspector.get_table_names())
    artifact_tables = [
        "artifact_links",
        "artifact_versions",
        "artifact_files",
        "code_artifacts",
    ]
    existing_tables = [table_name for table_name in artifact_tables if table_name in table_names]
    if not existing_tables:
        return
    with engine.begin() as connection:
        for table_name in existing_tables:
            connection.execute(text(f"DROP TABLE {table_name}"))
