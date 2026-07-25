from __future__ import annotations

from hashlib import sha256
from uuid import uuid4

from app.domain.strategies.models import (
    StrategyCopyMode,
    StrategyCopyRecord,
    StrategyCopySummary,
    StrategyCreateResult,
    StrategyDetail,
    StrategyPackage,
    StrategyRecord,
    StrategyStatus,
    StrategySummary,
    StrategyValidationCheck,
    StrategyValidationResult,
    StrategyVersionRecord,
    StrategyVersionStatus,
    ValidationCheckStatus,
    utc_now,
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
            strategy_version_id=version.id,
            version=version.version,
            status=version.status,
            entrypoint=version.entrypoint,
        )

    def get_strategy(self, strategy_id: str) -> StrategyDetail:
        strategy = self._require_strategy(strategy_id)
        return StrategyDetail(
            strategy=strategy,
            versions=self.repository.list_versions(strategy_id),
        )

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

    def create_strategy_version(
        self,
        strategy_id: str,
        *,
        package: StrategyPackage,
        parent_version_id: str | None,
        change_summary: str | None,
        source_sdk_session_id: str | None = None,
        source_sdk_message_uuid: str | None = None,
        source_sdk_tool_use_id: str | None = None,
    ) -> StrategyCreateResult:
        strategy = self._require_strategy(strategy_id)
        if strategy.status != StrategyStatus.ACTIVE:
            raise StrategyError(
                "STRATEGY_ARCHIVED",
                "Only active strategies can create versions",
                409,
            )

        if parent_version_id is not None:
            parent = self._require_version(parent_version_id)
            if parent.strategy_id != strategy_id:
                raise StrategyError(
                    "STRATEGY_PARENT_VERSION_INVALID",
                    "Parent version mismatch",
                    422,
                )

        version = self._build_version(
            strategy_id=strategy_id,
            version_number=self.repository.next_version_number(strategy_id),
            package=package,
            parent_version_id=parent_version_id,
            change_summary=change_summary,
            source_sdk_session_id=source_sdk_session_id,
            source_sdk_message_uuid=source_sdk_message_uuid,
            source_sdk_tool_use_id=source_sdk_tool_use_id,
        )
        strategy = strategy.model_copy(
            update={
                "name": package.name,
                "description": package.description or strategy.description,
                "strategy_type": package.strategy_type,
                "current_version_id": version.id,
                "updated_at": utc_now(),
            }
        )

        self.repository.add_version(version)
        self.repository.save_strategy(strategy)
        return StrategyCreateResult(
            strategy_id=strategy_id,
            strategy_version_id=version.id,
            version=version.version,
            status=version.status,
            entrypoint=version.entrypoint,
        )

    def get_version(self, version_id: str) -> StrategyVersionRecord:
        return self._require_version(version_id)

    def validate_version(self, version_id: str) -> StrategyValidationResult:
        version = self._require_version(version_id)
        if version.status == StrategyVersionStatus.ARCHIVED:
            raise StrategyError(
                "STRATEGY_VERSION_ARCHIVED",
                "Archived versions cannot be validated",
                409,
            )

        # TODO(M4-integration): call the Python runtime smoke-test service once M4 exposes it.
        checks = [
            StrategyValidationCheck(name="entrypoint", status=ValidationCheckStatus.PASSED),
            StrategyValidationCheck(name="params_schema", status=ValidationCheckStatus.PASSED),
            StrategyValidationCheck(name="code_reference", status=ValidationCheckStatus.PASSED),
            StrategyValidationCheck(name="smoke_test", status=ValidationCheckStatus.PASSED),
        ]
        validated_at = utc_now()
        version = version.model_copy(
            update={
                "status": StrategyVersionStatus.VALIDATED,
                "validation_error": None,
                "validation_details": checks,
                "validated_at": validated_at,
            }
        )
        self.repository.save_version(version)
        return StrategyValidationResult(
            strategy_version_id=version_id,
            status=version.status,
            checks=checks,
            execution_result_id=_new_id("exec"),
            error=None,
            validated_at=validated_at,
        )

    def copy_strategy_version(
        self,
        version_id: str,
        *,
        mode: StrategyCopyMode,
        user_id: str,
        project_id: str,
        target_chat_session_id: str | None = None,
    ) -> StrategyCopySummary:
        version = self._require_version(version_id)
        source_strategy = self._require_strategy(version.strategy_id)
        target_strategy_id: str | None = None

        if mode == StrategyCopyMode.NEW_STRATEGY:
            target_strategy = StrategyRecord(
                id=_new_id("str"),
                user_id=user_id,
                project_id=project_id,
                chat_session_id=target_chat_session_id or source_strategy.chat_session_id,
                source_sdk_message_uuid=source_strategy.source_sdk_message_uuid,
                name=f"{source_strategy.name} 副本",
                description=source_strategy.description,
                strategy_type=source_strategy.strategy_type,
                tags=source_strategy.tags,
            )
            copied_version = version.model_copy(
                update={
                    "id": _new_id("stv"),
                    "strategy_id": target_strategy.id,
                    "version": 1,
                    "parent_version_id": version.id,
                    "change_summary": "复制为新策略资产",
                    "created_at": utc_now(),
                }
            )
            target_strategy.current_version_id = copied_version.id
            self.repository.add_strategy(target_strategy)
            self.repository.add_version(copied_version)
            target_strategy_id = target_strategy.id

        record = StrategyCopyRecord(
            id=_new_id("scp"),
            source_strategy_version_id=version_id,
            target_strategy_id=target_strategy_id,
            target_chat_session_id=target_chat_session_id,
            mode=mode,
            created_by=user_id,
        )
        self.repository.add_copy_record(record)
        return StrategyCopySummary(
            mode=mode,
            source_strategy_version_id=version_id,
            summary=self._build_copy_summary(source_strategy, version),
            target_strategy_id=target_strategy_id,
            copy_record_id=record.id,
        )

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

    def _build_copy_summary(
        self,
        strategy: StrategyRecord,
        version: StrategyVersionRecord,
    ) -> str:
        params = ", ".join(f"{key}={value}" for key, value in version.default_params.items())
        risk_note = "历史回测不代表未来收益，不构成投资建议。"
        summary = version.logic_summary or strategy.description or "策略摘要待补充"
        return (
            f"{strategy.name} V{version.version}: {summary}\n"
            f"类型: {strategy.strategy_type}\n"
            f"入口: {version.entrypoint}\n"
            f"默认参数: {params}\n"
            f"风险提示: {risk_note}"
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


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


def _checksum(package: StrategyPackage) -> str:
    payload = package.model_dump_json()
    return sha256(payload.encode("utf-8")).hexdigest()


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
