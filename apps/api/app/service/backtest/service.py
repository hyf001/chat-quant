from __future__ import annotations

from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.db.payloads import StrategyBacktestPayload
from app.model.strategy import StrategyBacktestRow
from app.schema.backtest import (
    JsonValue,
    StrategyBacktestConfig,
    StrategyBacktestDetail,
    StrategyBacktestRecord,
    StrategyBacktestResultRecord,
    StrategyBacktestStatus,
)
from app.schema.strategy import (
    StrategyCustomParameter,
    StrategyStatus,
    StrategyVersionRecord,
    local_now,
    validate_param_value,
)
from app.service.backtest.backtrader import BacktraderStrategyBacktestEngine
from app.service.backtest.execution import StrategyBacktestEngine, StrategyBacktestError
from app.service.strategy.strategy_service import StrategyError, StrategyService

logger = get_logger(__name__)


class BacktestError(Exception):
    def __init__(self, error_code: str, message: str, status_code: int = 400) -> None:
        super().__init__(message)
        self.error_code = error_code
        self.message = message
        self.status_code = status_code


class BacktestService:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db
        self._strategies = StrategyService(db)

    async def backtest_strategy(
        self,
        *,
        strategy_id: str,
        project_id: str,
        config: StrategyBacktestConfig,
        engine: StrategyBacktestEngine | None = None,
        strategy_version_id: str | None = None,
    ) -> StrategyBacktestDetail:
        backtest = await self._create_backtest(
            strategy_id=strategy_id,
            project_id=project_id,
            config=config,
            strategy_version_id=strategy_version_id,
        )
        return await self._execute_backtest(
            backtest.id,
            engine=engine or BacktraderStrategyBacktestEngine(),
        )

    async def list_records(
        self,
        *,
        strategy_version_id: str | None,
        project_id: str | None = None,
        limit: int,
    ) -> list[StrategyBacktestRecord]:
        filters = []
        if strategy_version_id is not None:
            filters.append(StrategyBacktestRow.strategy_version_id == strategy_version_id)
        if project_id is not None:
            filters.append(StrategyBacktestRow.project_id == project_id)
        result = await self._db.scalars(
            select(StrategyBacktestRow)
            .where(*filters)
            .order_by(StrategyBacktestRow.created_at.desc())
            .limit(limit)
        )
        return [_backtest_from_row(row) for row in result.all()]

    async def get_detail(self, backtest_id: str) -> StrategyBacktestDetail:
        backtest = await self._require_backtest(backtest_id)
        return StrategyBacktestDetail(
            backtest=backtest,
            result=await self._get_backtest_result(backtest_id),
        )

    async def rerun_backtest(
        self,
        backtest_id: str,
        *,
        config: StrategyBacktestConfig,
        engine: StrategyBacktestEngine | None = None,
    ) -> StrategyBacktestDetail:
        current = await self._require_backtest(backtest_id)
        version = await self._require_strategy_version(current.strategy_version_id)
        if config.strategy_mode != version.strategy_mode:
            raise BacktestError(
                "STRATEGY_MODE_MISMATCH",
                "Backtest strategy_mode must match the strategy version",
                422,
            )

        merged_params = _custom_param_defaults(version.custom_params)
        merged_params.update(config.params)
        _validate_backtest_params(version, merged_params)
        config = config.model_copy(update={"params": merged_params})

        selected_engine = engine or BacktraderStrategyBacktestEngine()
        started_at = local_now()
        running = current.model_copy(
            update={
                "status": StrategyBacktestStatus.RUNNING,
                "config": config,
                "execution_engine": selected_engine.name,
                "started_at": started_at,
                "completed_at": None,
                "failure_code": None,
                "failure_message": None,
                "failure_detail": None,
                "updated_at": started_at,
            }
        )
        logger.info(
            "strategy backtest rerun started",
            extra={
                "backtest_id": running.id,
                "strategy_id": running.strategy_id,
                "strategy_version_id": running.strategy_version_id,
                "project_id": running.project_id,
                "execution_engine": selected_engine.name,
            },
        )

        try:
            result = selected_engine.execute(backtest=running, version=version)
        except StrategyBacktestError as exc:
            logger.warning(
                "strategy backtest rerun failed",
                extra={
                    "backtest_id": running.id,
                    "strategy_id": running.strategy_id,
                    "strategy_version_id": running.strategy_version_id,
                    "project_id": running.project_id,
                    "execution_engine": selected_engine.name,
                    "error": exc.message,
                    "failure_code": exc.error_code,
                },
                exc_info=True,
            )
            raise BacktestError(exc.error_code, exc.message, 400) from exc

        completed_at = local_now()
        succeeded = running.model_copy(
            update={
                "status": StrategyBacktestStatus.SUCCEEDED,
                "result_id": result.id,
                "completed_at": completed_at,
                "updated_at": completed_at,
            }
        )
        await self._save_backtest_result(result)
        await self._save_backtest(succeeded)
        logger.info(
            "strategy backtest rerun succeeded",
            extra={
                "backtest_id": succeeded.id,
                "strategy_id": succeeded.strategy_id,
                "strategy_version_id": succeeded.strategy_version_id,
                "project_id": succeeded.project_id,
                "execution_engine": selected_engine.name,
                "result_id": result.id,
            },
        )
        return StrategyBacktestDetail(backtest=succeeded, result=result)

    async def _create_backtest(
        self,
        *,
        strategy_id: str,
        project_id: str,
        config: StrategyBacktestConfig,
        strategy_version_id: str | None = None,
    ) -> StrategyBacktestRecord:
        try:
            strategy = (await self._strategies.get_strategy(strategy_id)).strategy
        except StrategyError as exc:
            raise _from_strategy_error(exc) from exc

        if strategy.status != StrategyStatus.ACTIVE:
            raise BacktestError("STRATEGY_NOT_ACTIVE", "Strategy is not active", 409)
        selected_version_id = strategy_version_id or strategy.current_version_id
        if selected_version_id is None:
            raise BacktestError(
                "STRATEGY_VERSION_NOT_FOUND",
                "Strategy has no executable code",
                422,
            )

        version = await self._require_strategy_version(selected_version_id)
        if version.strategy_id != strategy.id:
            raise BacktestError(
                "STRATEGY_VERSION_NOT_FOUND",
                "Strategy version not found",
                404,
            )
        if config.strategy_mode != version.strategy_mode:
            raise BacktestError(
                "STRATEGY_MODE_MISMATCH",
                "Backtest strategy_mode must match the strategy version",
                422,
            )

        merged_params = _custom_param_defaults(version.custom_params)
        merged_params.update(config.params)
        _validate_backtest_params(version, merged_params)
        config = config.model_copy(update={"params": merged_params})
        backtest = StrategyBacktestRecord(
            id=_new_id("sbt"),
            project_id=project_id,
            strategy_id=strategy.id,
            strategy_version_id=version.id,
            status=StrategyBacktestStatus.PENDING,
            config=config,
        )
        await self._save_backtest(backtest)
        logger.info(
            "strategy backtest created",
            extra={
                "backtest_id": backtest.id,
                "strategy_id": strategy.id,
                "strategy_version_id": version.id,
                "project_id": project_id,
                "strategy_mode": config.strategy_mode.value,
                "symbols": config.symbols,
            },
        )
        return backtest

    async def _execute_backtest(
        self,
        backtest_id: str,
        *,
        engine: StrategyBacktestEngine,
    ) -> StrategyBacktestDetail:
        backtest = await self._require_backtest(backtest_id)
        if backtest.status in {
            StrategyBacktestStatus.RUNNING,
            StrategyBacktestStatus.SUCCEEDED,
            StrategyBacktestStatus.FAILED,
            StrategyBacktestStatus.CANCELED,
        }:
            return await self.get_detail(backtest_id)

        version = await self._require_strategy_version(backtest.strategy_version_id)
        started_at = local_now()
        running = backtest.model_copy(
            update={
                "status": StrategyBacktestStatus.RUNNING,
                "execution_engine": engine.name,
                "started_at": started_at,
                "updated_at": started_at,
            }
        )
        await self._save_backtest(running)
        logger.info(
            "strategy backtest started",
            extra={
                "backtest_id": running.id,
                "strategy_id": running.strategy_id,
                "strategy_version_id": running.strategy_version_id,
                "project_id": running.project_id,
                "execution_engine": engine.name,
            },
        )

        try:
            result = engine.execute(backtest=running, version=version)
        except StrategyBacktestError as exc:
            failed_at = local_now()
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
            await self._save_backtest(failed)
            logger.warning(
                "strategy backtest failed",
                extra={
                    "backtest_id": failed.id,
                    "strategy_id": failed.strategy_id,
                    "strategy_version_id": failed.strategy_version_id,
                    "project_id": failed.project_id,
                    "execution_engine": engine.name,
                    "error": exc.message,
                    "failure_code": exc.error_code,
                },
                exc_info=True,
            )
            return StrategyBacktestDetail(backtest=failed)

        completed_at = local_now()
        succeeded = running.model_copy(
            update={
                "status": StrategyBacktestStatus.SUCCEEDED,
                "result_id": result.id,
                "completed_at": completed_at,
                "updated_at": completed_at,
            }
        )
        await self._save_backtest_result(result)
        await self._save_backtest(succeeded)
        logger.info(
            "strategy backtest succeeded",
            extra={
                "backtest_id": succeeded.id,
                "strategy_id": succeeded.strategy_id,
                "strategy_version_id": succeeded.strategy_version_id,
                "project_id": succeeded.project_id,
                "execution_engine": engine.name,
                "result_id": result.id,
            },
        )
        return StrategyBacktestDetail(backtest=succeeded, result=result)

    async def _require_strategy_version(self, version_id: str) -> StrategyVersionRecord:
        try:
            return await self._strategies.get_version(version_id)
        except StrategyError as exc:
            raise _from_strategy_error(exc) from exc

    async def _require_backtest(self, backtest_id: str) -> StrategyBacktestRecord:
        backtest = await self._get_backtest(backtest_id)
        if backtest is None:
            raise BacktestError("BACKTEST_NOT_FOUND", "Backtest record not found", 404)
        return backtest

    async def _save_backtest(self, backtest: StrategyBacktestRecord) -> None:
        row = await self._db.get(StrategyBacktestRow, backtest.id)
        if row is None:
            self._db.add(_backtest_to_row(backtest))
        else:
            _apply_backtest(row, backtest)
        await self._db.commit()

    async def _get_backtest(self, backtest_id: str) -> StrategyBacktestRecord | None:
        row = await self._db.get(StrategyBacktestRow, backtest_id)
        return _backtest_from_row(row) if row is not None else None

    async def _save_backtest_result(self, result: StrategyBacktestResultRecord) -> None:
        row = await self._db.get(StrategyBacktestRow, result.strategy_backtest_id)
        if row is None:
            raise KeyError(result.strategy_backtest_id)
        payload = _payload_from_json(row.payload_json)
        row.payload_json = _backtest_payload(payload.backtest, result)
        await self._db.commit()

    async def _get_backtest_result(
        self,
        backtest_id: str,
    ) -> StrategyBacktestResultRecord | None:
        row = await self._db.get(StrategyBacktestRow, backtest_id)
        return _backtest_result_from_row(row.payload_json) if row is not None else None


