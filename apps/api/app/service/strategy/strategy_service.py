from __future__ import annotations

from uuid import uuid4

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.model.strategy import StrategyRow, StrategyVersionRow
from app.schema.strategy import (
    StrategyCreate,
    StrategyCreateResult,
    StrategyCustomParameter,
    StrategyDetail,
    StrategyMode,
    StrategyRecord,
    StrategyStatus,
    StrategySummary,
    StrategyVersionCreate,
    StrategyVersionRecord,
    local_now,
)
from app.service import project as project_service
from app.service.project import ProjectNotFoundError
from app.service.strategy.validation import (
    StrategyAvailabilityError,
    validate_strategy_availability,
)

logger = get_logger(__name__)


class StrategyError(Exception):
    def __init__(
        self,
        error_code: str,
        message: str,
        status_code: int = 400,
        *,
        detail: dict[str, object] | None = None,
    ) -> None:
        super().__init__(message)
        self.error_code = error_code
        self.message = message
        self.status_code = status_code
        self.detail = detail or {}


class StrategyService:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def list_strategies(self, project_id: str) -> list[StrategySummary]:
        return [
            await self._to_summary(strategy)
            for strategy in await self._list_strategy_records(project_id)
        ]

    async def create_strategy(
        self,
        *,
        project_id: str,
        strategy_input: StrategyCreate,
    ) -> StrategyCreateResult:
        try:
            await project_service.require_project(self._db, project_id)
        except ProjectNotFoundError as exc:
            raise StrategyError("PROJECT_NOT_FOUND", "Project not found", 404) from exc

        strategy = StrategyRecord(
            id=_new_id("str"),
            project_id=project_id,
            name=strategy_input.name,
            description=strategy_input.description,
            tags=_default_tags(strategy_input),
        )
        version = self._build_version(
            strategy_id=strategy.id,
            version_number=1,
            version_input=strategy_input,
        )
        strategy.current_version_id = version.id

        await self._save_strategy(strategy)
        await self._save_version(version)
        logger.info(
            "strategy created",
            extra={
                "strategy_id": strategy.id,
                "strategy_version_id": version.id,
                "project_id": project_id,
                "strategy_name": strategy.name,
                "strategy_mode": version.strategy_mode.value,
                "version": version.version,
            },
        )
        return StrategyCreateResult(
            strategy_id=strategy.id,
        )

    async def get_strategy(self, strategy_id: str) -> StrategyDetail:
        strategy = await self._require_strategy(strategy_id)
        return StrategyDetail(strategy=strategy)

    async def create_strategy_version(
        self,
        strategy_id: str,
        *,
        version_input: StrategyVersionCreate,
    ) -> StrategyVersionRecord:
        strategy = await self._require_strategy(strategy_id)
        if strategy.status == StrategyStatus.DELETED:
            raise StrategyError("STRATEGY_DELETED", "Strategy is deleted", 409)

        version_number = await self._next_version_number(strategy_id)
        version = self._build_version(
            strategy_id=strategy_id,
            version_number=version_number,
            version_input=version_input,
        )
        updated_strategy = strategy.model_copy(
            update={
                "current_version_id": version.id,
                "updated_at": local_now(),
            }
        )

        self._db.add(_version_to_row(version))
        await self._db.merge(_strategy_to_row(updated_strategy))
        await self._db.commit()
        logger.info(
            "strategy version created",
            extra={
                "strategy_id": strategy_id,
                "strategy_version_id": version.id,
                "strategy_name": strategy.name,
                "strategy_mode": version.strategy_mode.value,
                "version": version.version,
            },
        )
        return version

    async def switch_current_version(
        self,
        strategy_id: str,
        *,
        version_id: str,
    ) -> StrategySummary:
        strategy = await self._require_strategy(strategy_id)
        if strategy.status == StrategyStatus.DELETED:
            raise StrategyError("STRATEGY_DELETED", "Strategy is deleted", 409)

        version = await self._require_version(version_id)
        if version.strategy_id != strategy_id:
            raise StrategyError(
                "STRATEGY_VERSION_MISMATCH",
                "Strategy version does not belong to this strategy",
                400,
            )

        updated_strategy = strategy.model_copy(
            update={
                "current_version_id": version.id,
                "updated_at": local_now(),
            }
        )
        await self._save_strategy(updated_strategy)
        return await self._to_summary(updated_strategy)

    async def update_strategy_metadata(
        self,
        strategy_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        tags: list[str] | None = None,
        status: StrategyStatus | None = None,
    ) -> StrategyRecord:
        strategy = await self._require_strategy(strategy_id)
        if strategy.status == StrategyStatus.DELETED:
            raise StrategyError("STRATEGY_DELETED", "Strategy is deleted", 409)

        update_data: dict[str, object] = {"updated_at": local_now()}
        if name is not None:
            update_data["name"] = name
        if description is not None:
            update_data["description"] = description
        if tags is not None:
            update_data["tags"] = _normalize_tags(tags)
        if status is not None:
            update_data["status"] = status

        strategy = strategy.model_copy(update=update_data)
        await self._save_strategy(strategy)
        return strategy

    def _build_version(
        self,
        *,
        strategy_id: str,
        version_number: int,
        version_input: StrategyVersionCreate,
    ) -> StrategyVersionRecord:
        custom_params = _validate_version_source(version_input)
        return StrategyVersionRecord(
            id=_new_id("stv"),
            strategy_id=strategy_id,
            version=version_number,
            source_code=version_input.source_code,
            strategy_mode=version_input.strategy_mode,
            custom_params=custom_params,
        )

    async def _to_summary(self, strategy: StrategyRecord) -> StrategySummary:
        version = await self._require_version(strategy.current_version_id or "")
        return StrategySummary(
            strategy_id=strategy.id,
            strategy_version_id=version.id,
            version=version.version,
            name=strategy.name,
            status=strategy.status,
            tags=strategy.tags,
            strategy_mode=version.strategy_mode,
            custom_params=version.custom_params,
            updated_at=strategy.updated_at,
        )

    async def _require_strategy(self, strategy_id: str) -> StrategyRecord:
        strategy = await self._get_strategy_record(strategy_id)
        if strategy is None:
            raise StrategyError("STRATEGY_NOT_FOUND", "Strategy not found", 404)
        return strategy

    async def _require_version(self, version_id: str) -> StrategyVersionRecord:
        version = await self._get_version(version_id)
        if version is None:
            raise StrategyError("STRATEGY_VERSION_NOT_FOUND", "Strategy version not found", 404)
        return version

    async def get_version(self, version_id: str) -> StrategyVersionRecord:
        return await self._require_version(version_id)

    async def clear(self) -> None:
        await self._db.execute(delete(StrategyVersionRow))
        await self._db.execute(delete(StrategyRow))
        await self._db.commit()

    async def _save_strategy(self, strategy: StrategyRecord) -> None:
        await self._db.merge(_strategy_to_row(strategy))
        await self._db.commit()

    async def _get_strategy_record(self, strategy_id: str) -> StrategyRecord | None:
        row = await self._db.get(StrategyRow, strategy_id)
        return _strategy_from_row(row) if row is not None else None

    async def _list_strategy_records(self, project_id: str) -> list[StrategyRecord]:
        result = await self._db.scalars(
            select(StrategyRow)
            .where(
                StrategyRow.project_id == project_id,
                StrategyRow.status != StrategyStatus.DELETED.value,
            )
            .order_by(StrategyRow.updated_at.desc())
        )
        return [_strategy_from_row(row) for row in result.all()]

    async def _save_version(self, version: StrategyVersionRecord) -> None:
        await self._db.merge(_version_to_row(version))
        await self._db.commit()

    async def _get_version(self, version_id: str) -> StrategyVersionRecord | None:
        row = await self._db.get(StrategyVersionRow, version_id)
        return _version_from_row(row) if row is not None else None

    async def list_versions(self, strategy_id: str) -> list[StrategyVersionRecord]:
        result = await self._db.scalars(
            select(StrategyVersionRow)
            .where(StrategyVersionRow.strategy_id == strategy_id)
            .order_by(StrategyVersionRow.version.asc())
        )
        return [_version_from_row(row) for row in result.all()]

    async def _next_version_number(self, strategy_id: str) -> int:
        result = await self._db.scalar(
            select(func.max(StrategyVersionRow.version)).where(
                StrategyVersionRow.strategy_id == strategy_id
            )
        )
        return (result or 0) + 1


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


