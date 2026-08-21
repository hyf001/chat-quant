from __future__ import annotations

import json
from datetime import datetime
from typing import Any
from uuid import uuid4

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.model.job_runtime import JobInstanceRow, JobSchedulerRow
from app.model.strategy import StrategyDeploymentRow, StrategySignalRow
from app.schema.strategy import (
    JsonValue,
    StrategyDeploymentCreate,
    StrategyDeploymentMode,
    StrategyDeploymentRecord,
    StrategyDeploymentUpdate,
    StrategySignalAction,
    StrategySignalActionType,
    StrategySignalRecord,
    StrategySignalStatus,
    StrategyVersionRecord,
    local_now,
    validate_param_value,
)
from app.service import project as project_service
from app.service.job_runtime import (
    JobRef,
    JobRuntimeInstanceService,
    JobRuntimeScheduleService,
    TriggerType,
)
from app.service.project import ProjectNotFoundError
from app.service.strategy.strategy_service import StrategyError, get_version

STRATEGY_DEPLOYMENT_TICK_JOB_TYPE = "strategy_deployment_tick"


class StrategyDeploymentError(Exception):
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


class StrategyDeploymentService:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def create_deployment(
        self,
        deployment_input: StrategyDeploymentCreate,
    ) -> StrategyDeploymentRecord:
        try:
            await project_service.require_project(self._db, deployment_input.project_id)
        except ProjectNotFoundError as exc:
            raise StrategyDeploymentError("PROJECT_NOT_FOUND", "Project not found", 404) from exc

        version = await _require_strategy_version(
            self._db,
            deployment_input.strategy_version_id,
            strategy_id=deployment_input.strategy_id,
        )
        now = local_now()
        params = _deployment_param_values(version, deployment_input.params)
        deployment = StrategyDeploymentRecord(
            id=_new_id("sdep"),
            project_id=deployment_input.project_id,
            strategy_id=deployment_input.strategy_id,
            strategy_version_id=version.id,
            name=deployment_input.name,
            mode=deployment_input.mode,
            symbols=deployment_input.symbols,
            lookback_bars=deployment_input.lookback_bars,
            params=params,
            broker_id=deployment_input.broker_id,
            requires_manual_confirm=deployment_input.requires_manual_confirm,
            risk_config=deployment_input.risk_config,
            state={},
            created_at=now,
            updated_at=now,
        )
        self._db.add(_deployment_to_row(deployment))
        await self._db.commit()
        return deployment

    async def list_deployments(
        self,
        *,
        project_id: str,
        strategy_id: str | None = None,
    ) -> list[StrategyDeploymentRecord]:
        stmt = (
            select(StrategyDeploymentRow)
            .where(StrategyDeploymentRow.project_id == project_id)
            .order_by(StrategyDeploymentRow.updated_at.desc())
        )
        if strategy_id is not None:
            stmt = stmt.where(StrategyDeploymentRow.strategy_id == strategy_id)
        result = await self._db.scalars(stmt)
        rows = result.all()
        schedulers = await _schedulers_by_deployment_id(self._db, [row.id for row in rows])
        return [_deployment_from_row(row, schedulers.get(row.id)) for row in rows]

    async def get_deployment(self, deployment_id: str) -> StrategyDeploymentRecord:
        row = await self._db.get(StrategyDeploymentRow, deployment_id)
        if row is None:
            raise StrategyDeploymentError(
                "STRATEGY_DEPLOYMENT_NOT_FOUND",
                "Strategy deployment not found",
                404,
            )
        scheduler = await _scheduler_for_deployment(self._db, deployment_id)
        return _deployment_from_row(row, scheduler)

    async def update_deployment(
        self,
        deployment_id: str,
        deployment_update: StrategyDeploymentUpdate,
    ) -> StrategyDeploymentRecord:
        current = await self.get_deployment(deployment_id)
        update_data = deployment_update.model_dump(exclude_unset=True)
        version: StrategyVersionRecord | None = None
        if "strategy_version_id" in update_data:
            version = await _require_strategy_version(
                self._db,
                str(update_data["strategy_version_id"]),
                strategy_id=current.strategy_id,
            )
            update_data["strategy_version_id"] = version.id
        if "params" in update_data or version is not None:
            version = version or await _require_strategy_version(
                self._db,
                current.strategy_version_id,
                strategy_id=current.strategy_id,
            )
            overrides = update_data.get("params", current.params)
            update_data["params"] = _deployment_param_values(version, _json_dict(overrides))
        if "state" in update_data:
            update_data["state"] = _json_dict(update_data["state"])
        updated = current.model_copy(
            update={
                **update_data,
                "updated_at": local_now(),
            }
        )
        if updated.mode != StrategyDeploymentMode.SIGNAL and not updated.broker_id:
            raise StrategyDeploymentError(
                "STRATEGY_DEPLOYMENT_BROKER_REQUIRED",
                "broker_id is required for paper/live deployments",
                422,
            )
        await self._db.merge(_deployment_to_row(updated))
        await self._db.commit()
        return await self.get_deployment(deployment_id)

    async def delete_deployment(
        self,
        deployment_id: str,
        *,
        instance_service: JobRuntimeInstanceService | None = None,
        schedule_service: JobRuntimeScheduleService | None = None,
    ) -> StrategyDeploymentRecord:
        deployment = await self.get_deployment(deployment_id)
        job_ref = _deployment_job_ref(deployment_id)

        signal_result = await self._db.scalars(
            select(StrategySignalRow).where(StrategySignalRow.deployment_id == deployment_id)
        )
        for signal in signal_result.all():
            await self._db.delete(signal)
        await self._db.commit()

        schedule_service = schedule_service or JobRuntimeScheduleService()
        await schedule_service.delete_scheduler(self._db, job_ref=job_ref)

        instance_service = instance_service or JobRuntimeInstanceService()
        await instance_service.delete_job_instances(self._db, job_ref=job_ref)

        row = await self._db.get(StrategyDeploymentRow, deployment_id)
        if row is not None:
            await self._db.delete(row)
            await self._db.commit()
        return deployment

    async def upsert_schedule(
        self,
        deployment_id: str,
        *,
        cron: str,
        schedule_service: JobRuntimeScheduleService | None = None,
    ) -> StrategyDeploymentRecord:
        await self.get_deployment(deployment_id)
        schedule_service = schedule_service or JobRuntimeScheduleService()
        try:
            await schedule_service.upsert_scheduler(
                self._db,
                job_ref=_deployment_job_ref(deployment_id),
                cron=cron,
                payload={},
            )
        except ValueError as exc:
            raise StrategyDeploymentError(
                "INVALID_STRATEGY_DEPLOYMENT_SCHEDULE",
                str(exc),
                422,
            ) from exc
        return await self.get_deployment(deployment_id)

    async def delete_schedule(
        self,
        deployment_id: str,
        *,
        schedule_service: JobRuntimeScheduleService | None = None,
    ) -> StrategyDeploymentRecord:
        await self.get_deployment(deployment_id)
        schedule_service = schedule_service or JobRuntimeScheduleService()
        await schedule_service.delete_scheduler(
            self._db,
            job_ref=_deployment_job_ref(deployment_id),
        )
        return await self.get_deployment(deployment_id)

    async def save_signal(
        self,
        *,
        deployment_id: str,
        job_instance_id: str | None,
        strategy_version_id: str,
        signal_datetime: datetime,
        action: StrategySignalAction | dict[str, Any],
        status: StrategySignalStatus = StrategySignalStatus.GENERATED,
        reason: str | None = None,
    ) -> StrategySignalRecord:
        signal = StrategySignalRecord(
            id=_new_id("ssig"),
            deployment_id=deployment_id,
            job_instance_id=job_instance_id,
            strategy_version_id=strategy_version_id,
            signal_datetime=signal_datetime,
            action=_signal_action_payload(action),
            status=status,
            reason=reason,
            created_at=local_now(),
        )
        self._db.add(_signal_to_row(signal))
        await self._db.commit()
        return signal

    async def list_signals(
        self,
        *,
        deployment_id: str,
        action: StrategySignalActionType | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[StrategySignalRecord]:
        action_expr = StrategySignalRow.action_json["action"].as_string()
        stmt = select(StrategySignalRow).where(StrategySignalRow.deployment_id == deployment_id)
        if action is not None:
            stmt = stmt.where(action_expr == action.value)
        result = await self._db.scalars(
            stmt
            .order_by(
                StrategySignalRow.signal_datetime.desc(),
                StrategySignalRow.created_at.desc(),
            )
            .offset(offset)
            .limit(limit)
        )
        return [_signal_from_row(row) for row in result.all()]

    async def count_signals(
        self,
        *,
        deployment_id: str,
        action: StrategySignalActionType | None = None,
    ) -> int:
        action_expr = StrategySignalRow.action_json["action"].as_string()
        stmt = select(func.count()).select_from(StrategySignalRow).where(
            StrategySignalRow.deployment_id == deployment_id
        )
        if action is not None:
            stmt = stmt.where(action_expr == action.value)
        return int(await self._db.scalar(stmt) or 0)

    async def count_signals_by_action(
        self,
        *,
        deployment_id: str,
    ) -> dict[StrategySignalActionType, int]:
        action_expr = StrategySignalRow.action_json["action"].as_string()
        result = await self._db.execute(
            select(action_expr, func.count())
            .select_from(StrategySignalRow)
            .where(StrategySignalRow.deployment_id == deployment_id)
            .group_by(action_expr)
        )
        counts: dict[StrategySignalActionType, int] = {}
        for raw_action, count in result.all():
            try:
                action = StrategySignalActionType(raw_action)
            except ValueError:
                continue
            counts[action] = int(count)
        return counts

    async def save_state(self, deployment_id: str, state: dict[str, Any]) -> None:
        deployment = await self.get_deployment(deployment_id)
        updated = deployment.model_copy(
            update={
                "state": _json_dict(state),
                "updated_at": local_now(),
            }
        )
        await self._db.merge(_deployment_to_row(updated))
        await self._db.commit()

    async def trigger_run(
        self,
        deployment_id: str,
        *,
        scheduled_for: datetime | None = None,
        payload: dict[str, Any] | None = None,
        trigger_key: str | None = None,
        instance_service: JobRuntimeInstanceService | None = None,
    ) -> JobInstanceRow:
        deployment = await self.get_deployment(deployment_id)
        scheduled_for = scheduled_for or local_now()
        trigger_key = trigger_key or f"manual:{scheduled_for.isoformat()}:{uuid4().hex[:8]}"
        instance_service = instance_service or JobRuntimeInstanceService()
        return await instance_service.create_job_instance(
            self._db,
            job_ref=JobRef(
                job_type=STRATEGY_DEPLOYMENT_TICK_JOB_TYPE,
                job_id=deployment.id,
            ),
            trigger_type=TriggerType.MANUAL,
            trigger_key=trigger_key,
            scheduled_for=scheduled_for,
            payload=dict(payload or {}),
        )


async def create_deployment(
    db: AsyncSession,
    deployment_input: StrategyDeploymentCreate,
) -> StrategyDeploymentRecord:
    return await StrategyDeploymentService(db).create_deployment(deployment_input)


async def list_deployments(
    db: AsyncSession,
    *,
    project_id: str,
    strategy_id: str | None = None,
) -> list[StrategyDeploymentRecord]:
    return await StrategyDeploymentService(db).list_deployments(
        project_id=project_id,
        strategy_id=strategy_id,
    )


async def get_deployment(
    db: AsyncSession,
    deployment_id: str,
) -> StrategyDeploymentRecord:
    return await StrategyDeploymentService(db).get_deployment(deployment_id)


async def update_deployment(
    db: AsyncSession,
    deployment_id: str,
    deployment_update: StrategyDeploymentUpdate,
) -> StrategyDeploymentRecord:
    return await StrategyDeploymentService(db).update_deployment(deployment_id, deployment_update)


async def delete_deployment(
    db: AsyncSession,
    deployment_id: str,
) -> StrategyDeploymentRecord:
    return await StrategyDeploymentService(db).delete_deployment(deployment_id)


async def upsert_strategy_deployment_schedule(
    db: AsyncSession,
    deployment_id: str,
    *,
    cron: str,
) -> StrategyDeploymentRecord:
    return await StrategyDeploymentService(db).upsert_schedule(deployment_id, cron=cron)


async def delete_strategy_deployment_schedule(
    db: AsyncSession,
    deployment_id: str,
) -> StrategyDeploymentRecord:
    return await StrategyDeploymentService(db).delete_schedule(deployment_id)


async def save_strategy_signal(
    db: AsyncSession,
    *,
    deployment_id: str,
    job_instance_id: str | None,
    strategy_version_id: str,
    signal_datetime: datetime,
    action: StrategySignalAction | dict[str, Any],
    status: StrategySignalStatus = StrategySignalStatus.GENERATED,
    reason: str | None = None,
) -> StrategySignalRecord:
    return await StrategyDeploymentService(db).save_signal(
        deployment_id=deployment_id,
        job_instance_id=job_instance_id,
        strategy_version_id=strategy_version_id,
        signal_datetime=signal_datetime,
        action=action,
        status=status,
        reason=reason,
    )


async def list_strategy_signals(
    db: AsyncSession,
    *,
    deployment_id: str,
    action: StrategySignalActionType | None = None,
    limit: int = 100,
    offset: int = 0,
) -> list[StrategySignalRecord]:
    return await StrategyDeploymentService(db).list_signals(
        deployment_id=deployment_id,
        action=action,
        limit=limit,
        offset=offset,
    )


async def count_strategy_signals(
    db: AsyncSession,
    *,
    deployment_id: str,
    action: StrategySignalActionType | None = None,
) -> int:
    return await StrategyDeploymentService(db).count_signals(
        deployment_id=deployment_id,
        action=action,
    )


async def count_strategy_signals_by_action(
    db: AsyncSession,
    *,
    deployment_id: str,
) -> dict[StrategySignalActionType, int]:
    return await StrategyDeploymentService(db).count_signals_by_action(
        deployment_id=deployment_id,
    )


async def save_strategy_state(
    db: AsyncSession,
    *,
    deployment_id: str,
    state: dict[str, Any],
) -> None:
    await StrategyDeploymentService(db).save_state(deployment_id, state)


async def _require_strategy_version(
    db: AsyncSession,
    version_id: str,
    *,
    strategy_id: str,
) -> StrategyVersionRecord:
    try:
        version = await get_version(db, version_id)
    except StrategyError as exc:
        raise StrategyDeploymentError(exc.error_code, exc.message, exc.status_code) from exc
    if version.strategy_id != strategy_id:
        raise StrategyDeploymentError(
            "STRATEGY_VERSION_MISMATCH",
            "Strategy version does not belong to this strategy",
            400,
        )
    return version


def _deployment_to_row(deployment: StrategyDeploymentRecord) -> StrategyDeploymentRow:
    return StrategyDeploymentRow(
        id=deployment.id,
        project_id=deployment.project_id,
        strategy_id=deployment.strategy_id,
        strategy_version_id=deployment.strategy_version_id,
        name=deployment.name,
        mode=deployment.mode.value,
        symbols_json=list(deployment.symbols),
        lookback_bars=deployment.lookback_bars,
        params_json=dict(deployment.params),
        broker_id=deployment.broker_id,
        requires_manual_confirm=deployment.requires_manual_confirm,
        risk_config_json=dict(deployment.risk_config),
        state_json=dict(deployment.state),
        created_at=deployment.created_at,
        updated_at=deployment.updated_at,
    )


def _deployment_from_row(
    row: StrategyDeploymentRow,
    scheduler: JobSchedulerRow | None = None,
) -> StrategyDeploymentRecord:
    return StrategyDeploymentRecord(
        id=row.id,
        project_id=row.project_id,
        strategy_id=row.strategy_id,
        strategy_version_id=row.strategy_version_id,
        name=row.name,
        mode=StrategyDeploymentMode(row.mode),
        scheduled=scheduler is not None,
        schedule_cron=scheduler.cron if scheduler is not None else None,
        scheduler_id=scheduler.id if scheduler is not None else None,
        symbols=_json_list(row.symbols_json),
        lookback_bars=row.lookback_bars,
        params=_json_dict(row.params_json),
        broker_id=row.broker_id,
        requires_manual_confirm=row.requires_manual_confirm,
        risk_config=_json_dict(row.risk_config_json),
        state=_json_dict(row.state_json),
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


async def _scheduler_for_deployment(
    db: AsyncSession,
    deployment_id: str,
) -> JobSchedulerRow | None:
    return await JobRuntimeScheduleService().get_scheduler(
        db,
        job_ref=_deployment_job_ref(deployment_id),
    )


async def _schedulers_by_deployment_id(
    db: AsyncSession,
    deployment_ids: list[str],
) -> dict[str, JobSchedulerRow]:
    if not deployment_ids:
        return {}
    result = await db.scalars(
        select(JobSchedulerRow)
        .where(
            JobSchedulerRow.job_type == STRATEGY_DEPLOYMENT_TICK_JOB_TYPE,
            JobSchedulerRow.job_id.in_(deployment_ids),
        )
        .order_by(JobSchedulerRow.id.asc())
    )
    return {scheduler.job_id: scheduler for scheduler in result.all()}


def _deployment_job_ref(deployment_id: str) -> JobRef:
    return JobRef(
        job_type=STRATEGY_DEPLOYMENT_TICK_JOB_TYPE,
        job_id=deployment_id,
    )


def _signal_to_row(signal: StrategySignalRecord) -> StrategySignalRow:
    return StrategySignalRow(
        id=signal.id,
        deployment_id=signal.deployment_id,
        job_instance_id=signal.job_instance_id,
        strategy_version_id=signal.strategy_version_id,
        signal_datetime=signal.signal_datetime,
        action_json=_signal_json_dict(signal.action),
        status=signal.status.value,
        reason=signal.reason,
        created_at=signal.created_at,
    )


def _signal_from_row(row: StrategySignalRow) -> StrategySignalRecord:
    return StrategySignalRecord(
        id=row.id,
        deployment_id=row.deployment_id,
        job_instance_id=row.job_instance_id,
        strategy_version_id=row.strategy_version_id,
        signal_datetime=row.signal_datetime,
        action=_signal_json_dict(row.action_json),
        status=StrategySignalStatus(row.status),
        reason=row.reason,
        created_at=row.created_at,
    )


def _deployment_param_values(
    version: StrategyVersionRecord,
    overrides: dict[str, JsonValue],
) -> dict[str, Any]:
    schema_keys = {param.name_en for param in version.custom_params}
    if not set(overrides).issubset(schema_keys):
        raise StrategyDeploymentError(
            "STRATEGY_DEPLOYMENT_PARAMS_INVALID",
            "Strategy deployment params must be declared by the strategy custom parameters",
            422,
        )
    params: dict[str, Any] = {param.name_en: param.default for param in version.custom_params}
    params.update(overrides)
    for param in version.custom_params:
        try:
            validate_param_value(param.name_en, params[param.name_en], param.type)
        except ValueError as exc:
            raise StrategyDeploymentError(
                "STRATEGY_DEPLOYMENT_PARAMS_INVALID",
                str(exc),
                422,
            ) from exc
    return params


def _json_dict(value: object) -> dict[str, JsonValue]:
    if not isinstance(value, dict):
        return {}
    return json.loads(json.dumps(value))


def _signal_action(value: StrategySignalAction | object) -> StrategySignalAction:
    if isinstance(value, StrategySignalAction):
        return value
    return StrategySignalAction.model_validate(_json_dict(value))


def _signal_action_payload(value: StrategySignalAction | object) -> dict[str, JsonValue]:
    if isinstance(value, StrategySignalAction):
        return value.model_dump(mode="json", exclude_none=True)
    return _signal_json_dict(value)


def _signal_json_dict(value: object) -> dict[str, JsonValue]:
    if not isinstance(value, dict):
        return {}
    return json.loads(json.dumps(value, default=str))


def _json_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if isinstance(item, str) and item]


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"