def _service(db: AsyncSession) -> BacktestService:
    return BacktestService(db)


async def backtest_strategy(
    db: AsyncSession,
    *,
    strategy_id: str,
    project_id: str,
    config: StrategyBacktestConfig,
    engine: StrategyBacktestEngine | None = None,
    strategy_version_id: str | None = None,
) -> StrategyBacktestDetail:
    return await _service(db).backtest_strategy(
        strategy_id=strategy_id,
        project_id=project_id,
        config=config,
        engine=engine,
        strategy_version_id=strategy_version_id,
    )


async def list_records(
    db: AsyncSession,
    *,
    strategy_version_id: str | None,
    project_id: str | None = None,
    limit: int,
) -> list[StrategyBacktestRecord]:
    return await _service(db).list_records(
        strategy_version_id=strategy_version_id,
        project_id=project_id,
        limit=limit,
    )


async def get_detail(db: AsyncSession, backtest_id: str) -> StrategyBacktestDetail:
    return await _service(db).get_detail(backtest_id)


async def rerun_backtest(
    db: AsyncSession,
    backtest_id: str,
    *,
    config: StrategyBacktestConfig,
    engine: StrategyBacktestEngine | None = None,
) -> StrategyBacktestDetail:
    return await _service(db).rerun_backtest(
        backtest_id,
        config=config,
        engine=engine,
    )


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


