from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING, Any, Protocol

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from app.schema.strategy import (
    StrategyDeploymentMode,
    StrategyDeploymentRecord,
    StrategySignalStatus,
)
from app.service.job_runtime import (
    ExecutionResult,
    JobRef,
    JobRuntimeInstanceService,
    JobRuntimeRegistry,
    JobTrigger,
    job_runtime_registry,
)
from app.service.market_data import MarketDataError, load_market
from app.service.strategy.deployment_service import (
    STRATEGY_DEPLOYMENT_TICK_JOB_TYPE,
    StrategyDeploymentError,
    StrategyDeploymentService,
    _require_strategy_version,
    _signal_action,
)
from app.service.strategy.protocol import (
    ChatQBar,
    ChatQOpenOrder,
    ChatQOrderEvent,
    ChatQPosition,
    ChatQReadOnlyServices,
)
from app.service.strategy.strategy_executor import (
    StrategyExecutionConfig,
    StrategyExecutionContext,
    StrategyExecutionError,
    StrategyExecutor,
)

if TYPE_CHECKING:
    from app.model.job_runtime import JobInstanceRow


@dataclass(frozen=True)
class StrategyRuntimeTrigger:
    instance_id: str | None
    scheduled_for: datetime
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class StrategyDeploymentRuntimeContext:
    history: dict[str, pd.DataFrame]
    current_bars: dict[str, ChatQBar]
    bars: dict[str, pd.DataFrame]
    cash: float = 0.0
    portfolio_value: float = 0.0
    positions: dict[str, ChatQPosition] = field(default_factory=dict)
    open_orders: list[ChatQOpenOrder] = field(default_factory=list)
    order_events: list[ChatQOrderEvent] = field(default_factory=list)
    chatq: ChatQReadOnlyServices | None = None


class StrategyDeploymentContextProvider(Protocol):
    async def load_context(
        self,
        db: AsyncSession,
        *,
        deployment: StrategyDeploymentRecord,
        trigger: StrategyRuntimeTrigger,
    ) -> StrategyDeploymentRuntimeContext: ...


class DatasetStrategyDeploymentContextProvider:
    async def load_context(
        self,
        db: AsyncSession,
        *,
        deployment: StrategyDeploymentRecord,
        trigger: StrategyRuntimeTrigger,
    ) -> StrategyDeploymentRuntimeContext:
        del db
        try:
            bars = {
                symbol: load_market(
                    symbol=symbol,
                    end_time=trigger.scheduled_for,
                    lookback_bars=deployment.lookback_bars,
                ).frame
                for symbol in deployment.symbols
            }
        except MarketDataError as exc:
            raise StrategyDeploymentError(
                exc.error_code,
                exc.message,
                422,
                detail=dict(exc.detail),
            ) from exc
        return StrategyDeploymentRuntimeContext(
            history=bars,
            bars=bars,
            current_bars={
                symbol: _current_bar(symbol, frame)
                for symbol, frame in bars.items()
            },
        )


def strategy_deployment_job_ref(deployment_id: str) -> JobRef:
    return JobRef(
        job_type=STRATEGY_DEPLOYMENT_TICK_JOB_TYPE,
        job_id=deployment_id,
    )


class StrategyDeploymentTickInstanceFactory:
    async def create_job_instances(
        self,
        db: AsyncSession,
        *,
        job_ref: JobRef,
        trigger: JobTrigger,
        instance_service: JobRuntimeInstanceService,
    ) -> list[JobInstanceRow]:
        return [
            await instance_service.create_job_instance(
                db,
                job_ref=job_ref,
                trigger_type=trigger.trigger_type,
                trigger_key=trigger.trigger_key,
                scheduled_for=trigger.scheduled_for,
                payload=dict(trigger.payload or {}),
            )
        ]


class StrategyDeploymentTickExecutor:
    def __init__(
        self,
        *,
        context_provider: StrategyDeploymentContextProvider | None = None,
    ) -> None:
        self._context_provider = context_provider

    async def execute_job_instance(
        self,
        db: AsyncSession,
        *,
        instance: JobInstanceRow,
        instance_service: JobRuntimeInstanceService,
    ) -> ExecutionResult:
        _ = instance_service
        return await execute_strategy_deployment_tick(
            db,
            deployment_id=instance.job_id,
            trigger=StrategyRuntimeTrigger(
                instance_id=instance.id,
                scheduled_for=instance.scheduled_for,
                payload=dict(instance.trigger_payload_json or {}),
            ),
            context_provider=self._context_provider,
        )


