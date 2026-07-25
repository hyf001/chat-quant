from __future__ import annotations

import json
from hashlib import sha256
from uuid import uuid4

from app.domain.backtests.execution import StrategyBacktestEngine, StrategyBacktestError
from app.domain.backtests.models import (
    JsonValue,
    StrategyBacktestConfig,
    StrategyBacktestDetail,
    StrategyBacktestRecord,
    StrategyBacktestStatus,
)
from app.domain.strategies.models import (
    StrategyCreateResult,
    StrategyDetail,
    StrategyPackage,
    StrategyRecord,
    StrategyStatus,
    StrategySummary,
    StrategyVersionRecord,
    utc_now,
    validate_param_value,
)
from app.domain.strategies.repository import StrategyRepository, strategy_repository


class StrategyError(Exception):
    def __init__(self, error_code: str, message: str, status_code: int = 400) -> None:
        super().__init__(message)
        self.error_code = error_code
        self.message = message
        self.status_code = status_code


class StrategyService:
    def __init__(self, repository: StrategyRepository) -> None:
        self.repository = repository

    def list_strategies(self, user_id: str, project_id: str) -> list[StrategySummary]:
        return [
            self._to_summary(strategy)
            for strategy in self.repository.list_strategies(user_id, project_id)
        ]

    def create_strategy(
        self,
        *,
        user_id: str,
        project_id: str,
        chat_session_id: str,
        package: StrategyPackage,
        source_sdk_session_id: str | None = None,
        source_sdk_message_uuid: str | None = None,
        source_sdk_tool_use_id: str | None = None,
    ) -> StrategyCreateResult:
        strategy = StrategyRecord(
            id=_new_id("str"),
            user_id=user_id,
            project_id=project_id,
            chat_session_id=chat_session_id,
            source_sdk_message_uuid=source_sdk_message_uuid,
            name=package.name,
            description=package.description,
            strategy_type=package.strategy_type,
            tags=_default_tags(package),
        )
        version = self._build_version(
            strategy_id=strategy.id,
            version_number=1,
            package=package,
            parent_version_id=None,
            change_summary=None,
            source_sdk_session_id=source_sdk_session_id,
            source_sdk_message_uuid=source_sdk_message_uuid,
            source_sdk_tool_use_id=source_sdk_tool_use_id,
        )
        strategy.current_version_id = version.id

        self.repository.add_strategy(strategy)
        self.repository.add_version(version)
        return StrategyCreateResult(
            strategy_id=strategy.id,
            entrypoint=version.entrypoint,
        )

    def get_strategy(self, strategy_id: str) -> StrategyDetail:
        strategy = self._require_strategy(strategy_id)
        return StrategyDetail(strategy=strategy)

    def update_strategy_metadata(
        self,
        strategy_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        tags: list[str] | None = None,
        status: StrategyStatus | None = None,
    ) -> StrategyRecord:
        strategy = self._require_strategy(strategy_id)
        if strategy.status == StrategyStatus.DELETED:
            raise StrategyError("STRATEGY_DELETED", "Strategy is deleted", 409)

        update_data: dict[str, object] = {"updated_at": utc_now()}
        if name is not None:
            update_data["name"] = name
        if description is not None:
            update_data["description"] = description
        if tags is not None:
            update_data["tags"] = _normalize_tags(tags)
        if status is not None:
            update_data["status"] = status

        strategy = strategy.model_copy(update=update_data)
        self.repository.save_strategy(strategy)
        return strategy

    def _build_version(
        self,
        *,
        strategy_id: str,
        version_number: int,
        package: StrategyPackage,
        parent_version_id: str | None,
        change_summary: str | None,
        source_sdk_session_id: str | None,
        source_sdk_message_uuid: str | None,
        source_sdk_tool_use_id: str | None,
    ) -> StrategyVersionRecord:
        return StrategyVersionRecord(
            id=_new_id("stv"),
            strategy_id=strategy_id,
            version=version_number,
            version_name=package.version_name,
            parent_version_id=parent_version_id,
            code_artifact_id=package.code_artifact_id,
            entrypoint=package.entrypoint,
            code_files=package.code_files,
            params_schema=package.params_schema,
            default_params=package.default_params,
            logic_summary=package.logic_summary,
            change_summary=change_summary,
            source_sdk_session_id=source_sdk_session_id,
            source_sdk_message_uuid=source_sdk_message_uuid,
            source_sdk_tool_use_id=source_sdk_tool_use_id,
            code_checksum=_checksum(package),
        )

    def _to_summary(self, strategy: StrategyRecord) -> StrategySummary:
        version = self._require_version(strategy.current_version_id or "")
        return StrategySummary(
            strategy_id=strategy.id,
            strategy_version_id=version.id,
            version=version.version,
            name=strategy.name,
            strategy_type=strategy.strategy_type,
            status=strategy.status,
            version_status=version.status,
            tags=strategy.tags,
            logic_summary=version.logic_summary,
            default_params=version.default_params,
            updated_at=strategy.updated_at,
        )

    def backtest_strategy(
        self,
        *,
        strategy_id: str,
        user_id: str,
        project_id: str,
        chat_session_id: str,
        config: StrategyBacktestConfig,
        engine: StrategyBacktestEngine,
    ) -> StrategyBacktestDetail:
        backtest = self._create_backtest(
            strategy_id=strategy_id,
            user_id=user_id,
            project_id=project_id,
            chat_session_id=chat_session_id,
            config=config,
        )
        return self._execute_backtest(backtest.id, engine=engine)

    def _create_backtest(
        self,
        *,
        strategy_id: str,
        user_id: str,
        project_id: str,
        chat_session_id: str,
        config: StrategyBacktestConfig,
    ) -> StrategyBacktestRecord:
        strategy = self._require_strategy(strategy_id)
        if strategy.status != StrategyStatus.ACTIVE:
            raise StrategyError("STRATEGY_NOT_ACTIVE", "Strategy is not active", 409)
        if strategy.current_version_id is None:
            raise StrategyError(
                "STRATEGY_VERSION_NOT_FOUND",
                "Strategy has no executable code",
                422,
            )
        version = self._require_version(strategy.current_version_id)

        merged_params = dict(version.default_params)
        merged_params.update(config.params)
        self._validate_backtest_params(version, merged_params)
        config = config.model_copy(update={"params": merged_params})
        backtest = StrategyBacktestRecord(
            id=_new_id("sbt"),
            user_id=user_id,
            project_id=project_id,
            chat_session_id=chat_session_id,
            strategy_id=strategy.id,
            strategy_version_id=version.id,
            status=StrategyBacktestStatus.PENDING,
            config=config,
            config_hash=_hash_backtest_config(config),
        )
        self.repository.add_backtest(backtest)
        return backtest

    def _execute_backtest(
        self,
        backtest_id: str,
        *,
        engine: StrategyBacktestEngine,
    ) -> StrategyBacktestDetail:
        backtest = self._require_backtest(backtest_id)
        if backtest.status in {
            StrategyBacktestStatus.RUNNING,
            StrategyBacktestStatus.SUCCEEDED,
            StrategyBacktestStatus.FAILED,
            StrategyBacktestStatus.CANCELED,
        }:
            return self._get_backtest_detail(backtest_id)

        version = self._require_version(backtest.strategy_version_id)
        started_at = utc_now()
        running = backtest.model_copy(
            update={
                "status": StrategyBacktestStatus.RUNNING,
                "execution_engine": engine.name,
                "started_at": started_at,
                "updated_at": started_at,
            }
        )
        self.repository.save_backtest(running)

        try:
            result = engine.execute(backtest=running, version=version)
        except StrategyBacktestError as exc:
            failed_at = utc_now()
            failed = running.model_copy(
                update={
                    "status": StrategyBacktestStatus.FAILED,
                    "failure_code": exc.error_code,
                    "failure_message": exc.message,
                    "failure_detail": exc.detail,
                    "completed_at": failed_at,
                    "updated_at": failed_at,
                }
            )
            self.repository.save_backtest(failed)
            return StrategyBacktestDetail(backtest=failed)

        completed_at = utc_now()
        succeeded = running.model_copy(
            update={
                "status": StrategyBacktestStatus.SUCCEEDED,
                "result_id": result.id,
                "completed_at": completed_at,
                "updated_at": completed_at,
            }
        )
        self.repository.save_backtest_result(result)
        self.repository.save_backtest(succeeded)
        return StrategyBacktestDetail(backtest=succeeded, result=result)

    def _get_backtest_detail(self, backtest_id: str) -> StrategyBacktestDetail:
        backtest = self._require_backtest(backtest_id)
        return StrategyBacktestDetail(
            backtest=backtest,
            result=self.repository.get_backtest_result(backtest_id),
        )

    def _require_strategy(self, strategy_id: str) -> StrategyRecord:
        strategy = self.repository.get_strategy(strategy_id)
        if strategy is None:
            raise StrategyError("STRATEGY_NOT_FOUND", "Strategy not found", 404)
        return strategy

    def _require_version(self, version_id: str) -> StrategyVersionRecord:
        version = self.repository.get_version(version_id)
        if version is None:
            raise StrategyError("STRATEGY_VERSION_NOT_FOUND", "Strategy version not found", 404)
        return version

    def _require_backtest(self, backtest_id: str) -> StrategyBacktestRecord:
        backtest = self.repository.get_backtest(backtest_id)
        if backtest is None:
            raise StrategyError("STRATEGY_BACKTEST_NOT_FOUND", "Strategy backtest not found", 404)
        return backtest

    def _validate_backtest_params(
        self,
        version: StrategyVersionRecord,
        params: dict[str, JsonValue],
    ) -> None:
        schema_keys = set(version.params_schema)
        param_keys = set(params)
        if schema_keys != param_keys:
            raise StrategyError(
                "STRATEGY_BACKTEST_PARAMS_INVALID",
                "Strategy backtest params must exactly match the strategy parameter schema",
                422,
            )
        for name, spec in version.params_schema.items():
            value = params[name]
            try:
                validate_param_value(name, value, spec)
            except ValueError as exc:
                raise StrategyError("STRATEGY_BACKTEST_PARAMS_INVALID", str(exc), 422) from exc


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


def _checksum(package: StrategyPackage) -> str:
    payload = package.model_dump_json()
    return sha256(payload.encode("utf-8")).hexdigest()


def _hash_backtest_config(config: StrategyBacktestConfig) -> str:
    payload = config.model_dump(mode="json")
    encoded = json.dumps(_normalize_json(payload), sort_keys=True, separators=(",", ":"))
    return f"sha256:{sha256(encoded.encode('utf-8')).hexdigest()}"


def _normalize_json(value: JsonValue) -> JsonValue:
    if isinstance(value, dict):
        return {key: _normalize_json(value[key]) for key in sorted(value)}
    if isinstance(value, list):
        return [_normalize_json(item) for item in value]
    return value


def _default_tags(package: StrategyPackage) -> list[str]:
    return _normalize_tags(["策略创建", package.strategy_type, *package.risk_notes[:1]])


def _normalize_tags(tags: list[str]) -> list[str]:
    normalized: list[str] = []
    for tag in tags:
        stripped = tag.strip()
        if stripped and stripped not in normalized:
            normalized.append(stripped[:32])
    return normalized


strategy_service = StrategyService(strategy_repository)