def _custom_param_defaults(params: list[StrategyCustomParameter]) -> dict[str, object]:
    return {param.name_en: param.default for param in params}


def _validate_backtest_params(
    version: StrategyVersionRecord,
    params: dict[str, JsonValue],
) -> None:
    schema_keys = {param.name_en for param in version.custom_params}
    param_keys = set(params)
    if not param_keys.issubset(schema_keys):
        raise BacktestError(
            "STRATEGY_BACKTEST_PARAMS_INVALID",
            "Strategy backtest params must be declared by the strategy custom parameters",
            422,
        )
    for param in version.custom_params:
        value = params.get(param.name_en, param.default)
        try:
            validate_param_value(param.name_en, value, param.type)
        except ValueError as exc:
            raise BacktestError("STRATEGY_BACKTEST_PARAMS_INVALID", str(exc), 422) from exc


def _backtest_to_row(backtest: StrategyBacktestRecord) -> StrategyBacktestRow:
    row = StrategyBacktestRow()
    _apply_backtest(row, backtest)
    return row


def _apply_backtest(row: StrategyBacktestRow, backtest: StrategyBacktestRecord) -> None:
    result = _result_from_json(row.payload_json)
    row.id = backtest.id
    row.project_id = backtest.project_id
    row.strategy_id = backtest.strategy_id
    row.strategy_version_id = backtest.strategy_version_id
    row.status = backtest.status.value
    row.result_id = backtest.result_id
    row.started_at = backtest.started_at
    row.completed_at = backtest.completed_at
    row.created_at = backtest.created_at
    row.updated_at = backtest.updated_at
    row.payload_json = _backtest_payload(backtest, result)