def register_strategy_deployment_job_runtime_handlers(
    registry: JobRuntimeRegistry | None = None,
) -> JobRuntimeRegistry:
    registry = registry or job_runtime_registry
    registry.register_instance_factory(
        job_type=STRATEGY_DEPLOYMENT_TICK_JOB_TYPE,
        factory=StrategyDeploymentTickInstanceFactory(),
    )
    registry.register_job_executor(
        job_type=STRATEGY_DEPLOYMENT_TICK_JOB_TYPE,
        executor=StrategyDeploymentTickExecutor(),
    )
    return registry


async def execute_strategy_deployment_tick(
    db: AsyncSession,
    *,
    deployment_id: str,
    trigger: StrategyRuntimeTrigger,
    context_provider: StrategyDeploymentContextProvider | None = None,
) -> ExecutionResult:
    service = StrategyDeploymentService(db)
    deployment = await service.get_deployment(deployment_id)
    if deployment.mode != StrategyDeploymentMode.SIGNAL:
        return ExecutionResult(
            result_status="skipped",
            summary=f"deployment mode {deployment.mode.value} is not implemented in phase 2",
            payload={"deployment_id": deployment_id, "mode": deployment.mode.value},
        )
    if context_provider is None:
        context_provider = DatasetStrategyDeploymentContextProvider()

    version = await _require_strategy_version(
        db,
        deployment.strategy_version_id,
        strategy_id=deployment.strategy_id,
    )
    runtime_context = await context_provider.load_context(
        db,
        deployment=deployment,
        trigger=trigger,
    )
    config = StrategyExecutionConfig(
        mode=deployment.mode,
        symbols=deployment.symbols,
        lookback_bars=deployment.lookback_bars,
        params=deployment.params,
        broker_id=deployment.broker_id,
        requires_manual_confirm=deployment.requires_manual_confirm,
        risk_config=deployment.risk_config,
        validate_actions=False,
    )
    executor: StrategyExecutor | None = None
    try:
        executor = StrategyExecutor(
            strategy_version=version,
            config=config,
            module_name=f"chatq_deployment_{deployment.id}_{trigger.instance_id or 'manual'}",
        )
        result = executor.run_next(
            state=dict(deployment.state),
            context=StrategyExecutionContext(
                execution_time=trigger.scheduled_for.isoformat(),
                history=runtime_context.history,
                current_bars=runtime_context.current_bars,
                bars=runtime_context.bars,
                cash=runtime_context.cash,
                portfolio_value=runtime_context.portfolio_value,
                positions=runtime_context.positions,
                open_orders=runtime_context.open_orders,
                order_events=runtime_context.order_events,
                chatq=runtime_context.chatq,
            ),
        )
    except StrategyExecutionError as exc:
        raise StrategyDeploymentError(exc.error_code, exc.message, 422) from exc
    finally:
        if executor is not None:
            executor.close()

    saved_signals = []
    generated_count = 0
    rejected_count = 0
    for action in result.actions:
        status = StrategySignalStatus.GENERATED
        reason = str(action.get("reason")) if action.get("reason") is not None else None
        try:
            signal_action = _signal_action(action)
        except Exception as exc:
            signal_action = action
            status = StrategySignalStatus.REJECTED
            rejected_count += 1
            reason = str(exc)
        else:
            generated_count += 1
        saved_signals.append(
            await service.save_signal(
                deployment_id=deployment.id,
                job_instance_id=trigger.instance_id,
                strategy_version_id=deployment.strategy_version_id,
                signal_datetime=trigger.scheduled_for,
                action=signal_action,
                status=status,
                reason=reason,
            )
        )

    await service.save_state(deployment.id, result.state)
    return ExecutionResult(
        result_status="completed",
        summary=(
            f"saved {len(saved_signals)} signals "
            f"({generated_count} generated, {rejected_count} rejected)"
        ),
        payload={
            "deployment_id": deployment.id,
            "signal_count": len(saved_signals),
            "generated_count": generated_count,
            "rejected_count": rejected_count,
        },
    )


def _current_bar(symbol: str, frame: pd.DataFrame) -> ChatQBar:
    row = frame.iloc[-1]
    index_value = frame.index[-1]
    if hasattr(index_value, "isoformat"):
        datetime_value = index_value.isoformat()
    else:
        datetime_value = str(index_value)
    return {
        "symbol": symbol,
        "datetime": datetime_value,
        "open": float(row["open"]),
        "high": float(row["high"]),
        "low": float(row["low"]),
        "close": float(row["close"]),
        "volume": float(row["volume"]),
    }