def _validate_version_source(
    version_input: StrategyVersionCreate,
) -> list[StrategyCustomParameter]:
    try:
        spec = validate_strategy_availability(
            version_input.source_code,
            strategy_mode=version_input.strategy_mode,
        )
    except StrategyAvailabilityError as exc:
        raise StrategyError(
            _availability_error_code(exc),
            exc.message,
            422,
            detail={"issues": [issue.model_dump(mode="json") for issue in exc.issues]},
        ) from exc
    if spec.param_source != "none":
        return spec.custom_params
    return []


def _availability_error_code(error: StrategyAvailabilityError) -> str:
    if len(error.issues) == 1:
        return error.issues[0].code
    return "STRATEGY_AVAILABILITY_CHECK_FAILED"


def _default_tags(strategy: StrategyCreate) -> list[str]:
    return _normalize_tags(["策略创建", *strategy.risk_notes[:1]])


def _normalize_tags(tags: list[str]) -> list[str]:
    normalized: list[str] = []
    for tag in tags:
        stripped = tag.strip()
        if stripped and stripped not in normalized:
            normalized.append(stripped[:32])
    return normalized


def _strategy_to_row(strategy: StrategyRecord) -> StrategyRow:
    return StrategyRow(
        id=strategy.id,
        project_id=strategy.project_id,
        name=strategy.name,
        description=strategy.description,
        tags_json=list(strategy.tags),
        current_version_id=strategy.current_version_id,
        status=strategy.status.value,
        created_at=strategy.created_at,
        updated_at=strategy.updated_at,
    )


