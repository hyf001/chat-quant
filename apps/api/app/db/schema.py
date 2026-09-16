from __future__ import annotations

import json
import logging
from threading import Lock

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError

from app.core.config import (
    APP_CONFIG_DEFINITIONS,
    DEFAULT_MODEL_PROVIDER_ID,
    DEFAULT_MODEL_PROVIDER_NAME,
    Settings,
    default_app_config_values,
)
from app.db.session import Base, sync_database_url
from app.model.chat_session import chat_session as chat_session_model  # noqa: F401
from app.model.config import app_setting as app_setting_model  # noqa: F401
from app.model.config import model_provider as model_provider_model  # noqa: F401
from app.model.dataset import dataset as dataset_model  # noqa: F401
from app.model.job_runtime import job_runtime as job_runtime_model  # noqa: F401
from app.model.project import project as project_model  # noqa: F401
from app.model.stock_pool import stock_pool as stock_pool_model  # noqa: F401
from app.model.strategy import strategy as strategy_model  # noqa: F401
from app.model.training import training as training_model  # noqa: F401

_SCHEMA_LOCK = Lock()
_INITIALIZED_DATABASE_URLS: set[str] = set()
logger = logging.getLogger(__name__)


def ensure_database_schema(settings: Settings) -> None:
    database_url = sync_database_url(settings)
    with _SCHEMA_LOCK:
        if database_url in _INITIALIZED_DATABASE_URLS and settings.database_path.exists():
            return
        settings.database_path.parent.mkdir(parents=True, exist_ok=True)
        engine = create_engine(database_url)
        try:
            Base.metadata.create_all(engine)
            _migrate_job_runtime_scheduler_schema(engine)
            _migrate_job_runtime_instance_trigger_schema(engine)
            _migrate_local_project_schema(engine, settings)
            _migrate_strategy_source_code(engine)
            _migrate_strategy_version_contract(engine)
            _merge_backtest_payloads(engine)
            _migrate_strategy_deployment_schema(engine)
            _migrate_market_data_settings(engine)
            _seed_model_providers(engine)
            _seed_app_settings(engine, settings)
            _migrate_legacy_agent_provider_settings(engine)
            _drop_retired_strategy_columns(engine)
            _drop_retired_backtest_result_table(engine)
            _drop_retired_artifact_tables(engine)
        finally:
            engine.dispose()
        _INITIALIZED_DATABASE_URLS.add(database_url)


def _migrate_local_project_schema(engine: Engine, settings: Settings) -> None:
    inspector = inspect(engine)
    table_names = set(inspector.get_table_names())
    if "projects" in table_names:
        _migrate_projects_local_path(engine, inspector, settings)
    for table_name, index_names in {
        "chat_sessions": ("idx_chat_sessions_user_updated",),
        "strategies": ("idx_strategies_user_project_updated",),
        "strategy_backtests": (),
    }.items():
        if table_name in table_names:
            _drop_column_if_exists(engine, inspector, table_name, "user_id", index_names)


def _migrate_projects_local_path(
    engine: Engine, inspector, settings: Settings
) -> None:
    columns = {column["name"] for column in inspector.get_columns("projects")}
    with engine.begin() as connection:
        if "local_path" not in columns:
            connection.execute(text("ALTER TABLE projects ADD COLUMN local_path TEXT"))
            legacy_root = settings.database_path.parent / "projects"
            rows = connection.execute(text("SELECT id FROM projects")).mappings()
            for row in rows:
                project_id = str(row["id"])
                legacy_path = str((legacy_root / project_id).expanduser().resolve(strict=False))
                connection.execute(
                    text("UPDATE projects SET local_path = :local_path WHERE id = :id"),
                    {"id": project_id, "local_path": legacy_path},
                )
        connection.execute(text("DROP INDEX IF EXISTS idx_projects_user_updated"))
        connection.execute(
            text("CREATE INDEX IF NOT EXISTS idx_projects_updated ON projects(updated_at)")
        )
        connection.execute(
            text(
                "CREATE UNIQUE INDEX IF NOT EXISTS "
                "idx_projects_local_path_unique ON projects(local_path)"
            )
        )
    _drop_column_if_exists(engine, inspector, "projects", "user_id", ())


def _drop_column_if_exists(
    engine: Engine,
    inspector,
    table_name: str,
    column_name: str,
    index_names: tuple[str, ...],
) -> None:
    columns = {column["name"] for column in inspector.get_columns(table_name)}
    if column_name not in columns:
        return
    with engine.begin() as connection:
        for index_name in index_names:
            connection.execute(text(f"DROP INDEX IF EXISTS {index_name}"))
        connection.execute(text(f"ALTER TABLE {table_name} DROP COLUMN {column_name}"))


