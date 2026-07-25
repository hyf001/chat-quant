from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from threading import RLock

from app.domain.strategies.models import (
    StrategyCopyRecord,
    StrategyRecord,
    StrategyStatus,
    StrategyVersionRecord,
)


class StrategyRepository:
    def __init__(self, db_path: str = "storage/m5_strategy_assets.sqlite3") -> None:
        self.db_path = Path(db_path)
        self._lock = RLock()
        self._connect().close()
        self._migrate()

    def clear(self) -> None:
        with self._lock, self._connect() as connection:
            connection.execute("delete from strategy_copy_records")
            connection.execute("delete from strategy_versions")
            connection.execute("delete from strategies")

    def add_strategy(self, strategy: StrategyRecord) -> None:
        self.save_strategy(strategy)

    def save_strategy(self, strategy: StrategyRecord) -> None:
        payload = _json_dump(strategy)
        with self._lock, self._connect() as connection:
            connection.execute(
                """
                insert into strategies (
                    id, user_id, project_id, chat_session_id, source_sdk_message_uuid,
                    name, description, strategy_type, tags_json, current_version_id,
                    status, created_at, updated_at, payload_json
                )
                values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                on conflict(id) do update set
                    user_id=excluded.user_id,
                    project_id=excluded.project_id,
                    chat_session_id=excluded.chat_session_id,
                    source_sdk_message_uuid=excluded.source_sdk_message_uuid,
                    name=excluded.name,
                    description=excluded.description,
                    strategy_type=excluded.strategy_type,
                    tags_json=excluded.tags_json,
                    current_version_id=excluded.current_version_id,
                    status=excluded.status,
                    updated_at=excluded.updated_at,
                    payload_json=excluded.payload_json
                """,
                (
                    strategy.id,
                    strategy.user_id,
                    strategy.project_id,
                    strategy.chat_session_id,
                    strategy.source_sdk_message_uuid,
                    strategy.name,
                    strategy.description,
                    strategy.strategy_type,
                    json.dumps(strategy.tags, ensure_ascii=False),
                    strategy.current_version_id,
                    strategy.status.value,
                    strategy.created_at.isoformat(),
                    strategy.updated_at.isoformat(),
                    payload,
                ),
            )

    def get_strategy(self, strategy_id: str) -> StrategyRecord | None:
        row = self._fetch_one("select payload_json from strategies where id = ?", (strategy_id,))
        if row is None:
            return None
        return StrategyRecord.model_validate_json(row["payload_json"])

    def list_strategies(self, user_id: str, project_id: str) -> list[StrategyRecord]:
        with self._lock, self._connect() as connection:
            rows = connection.execute(
                """
                select payload_json
                from strategies
                where user_id = ?
                  and project_id = ?
                  and status != ?
                order by updated_at desc
                """,
                (user_id, project_id, StrategyStatus.DELETED.value),
            ).fetchall()
        return [StrategyRecord.model_validate_json(row["payload_json"]) for row in rows]

    def add_version(self, version: StrategyVersionRecord) -> None:
        self.save_version(version)

    def save_version(self, version: StrategyVersionRecord) -> None:
        payload = _json_dump(version)
        with self._lock, self._connect() as connection:
            connection.execute(
                """
                insert into strategy_versions (
                    id, strategy_id, version, version_name, parent_version_id,
                    code_artifact_id, entrypoint, params_schema_json, default_params_json,
                    logic_summary, change_summary, source_sdk_session_id,
                    source_sdk_message_uuid, source_sdk_tool_use_id, code_checksum,
                    status, validation_error, validation_details_json, validated_at,
                    created_at, payload_json
                )
                values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                on conflict(id) do update set
                    version_name=excluded.version_name,
                    status=excluded.status,
                    validation_error=excluded.validation_error,
                    validation_details_json=excluded.validation_details_json,
                    validated_at=excluded.validated_at,
                    payload_json=excluded.payload_json
                """,
                (
                    version.id,
                    version.strategy_id,
                    version.version,
                    version.version_name,
                    version.parent_version_id,
                    version.code_artifact_id,
                    version.entrypoint,
                    json.dumps(
                        {
                            key: value.model_dump(mode="json")
                            for key, value in version.params_schema.items()
                        },
                        ensure_ascii=False,
                    ),
                    json.dumps(version.default_params, ensure_ascii=False),
                    version.logic_summary,
                    version.change_summary,
                    version.source_sdk_session_id,
                    version.source_sdk_message_uuid,
                    version.source_sdk_tool_use_id,
                    version.code_checksum,
                    version.status.value,
                    version.validation_error,
                    json.dumps(
                        [check.model_dump(mode="json") for check in version.validation_details],
                        ensure_ascii=False,
                    ),
                    version.validated_at.isoformat() if version.validated_at else None,
                    version.created_at.isoformat(),
                    payload,
                ),
            )

    def get_version(self, version_id: str) -> StrategyVersionRecord | None:
        row = self._fetch_one(
            "select payload_json from strategy_versions where id = ?",
            (version_id,),
        )
        if row is None:
            return None
        return StrategyVersionRecord.model_validate_json(row["payload_json"])

    def list_versions(self, strategy_id: str) -> list[StrategyVersionRecord]:
        with self._lock, self._connect() as connection:
            rows = connection.execute(
                """
                select payload_json
                from strategy_versions
                where strategy_id = ?
                order by version asc
                """,
                (strategy_id,),
            ).fetchall()
        return [StrategyVersionRecord.model_validate_json(row["payload_json"]) for row in rows]

    def next_version_number(self, strategy_id: str) -> int:
        with self._lock, self._connect() as connection:
            row = connection.execute(
                """
                select coalesce(max(version), 0) as max_version
                from strategy_versions
                where strategy_id = ?
                """,
                (strategy_id,),
            ).fetchone()
        return int(row["max_version"]) + 1

    def add_copy_record(self, record: StrategyCopyRecord) -> None:
        with self._lock, self._connect() as connection:
            connection.execute(
                """
                insert into strategy_copy_records (
                    id, source_strategy_version_id, target_strategy_id,
                    target_chat_session_id, mode, created_by, created_at, payload_json
                )
                values (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record.id,
                    record.source_strategy_version_id,
                    record.target_strategy_id,
                    record.target_chat_session_id,
                    record.mode.value,
                    record.created_by,
                    record.created_at.isoformat(),
                    _json_dump(record),
                ),
            )

    def _connect(self) -> sqlite3.Connection:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        connection.execute("pragma foreign_keys = on")
        return connection

    def _fetch_one(self, query: str, params: tuple[str, ...]) -> sqlite3.Row | None:
        with self._lock, self._connect() as connection:
            return connection.execute(query, params).fetchone()

    def _migrate(self) -> None:
        with self._lock, self._connect() as connection:
            connection.executescript(
                """
                create table if not exists strategies (
                    id text primary key,
                    user_id text not null,
                    project_id text not null,
                    chat_session_id text not null,
                    source_sdk_message_uuid text,
                    name text not null,
                    description text,
                    strategy_type text not null,
                    tags_json text not null default '[]',
                    current_version_id text,
                    status text not null,
                    created_at text not null,
                    updated_at text not null,
                    payload_json text not null
                );

                create index if not exists idx_strategies_user_project_updated
                    on strategies(user_id, project_id, updated_at);
                create index if not exists idx_strategies_chat_session
                    on strategies(chat_session_id);
                create index if not exists idx_strategies_type
                    on strategies(strategy_type);

                create table if not exists strategy_versions (
                    id text primary key,
                    strategy_id text not null references strategies(id),
                    version integer not null check(version > 0),
                    version_name text,
                    parent_version_id text,
                    code_artifact_id text not null,
                    entrypoint text not null,
                    params_schema_json text not null,
                    default_params_json text not null,
                    logic_summary text,
                    change_summary text,
                    source_sdk_session_id text,
                    source_sdk_message_uuid text,
                    source_sdk_tool_use_id text,
                    code_checksum text not null,
                    status text not null,
                    validation_error text,
                    validation_details_json text,
                    validated_at text,
                    created_at text not null,
                    payload_json text not null,
                    unique(strategy_id, version)
                );

                create index if not exists idx_strategy_versions_strategy
                    on strategy_versions(strategy_id, version);
                create index if not exists idx_strategy_versions_parent
                    on strategy_versions(parent_version_id);
                create index if not exists idx_strategy_versions_artifact
                    on strategy_versions(code_artifact_id);
                create index if not exists idx_strategy_versions_status
                    on strategy_versions(status);

                create table if not exists strategy_copy_records (
                    id text primary key,
                    source_strategy_version_id text not null references strategy_versions(id),
                    target_strategy_id text references strategies(id),
                    target_chat_session_id text,
                    mode text not null,
                    created_by text not null,
                    created_at text not null,
                    payload_json text not null
                );

                create index if not exists idx_strategy_copy_records_source
                    on strategy_copy_records(source_strategy_version_id);
                create index if not exists idx_strategy_copy_records_target
                    on strategy_copy_records(target_strategy_id);
                """
            )


def _json_dump(record: StrategyRecord | StrategyVersionRecord | StrategyCopyRecord) -> str:
    return record.model_dump_json()


strategy_repository = StrategyRepository()