def _strategy_from_row(row: StrategyRow) -> StrategyRecord:
    return StrategyRecord(
        id=row.id,
        project_id=row.project_id,
        name=row.name,
        description=row.description,
        tags=list(row.tags_json) if isinstance(row.tags_json, list) else [],
        current_version_id=row.current_version_id,
        status=StrategyStatus(row.status),
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def _version_to_row(version: StrategyVersionRecord) -> StrategyVersionRow:
    return StrategyVersionRow(
        id=version.id,
        strategy_id=version.strategy_id,
        version=version.version,
        source_code=version.source_code,
        strategy_mode=version.strategy_mode.value,
        custom_params_json=[param.model_dump(mode="json") for param in version.custom_params],
        created_at=version.created_at,
    )


def _version_from_row(row: StrategyVersionRow) -> StrategyVersionRecord:
    return StrategyVersionRecord(
        id=row.id,
        strategy_id=row.strategy_id,
        version=row.version,
        source_code=row.source_code,
        strategy_mode=StrategyMode(getattr(row, "strategy_mode", StrategyMode.SINGLE_SYMBOL.value)),
        custom_params=[
            StrategyCustomParameter.model_validate(value)
            for value in _list_payload(row.custom_params_json)
        ],
        created_at=row.created_at,
    )


def _list_payload(payload: object) -> list[object]:
    return payload if isinstance(payload, list) else []


def _service(db: AsyncSession) -> StrategyService:
    return StrategyService(db)


async def list_strategies(
    db: AsyncSession,
    *,
    project_id: str,
) -> list[StrategySummary]:
    return await _service(db).list_strategies(project_id=project_id)


async def create_strategy(
    db: AsyncSession,
    *,
    project_id: str,
    strategy_input: StrategyCreate,
) -> StrategyCreateResult:
    return await _service(db).create_strategy(
        project_id=project_id,
        strategy_input=strategy_input,
    )


async def get_strategy(db: AsyncSession, strategy_id: str) -> StrategyDetail:
    return await _service(db).get_strategy(strategy_id)


async def create_strategy_version(
    db: AsyncSession,
    *,
    strategy_id: str,
    version_input: StrategyVersionCreate,
) -> StrategyVersionRecord:
    return await _service(db).create_strategy_version(
        strategy_id,
        version_input=version_input,
    )


async def list_versions(db: AsyncSession, strategy_id: str) -> list[StrategyVersionRecord]:
    return await _service(db).list_versions(strategy_id)


async def get_version(db: AsyncSession, version_id: str) -> StrategyVersionRecord:
    return await _service(db).get_version(version_id)


async def switch_current_version(
    db: AsyncSession,
    strategy_id: str,
    *,
    version_id: str,
) -> StrategySummary:
    return await _service(db).switch_current_version(strategy_id, version_id=version_id)


async def update_strategy_metadata(
    db: AsyncSession,
    strategy_id: str,
    *,
    name: str | None = None,
    description: str | None = None,
    tags: list[str] | None = None,
    status: StrategyStatus | None = None,
) -> StrategyRecord:
    return await _service(db).update_strategy_metadata(
        strategy_id,
        name=name,
        description=description,
        tags=tags,
        status=status,
    )