def _migrate_job_runtime_scheduler_schema(engine: Engine) -> None:
    inspector = inspect(engine)
    if "job_schedulers" not in inspector.get_table_names():
        return
    with engine.begin() as connection:
        connection.execute(text("DROP INDEX IF EXISTS idx_job_schedulers_enabled"))
        connection.execute(
            text(
                "CREATE INDEX IF NOT EXISTS "
                "idx_job_schedulers_job_type ON job_schedulers(job_type)"
            )
        )
    for column_name in ("enabled", "run_mode", "run_at", "timezone"):
        _drop_column_if_exists(engine, inspect(engine), "job_schedulers", column_name, ())


def _migrate_job_runtime_instance_trigger_schema(engine: Engine) -> None:
    inspector = inspect(engine)
    if "job_instances" not in inspector.get_table_names():
        return
    trigger_columns = ("job_type", "job_id", "trigger_key")
    for constraint in inspector.get_unique_constraints("job_instances"):
        if tuple(constraint.get("column_names") or ()) == trigger_columns:
            return
    for index in inspector.get_indexes("job_instances"):
        if tuple(index.get("column_names") or ()) == trigger_columns and index.get("unique"):
            return
    try:
        with engine.begin() as connection:
            connection.execute(
                text(
                    "CREATE UNIQUE INDEX IF NOT EXISTS "
                    "idx_job_instances_trigger_key_unique "
                    "ON job_instances(job_type, job_id, trigger_key)"
                )
            )
    except IntegrityError:
        logger.warning(
            "job_instances has duplicate job_type/job_id/trigger_key rows; "
            "skipping trigger-key unique index migration"
        )


def _seed_model_providers(engine: Engine) -> None:
    inspector = inspect(engine)
    if "model_providers" not in inspector.get_table_names():
        return

    with engine.begin() as connection:
        count = connection.execute(
            text("SELECT COUNT(*) FROM model_providers WHERE id = :id"),
            {"id": DEFAULT_MODEL_PROVIDER_ID},
        ).scalar_one()
        if count:
            return
        connection.execute(
            text(
                "INSERT INTO model_providers "
                "(id, name, base_url, api_key, enabled, created_at, updated_at) "
                "VALUES (:id, :name, NULL, NULL, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)"
            ),
            {"id": DEFAULT_MODEL_PROVIDER_ID, "name": DEFAULT_MODEL_PROVIDER_NAME},
        )


def _seed_app_settings(engine: Engine, settings: Settings) -> None:
    inspector = inspect(engine)
    if "app_settings" not in inspector.get_table_names():
        return

    now = "CURRENT_TIMESTAMP"
    defaults = default_app_config_values()
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


def _migrate_market_data_settings(engine: Engine) -> None:
    inspector = inspect(engine)
    if "app_settings" not in inspector.get_table_names():
        return
    with engine.begin() as connection:
        legacy_market = _legacy_setting_json(connection, "market_data_dataset")
        legacy_benchmark = _legacy_setting_json(connection, "benchmark_dataset")
        if not _dataset_configured(legacy_market):
            legacy_market = _legacy_setting_json(connection, "market_data_day_dataset")
        if not _dataset_configured(legacy_benchmark):
            legacy_benchmark = _legacy_setting_json(connection, "benchmark_day_dataset")
        if not _dataset_configured(legacy_market):
            legacy_market = _legacy_setting_json(connection, "backtest_market_dataset")
        if not _dataset_configured(legacy_benchmark):
            legacy_benchmark = _legacy_setting_json(connection, "backtest_benchmark_dataset")
        grouped_market = _legacy_setting_json(connection, "market_data_datasets")
        grouped_benchmark = _legacy_setting_json(connection, "market_data_benchmark_datasets")
        market_day = _legacy_daily_dataset(grouped_market)
        benchmark_day = _legacy_daily_dataset(grouped_benchmark)
        if not _dataset_configured(market_day):
            market_day = legacy_market
        if not _dataset_configured(benchmark_day):
            benchmark_day = legacy_benchmark
        if _dataset_configured(market_day):
            _upsert_app_setting(
                connection,
                namespace="market_data",
                key="market_data_dataset",
                value=market_day,
                label="行情数据集",
                description="策略执行和回测使用的行情数据集和 OHLCV 字段映射。",
            )
        if _dataset_configured(benchmark_day):
            _upsert_app_setting(
                connection,
                namespace="market_data",
                key="benchmark_dataset",
                value=benchmark_day,
                label="基准数据集",
                description="策略执行和回测使用的基准数据集和字段映射。",
            )
        connection.execute(
            text(
                "DELETE FROM app_settings "
                "WHERE scope = 'global' "
                "AND key IN ("
                "'backtest_market_dataset', "
                "'backtest_benchmark_dataset', "
                "'market_data_datasets', "
                "'market_data_benchmark_datasets', "
                "'market_data_month_dataset', "
                "'market_data_week_dataset', "
                "'market_data_day_dataset', "
                "'market_data_hour_dataset', "
                "'market_data_minute_dataset', "
                "'benchmark_month_dataset', "
                "'benchmark_week_dataset', "
                "'benchmark_day_dataset', "
                "'benchmark_hour_dataset', "
                "'benchmark_minute_dataset'"
                ")"
            )
        )


