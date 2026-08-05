from __future__ import annotations

import json
from threading import Lock

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine

from app.core.config import APP_CONFIG_DEFINITIONS, Settings, default_app_config_values
from app.db.session import Base, sync_database_url
from app.model.chat_session import chat_session as chat_session_model  # noqa: F401
from app.model.config import app_setting as app_setting_model  # noqa: F401
from app.model.project import project as project_model  # noqa: F401
from app.model.strategy import strategy as strategy_model  # noqa: F401

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
            _migrate_strategy_source_code(engine)
            _migrate_strategy_version_contract(engine)
            _merge_backtest_payloads(engine)
            _seed_app_settings(engine, settings)
            _drop_retired_strategy_columns(engine)
            _drop_retired_backtest_result_table(engine)
            _drop_retired_artifact_tables(engine)
        finally:
            engine.dispose()
        _INITIALIZED_DATABASE_URLS.add(database_url)


def _seed_app_settings(engine: Engine, settings: Settings) -> None:
    inspector = inspect(engine)
    if "app_settings" not in inspector.get_table_names():
        return

    now = "CURRENT_TIMESTAMP"
    defaults = default_app_config_values(settings.database_path)
    with engine.begin() as connection:
        for definition in APP_CONFIG_DEFINITIONS:
            count = connection.execute(
                text(
                    "SELECT COUNT(*) FROM app_settings "
                    "WHERE scope = 'global' AND namespace = :namespace AND key = :key"
                ),
                {"namespace": definition.group, "key": definition.key},
            ).scalar_one()
            if count:
                continue
            connection.execute(
                text(
                    "INSERT INTO app_settings "
                    "(scope, namespace, key, value_json, value_type, is_secret, "
                    f"label, description, updated_at) VALUES "
                    "('global', :namespace, :key, :value_json, :value_type, :is_secret, "
                    f":label, :description, {now})"
                ),
                {
                    "namespace": definition.group,
                    "key": definition.key,
                    "value_json": json.dumps(defaults[definition.key]),
                    "value_type": definition.value_type,
                    "is_secret": definition.value_type == "password",
                    "label": definition.label,
                    "description": definition.description,
                },
            )


def _drop_retired_strategy_columns(engine: Engine) -> None:
    inspector = inspect(engine)
    table_names = set(inspector.get_table_names())
    if "strategies" not in table_names:
        return

    retired_columns_by_table = {
        "strategies": {
            "chat_session_id",
            "payload_json",
            "source_sdk_message_uuid",
            "strategy_type",
        },
        "strategy_versions": {
            "change_summary",
            "code_checksum",
            "strategy_config_json",
            "logic_summary",
            "parent_version_id",
            "entrypoint",
            "payload_json",
            "python_file_content",
            "python_file_path",
            "params_schema_json",
            "default_params_json",
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


def _migrate_strategy_source_code(engine: Engine) -> None:
    inspector = inspect(engine)
    table_names = set(inspector.get_table_names())
    if "strategy_versions" not in table_names:
        return

    columns = {column["name"] for column in inspector.get_columns("strategy_versions")}
    with engine.begin() as connection:
        if "source_code" not in columns:
            connection.execute(
                text(
                    "ALTER TABLE strategy_versions "
                    "ADD COLUMN source_code TEXT NOT NULL DEFAULT ''"
                )
            )
            columns.add("source_code")

        select_columns = ["id"]
        if "payload_json" in columns:
            select_columns.append("payload_json")
        if "python_file_content" in columns:
            select_columns.append("python_file_content")
        if len(select_columns) == 1:
            return

        rows = connection.execute(
            text(f"SELECT {', '.join(select_columns)} FROM strategy_versions")
        ).mappings()
        for row in rows:
            source_code = _strategy_source_code_from_row(row)
            if source_code:
                connection.execute(
                    text("UPDATE strategy_versions SET source_code = :source_code WHERE id = :id"),
                    {"id": row["id"], "source_code": source_code},
                )


def _strategy_source_code_from_row(row: object) -> str | None:
    if not isinstance(row, dict):
        row = dict(row)

    python_file_content = row.get("python_file_content")
    if isinstance(python_file_content, str) and python_file_content:
        return python_file_content

    payload = _json_object(row.get("payload_json"))
    if payload is None:
        return None

    python_file = payload.get("python_file")
    if isinstance(python_file, dict) and isinstance(python_file.get("content"), str):
        return python_file["content"]

    code_files = payload.get("code_files")
    if isinstance(code_files, list):
        selected = next((item for item in code_files if isinstance(item, dict)), None)
        if selected is not None and isinstance(selected.get("content"), str):
            return selected["content"]

    return None


def _migrate_strategy_version_contract(engine: Engine) -> None:
    inspector = inspect(engine)
    if "strategy_versions" not in inspector.get_table_names():
        return

    columns = {column["name"] for column in inspector.get_columns("strategy_versions")}
    with engine.begin() as connection:
        if "custom_params_json" not in columns:
            connection.execute(
                text(
                    "ALTER TABLE strategy_versions "
                    "ADD COLUMN custom_params_json JSON NOT NULL DEFAULT '[]'"
                )
            )
            columns.add("custom_params_json")
        if "strategy_mode" not in columns:
            connection.execute(
                text(
                    "ALTER TABLE strategy_versions "
                    "ADD COLUMN strategy_mode TEXT NOT NULL DEFAULT 'single_symbol'"
                )
            )
            columns.add("strategy_mode")

        select_columns = ["id"]
        if "params_schema_json" in columns:
            select_columns.append("params_schema_json")
        if "default_params_json" in columns:
            select_columns.append("default_params_json")
        if len(select_columns) == 1:
            return

        rows = connection.execute(
            text(f"SELECT {', '.join(select_columns)} FROM strategy_versions")
        ).mappings()
        for row in rows:
            custom_params = _custom_params_from_legacy_row(row)
            connection.execute(
                text(
                    "UPDATE strategy_versions "
                    "SET custom_params_json = :custom_params "
                    "WHERE id = :id"
                ),
                {"id": row["id"], "custom_params": json.dumps(custom_params)},
            )


def _custom_params_from_legacy_row(row: object) -> list[dict[str, object]]:
    if not isinstance(row, dict):
        row = dict(row)
    params_schema = _json_object(row.get("params_schema_json")) or {}
    default_params = _json_object(row.get("default_params_json")) or {}
    custom_params: list[dict[str, object]] = []
    for name, spec_value in params_schema.items():
        spec = spec_value if isinstance(spec_value, dict) else {}
        custom_params.append(
            {
                "name_cn": str(spec.get("title") or name),
                "name_en": name,
                "type": spec.get("type") or "string",
                "default": default_params.get(name, spec.get("default")),
                "required": bool(spec.get("required", True)),
            }
        )
    return custom_params


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
