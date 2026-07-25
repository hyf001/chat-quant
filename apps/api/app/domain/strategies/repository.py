from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from threading import RLock

from app.domain.backtests.models import (
    StrategyBacktestRecord,
    StrategyBacktestResultRecord,
)
from app.domain.strategies.models import (
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
            connection.execute("delete from strategy_backtest_results")
            connection.execute("delete from strategy_backtests")
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
                    status, created_at, payload_json
                )
                values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                on conflict(id) do update set
                    version_name=excluded.version_name,
                    status=excluded.status,
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

    def add_backtest(self, backtest: StrategyBacktestRecord) -> None:
        self.save_backtest(backtest)

    def save_backtest(self, backtest: StrategyBacktestRecord) -> None:
        with self._lock, self._connect() as connection:
            connection.execute(
                """
                insert into strategy_backtests (
                    id, user_id, project_id, chat_session_id, strategy_id,
                    strategy_version_id, run_type, status, config_hash,
                    result_id, started_at, completed_at, created_at, updated_at,
                    payload_json
                )
                values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                on conflict(id) do update set
                    status=excluded.status,
                    result_id=excluded.result_id,
                    started_at=excluded.started_at,
                    completed_at=excluded.completed_at,
                    updated_at=excluded.updated_at,
                    payload_json=excluded.payload_json
                """,
                (
                    backtest.id,
                    backtest.user_id,
                    backtest.project_id,
                    backtest.chat_session_id,
                    backtest.strategy_id,
                    backtest.strategy_version_id,
                    "backtest",
                    backtest.status.value,
                    backtest.config_hash,
                    backtest.result_id,
                    backtest.started_at.isoformat() if backtest.started_at else None,
                    backtest.completed_at.isoformat() if backtest.completed_at else None,
                    backtest.created_at.isoformat(),
                    backtest.updated_at.isoformat(),
                    _json_dump(backtest),
                ),
            )

    def get_backtest(self, backtest_id: str) -> StrategyBacktestRecord | None:
        row = self._fetch_one(
            "select payload_json from strategy_backtests where id = ?",
            (backtest_id,),
        )
        if row is None:
            return None
        return StrategyBacktestRecord.model_validate_json(row["payload_json"])

    def list_backtests(
        self,
        *,
        strategy_version_id: str | None,
        limit: int,
    ) -> list[StrategyBacktestRecord]:
        with self._lock, self._connect() as connection:
            params: tuple[object, ...]
            where_clause = ""
            if strategy_version_id is not None:
                where_clause = "where strategy_version_id = ?"
                params = (strategy_version_id, limit)
            else:
                params = (limit,)
            rows = connection.execute(
                f"""
                select payload_json
                from strategy_backtests
                {where_clause}
                order by created_at desc
                limit ?
                """,
                params,
            ).fetchall()
        return [StrategyBacktestRecord.model_validate_json(row["payload_json"]) for row in rows]

    def save_backtest_result(self, result: StrategyBacktestResultRecord) -> None:
        with self._lock, self._connect() as connection:
            connection.execute(
                """
                insert into strategy_backtest_results (
                    id, strategy_backtest_id, created_at, payload_json
                )
                values (?, ?, ?, ?)
                on conflict(id) do update set
                    payload_json=excluded.payload_json
                """,
                (
                    result.id,
                    result.strategy_backtest_id,
                    result.created_at.isoformat(),
                    _json_dump(result),
                ),
            )

    def get_backtest_result(self, backtest_id: str) -> StrategyBacktestResultRecord | None:
        row = self._fetch_one(
            "select payload_json from strategy_backtest_results where strategy_backtest_id = ?",
            (backtest_id,),
        )
        if row is None:
            return None
        return StrategyBacktestResultRecord.model_validate_json(row["payload_json"])

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

                create table if not exists strategy_backtests (
                    id text primary key,
                    user_id text not null,
                    project_id text not null,
                    chat_session_id text not null,
                    strategy_id text not null references strategies(id),
                    strategy_version_id text not null references strategy_versions(id),
                    run_type text not null,
                    status text not null,
                    config_hash text not null,
                    result_id text,
                    started_at text,
                    completed_at text,
                    created_at text not null,
                    updated_at text not null,
                    payload_json text not null
                );

                create index if not exists idx_strategy_backtests_version_created
                    on strategy_backtests(strategy_version_id, created_at);
                create index if not exists idx_strategy_backtests_status
                    on strategy_backtests(status);

                create table if not exists strategy_backtest_results (
                    id text primary key,
                    strategy_backtest_id text not null references strategy_backtests(id),
                    created_at text not null,
                    payload_json text not null
                );

                create unique index if not exists uq_strategy_backtest_results_run
                    on strategy_backtest_results(strategy_backtest_id);
                """
            )


def _json_dump(
    record: (
        StrategyRecord
        | StrategyVersionRecord
        | StrategyBacktestRecord
        | StrategyBacktestResultRecord
    ),
) -> str:
    return record.model_dump_json()


strategy_repository = StrategyRepository()