def _legacy_setting_json(connection, key: str) -> dict[str, object] | None:
    row = connection.execute(
        text(
            "SELECT value_json FROM app_settings "
            "WHERE scope = 'global' AND key = :key "
            "ORDER BY updated_at DESC LIMIT 1"
        ),
        {"key": key},
    ).mappings().first()
    if row is None:
        return None
    return _json_object(row["value_json"])


def _legacy_daily_dataset(value: dict[str, object] | None) -> dict[str, object] | None:
    if value is None:
        return None
    for key in ("day", "1d", "daily", "d"):
        dataset = _json_object(value.get(key))
        if dataset is not None:
            return dataset
    return None


def _dataset_configured(value: dict[str, object] | None) -> bool:
    if value is None:
        return False
    dataset_id = value.get("dataset_id")
    return isinstance(dataset_id, str) and bool(dataset_id.strip())


def _upsert_app_setting(
    connection,
    *,
    namespace: str,
    key: str,
    value: dict[str, object],
    label: str,
    description: str,
) -> None:
    count = connection.execute(
        text(
            "SELECT COUNT(*) FROM app_settings "
            "WHERE scope = 'global' AND namespace = :namespace AND key = :key"
        ),
        {"namespace": namespace, "key": key},
    ).scalar_one()
    params = {
        "namespace": namespace,
        "key": key,
        "value_json": json.dumps(value),
        "label": label,
        "description": description,
    }
    if count:
        connection.execute(
            text(
                "UPDATE app_settings "
                "SET value_json = :value_json, value_type = 'json', is_secret = 0, "
                "label = :label, description = :description, updated_at = CURRENT_TIMESTAMP "
                "WHERE scope = 'global' AND namespace = :namespace AND key = :key"
            ),
            params,
        )
        return
    connection.execute(
        text(
            "INSERT INTO app_settings "
            "(scope, namespace, key, value_json, value_type, is_secret, "
            "label, description, updated_at) VALUES "
            "('global', :namespace, :key, :value_json, 'json', 0, "
            ":label, :description, CURRENT_TIMESTAMP)"
        ),
        params,
    )


def _migrate_legacy_agent_provider_settings(engine: Engine) -> None:
    inspector = inspect(engine)
    table_names = set(inspector.get_table_names())
    if "app_settings" not in table_names or "model_providers" not in table_names:
        return

    with engine.begin() as connection:
        rows = connection.execute(
            text(
                "SELECT key, value_json FROM app_settings "
                "WHERE scope = 'global' AND namespace = 'agent' "
                "AND key IN ('agent_base_url', 'agent_api_token')"
            )
        ).mappings()
        legacy_values = {str(row["key"]): _schema_json_value(row["value_json"]) for row in rows}
        base_url = legacy_values.get("agent_base_url")
        api_key = legacy_values.get("agent_api_token")
        if not isinstance(base_url, str) and not isinstance(api_key, str):
            return
        connection.execute(
            text(
                "UPDATE model_providers "
                "SET base_url = COALESCE(:base_url, base_url), "
                "api_key = COALESCE(:api_key, api_key), "
                "updated_at = CURRENT_TIMESTAMP "
                "WHERE id = :id"
            ),
            {
                "id": DEFAULT_MODEL_PROVIDER_ID,
                "base_url": base_url if isinstance(base_url, str) and base_url else None,
                "api_key": api_key if isinstance(api_key, str) and api_key else None,
            },
        )


def _schema_json_value(value: object) -> object:
    if not isinstance(value, str):
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return None


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
        "strategy_deployments": {"timeframe"},
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


def _migrate_strategy_deployment_schema(engine: Engine) -> None:
    inspector = inspect(engine)
    if "strategy_deployments" not in inspector.get_table_names():
        return
    columns = {column["name"] for column in inspector.get_columns("strategy_deployments")}
    with engine.begin() as connection:
        connection.execute(text("DROP INDEX IF EXISTS idx_strategy_deployments_enabled_mode"))
        connection.execute(
            text(
                "CREATE INDEX IF NOT EXISTS "
                "idx_strategy_deployments_mode ON strategy_deployments(mode)"
            )
        )
        if "lookback_bars" not in columns:
            connection.execute(
                text(
                    "ALTER TABLE strategy_deployments "
                    "ADD COLUMN lookback_bars INTEGER NOT NULL DEFAULT 250"
                )
            )
    for column_name in ("enabled", "market_data_source_id"):
        _drop_column_if_exists(engine, inspect(engine), "strategy_deployments", column_name, ())


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