def _backtest_payload(
    backtest: StrategyBacktestRecord,
    result: StrategyBacktestResultRecord | None,
) -> dict[str, object]:
    return StrategyBacktestPayload(backtest=backtest, result=result).model_dump(
        mode="json",
        exclude_none=True,
    )


def _payload_from_json(payload: object) -> StrategyBacktestPayload:
    if isinstance(payload, dict) and "backtest" in payload:
        return StrategyBacktestPayload.model_validate(_strip_legacy_timeframe(payload))
    return StrategyBacktestPayload(
        backtest=StrategyBacktestRecord.model_validate(_strip_legacy_timeframe(payload))
    )


def _strip_legacy_timeframe(payload: object) -> object:
    if not isinstance(payload, dict):
        return payload
    cleaned = dict(payload)
    config = cleaned.get("config")
    if isinstance(config, dict):
        cleaned["config"] = {key: value for key, value in config.items() if key != "timeframe"}
    backtest = cleaned.get("backtest")
    if isinstance(backtest, dict):
        cleaned["backtest"] = _strip_legacy_timeframe(backtest)
    return cleaned


def _result_from_json(payload: object | None) -> StrategyBacktestResultRecord | None:
    if payload is not None:
        return _payload_from_json(payload).result
    return None


def _backtest_from_row(row: StrategyBacktestRow) -> StrategyBacktestRecord:
    return _payload_from_json(row.payload_json).backtest


def _backtest_result_from_row(payload: object) -> StrategyBacktestResultRecord | None:
    return _payload_from_json(payload).result


def _from_strategy_error(error: StrategyError) -> BacktestError:
    return BacktestError(error.error_code, error.message, error.status_code)
