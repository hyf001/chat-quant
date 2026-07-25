from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, time, timedelta
from decimal import ROUND_HALF_UP, Decimal

from app.schemas.contracts.backtests import (
    BacktestComparisonDifference,
    BacktestComparisonDTO,
    BacktestComparisonMetricRow,
    BacktestComparisonSeries,
    BacktestConfig,
    BacktestDetailDTO,
    BacktestMetrics,
    BacktestResultDTO,
    BacktestRunDTO,
    BacktestRunStatus,
    CompareBacktestsRequest,
    CreateBacktestRunRequest,
    CurveArtifactDTO,
    CurvePointDTO,
    CurveType,
    JsonValue,
    RerunBacktestRequest,
    TradeRecordDTO,
    TradeSide,
    TradeStatus,
)


class BacktestNotFoundError(Exception):
    pass


class BacktestConflictError(Exception):
    pass


class BacktestValidationError(Exception):
    pass


@dataclass
class BacktestStore:
    runs: dict[str, BacktestRunDTO] = field(default_factory=dict)
    results: dict[str, BacktestResultDTO] = field(default_factory=dict)
    trades: dict[str, list[TradeRecordDTO]] = field(default_factory=dict)
    curves: dict[str, list[CurveArtifactDTO]] = field(default_factory=dict)


def utc_now() -> datetime:
    return datetime.now(tz=UTC)


def quantize(value: Decimal | float | int | str, scale: str = "0.0001") -> Decimal:
    return Decimal(str(value)).quantize(Decimal(scale), rounding=ROUND_HALF_UP)


def normalize_json(value: JsonValue) -> JsonValue:
    if isinstance(value, dict):
        return {key: normalize_json(value[key]) for key in sorted(value)}
    if isinstance(value, list):
        return [normalize_json(item) for item in value]
    return value


class BacktestResultService:
    def __init__(self, store: BacktestStore | None = None) -> None:
        self.store = store or BacktestStore()
        self._sequence = 0

    def reset(self) -> None:
        self.store = BacktestStore()
        self._sequence = 0

    def create_run(self, request: CreateBacktestRunRequest) -> BacktestRunDTO:
        config = self._build_config(request)
        self._validate_config(config)
        now = utc_now()
        run = BacktestRunDTO(
            id=self._next_id("bt"),
            user_id=request.user_id,
            project_id=request.project_id,
            chat_session_id=request.chat_session_id,
            source_sdk_session_id=request.source_sdk_session_id,
            source_sdk_message_uuid=request.source_sdk_message_uuid,
            source_sdk_tool_use_id=request.source_sdk_tool_use_id,
            strategy_id=(
                request.strategy_id
                or self._derive_strategy_id(request.strategy_version_id)
            ),
            strategy_version_id=request.strategy_version_id,
            code_artifact_id=request.code_artifact_id or f"ca_{request.strategy_version_id}",
            status=BacktestRunStatus.PENDING,
            config=config,
            config_hash=self._hash_config(config),
            created_at=now,
            updated_at=now,
        )
        self.store.runs[run.id] = run
        return run

    def run(self, backtest_run_id: str) -> BacktestDetailDTO:
        run = self._get_run(backtest_run_id)
        if run.status in {
            BacktestRunStatus.RUNNING,
            BacktestRunStatus.SUCCEEDED,
            BacktestRunStatus.FAILED,
            BacktestRunStatus.CANCELED,
        }:
            return self.get_detail(backtest_run_id, include_trades=True, include_curves=True)

        now = utc_now()
        running = run.model_copy(
            update={"status": BacktestRunStatus.RUNNING, "started_at": now, "updated_at": now}
        )
        self.store.runs[backtest_run_id] = running

        try:
            detail = self._execute_simulated_backtest(running)
        except BacktestValidationError as exc:
            failed_at = utc_now()
            failed = running.model_copy(
                update={
                    "status": BacktestRunStatus.FAILED,
                    "failure_code": "BACKTEST_CONFIG_INVALID",
                    "failure_message": str(exc),
                    "failure_detail": {"stage": "simulation"},
                    "completed_at": failed_at,
                    "updated_at": failed_at,
                }
            )
            self.store.runs[backtest_run_id] = failed
            return self.get_detail(backtest_run_id, include_trades=True, include_curves=True)

        completed_at = utc_now()
        succeeded = running.model_copy(
            update={
                "status": BacktestRunStatus.SUCCEEDED,
                "execution_result_id": f"exec_{running.id}",
                "result_id": detail.result.id if detail.result else None,
                "completed_at": completed_at,
                "updated_at": completed_at,
            }
        )
        self.store.runs[backtest_run_id] = succeeded
        return detail.model_copy(update={"run": succeeded})

    def get_detail(
        self,
        backtest_run_id: str,
        *,
        include_trades: bool = False,
        include_curves: bool = True,
    ) -> BacktestDetailDTO:
        run = self._get_run(backtest_run_id)
        return BacktestDetailDTO(
            run=run,
            result=self.store.results.get(backtest_run_id),
            trades=self.store.trades.get(backtest_run_id, []) if include_trades else [],
            curves=self.store.curves.get(backtest_run_id, []) if include_curves else [],
        )

    def list_by_strategy_version(
        self, strategy_version_id: str, status: BacktestRunStatus | None, limit: int
    ) -> list[BacktestRunDTO]:
        runs = [
            run
            for run in self.store.runs.values()
            if run.strategy_version_id == strategy_version_id
            and (status is None or run.status == status)
        ]
        runs.sort(key=lambda run: run.created_at, reverse=True)
        return runs[:limit]

    def rerun(self, backtest_run_id: str, request: RerunBacktestRequest) -> BacktestDetailDTO:
        source = self._get_run(backtest_run_id)
        config_data = source.config.model_dump(mode="json")
        config_data.update(request.override_config)
        if "params" in request.override_config:
            original_params = source.config.params.copy()
            override_params = request.override_config["params"]
            if not isinstance(override_params, dict):
                raise BacktestValidationError("override_config.params must be an object")
            original_params.update(override_params)
            config_data["params"] = original_params

        config = BacktestConfig.model_validate(config_data)
        self._validate_config(config)
        now = utc_now()
        run = BacktestRunDTO(
            id=self._next_id("bt"),
            user_id=source.user_id,
            project_id=source.project_id,
            chat_session_id=source.chat_session_id,
            source_sdk_session_id=source.source_sdk_session_id,
            strategy_id=source.strategy_id,
            strategy_version_id=request.strategy_version_id or source.strategy_version_id,
            code_artifact_id=source.code_artifact_id,
            parent_backtest_run_id=source.id,
            status=BacktestRunStatus.PENDING,
            config=config,
            config_hash=self._hash_config(config),
            created_at=now,
            updated_at=now,
        )
        self.store.runs[run.id] = run
        if request.run_immediately:
            return self.run(run.id)
        return BacktestDetailDTO(run=run)

    def compare(self, request: CompareBacktestsRequest) -> BacktestComparisonDTO:
        details = [
            self.get_detail(run_id, include_trades=False, include_curves=True)
            for run_id in request.backtest_run_ids
        ]
        incomplete = [detail.run.id for detail in details if detail.result is None]
        if incomplete:
            raise BacktestConflictError(
                f"Only succeeded backtests can be compared: {', '.join(incomplete)}"
            )

        metrics_rows: list[BacktestComparisonMetricRow] = []
        equity_series: list[BacktestComparisonSeries] = []
        drawdown_series: list[BacktestComparisonSeries] = []
        warnings: list[str] = []
        for detail in details:
            result = detail.result
            if result is None:
                continue
            metrics = result.metrics
            metrics_rows.append(
                BacktestComparisonMetricRow(
                    backtest_run_id=detail.run.id,
                    strategy_version_id=detail.run.strategy_version_id,
                    summary=result.summary,
                    annual_return_pct=metrics.annual_return_pct,
                    total_return_pct=metrics.total_return_pct,
                    max_drawdown_pct=metrics.max_drawdown_pct,
                    sharpe_ratio=metrics.sharpe_ratio,
                    win_rate_pct=metrics.win_rate_pct,
                    total_trades=metrics.total_trades,
                )
            )
            for curve in detail.curves:
                series = BacktestComparisonSeries(
                    backtest_run_id=detail.run.id,
                    label=f"{detail.run.strategy_version_id} / {detail.run.id}",
                    points=curve.points,
                )
                if curve.curve_type == CurveType.EQUITY:
                    equity_series.append(series)
                elif curve.curve_type == CurveType.DRAWDOWN:
                    drawdown_series.append(series)
            warnings.extend(result.warnings)

        differences = self._build_differences(metrics_rows)
        return BacktestComparisonDTO(
            comparison_id=self._next_id("btc"),
            base_backtest_run_id=request.base_backtest_run_id,
            backtest_run_ids=request.backtest_run_ids,
            metrics_table=metrics_rows,
            equity_series=equity_series,
            drawdown_series=drawdown_series,
            differences=differences,
            warnings=warnings,
        )

    def _execute_simulated_backtest(self, run: BacktestRunDTO) -> BacktestDetailDTO:
        config = run.config
        points = self._build_equity_points(config)
        metrics, drawdown_points, warnings = self._calculate_metrics(config, points)
        trades = self._build_trade_records(run, metrics)
        result = BacktestResultDTO(
            id=self._next_id("btr"),
            backtest_run_id=run.id,
            summary=self._build_summary(metrics),
            metrics=metrics,
            warnings=warnings,
            config_snapshot=config,
            artifact_refs={
                "result_json": f"artifact://{run.id}/result.json",
                "equity_curve_json": f"artifact://{run.id}/equity_curve.json",
                "drawdown_curve_json": f"artifact://{run.id}/drawdown_curve.json",
            },
            created_at=utc_now(),
        )
        equity_curve = CurveArtifactDTO(
            id=self._next_id("cv"),
            backtest_run_id=run.id,
            backtest_result_id=result.id,
            curve_type=CurveType.EQUITY,
            point_count=len(points),
            start_date=points[0].date,
            end_date=points[-1].date,
            metadata={"sampling": "daily", "currency": config.currency, "normalized_base": 100},
            points=points,
            created_at=utc_now(),
        )
        drawdown_curve = CurveArtifactDTO(
            id=self._next_id("cv"),
            backtest_run_id=run.id,
            backtest_result_id=result.id,
            curve_type=CurveType.DRAWDOWN,
            point_count=len(drawdown_points),
            start_date=drawdown_points[0].date,
            end_date=drawdown_points[-1].date,
            metadata={"sampling": "daily", "unit": "percent"},
            points=drawdown_points,
            created_at=utc_now(),
        )
        self.store.results[run.id] = result
        self.store.trades[run.id] = trades
        self.store.curves[run.id] = [equity_curve, drawdown_curve]
        return BacktestDetailDTO(
            run=run,
            result=result,
            trades=trades,
            curves=[equity_curve, drawdown_curve],
        )

    def _build_equity_points(self, config: BacktestConfig) -> list[CurvePointDTO]:
        days = (config.end_date - config.start_date).days
        if days < 1:
            raise BacktestValidationError(
                "backtest date range must span at least two calendar days"
            )
        total_points = min(days + 1, 260)
        step = max(1, math.ceil((days + 1) / total_points))
        dates = [config.start_date + timedelta(days=offset) for offset in range(0, days + 1, step)]
        if dates[-1] != config.end_date:
            dates.append(config.end_date)

        fast = Decimal(str(config.params.get("fast_period", 20)))
        slow = Decimal(str(config.params.get("slow_period", 60)))
        symbol_factor = Decimal(len(config.symbols)) / Decimal("1000")
        trend = (slow - fast) / Decimal("10000") + symbol_factor
        volatility = Decimal("0.018") + Decimal(str(len(config.symbols))) / Decimal("10000")
        initial = config.initial_cash
        current = initial
        peak = initial
        points: list[CurvePointDTO] = []
        for idx, point_date in enumerate(dates):
            if idx == 0:
                current = initial
            else:
                seasonal = Decimal(str(math.sin(idx / 3))) * volatility
                pulse = Decimal("-0.011") if idx % 17 == 0 else Decimal("0.004")
                daily_return = trend + seasonal + pulse - config.commission - config.slippage
                current = max(Decimal("1"), current * (Decimal("1") + daily_return))
            peak = max(peak, current)
            normalized = current / initial * Decimal("100")
            benchmark = Decimal("100") + Decimal(idx) * Decimal("0.018")
            points.append(
                CurvePointDTO(
                    date=point_date,
                    value=quantize(current),
                    normalized_value=quantize(normalized),
                    benchmark_value=quantize(benchmark),
                    extra={
                        "cash": str(quantize(current * Decimal("0.08"))),
                        "position_value": str(quantize(current * Decimal("0.92"))),
                        "peak_value": str(quantize(peak)),
                    },
                )
            )
        return points

    def _calculate_metrics(
        self, config: BacktestConfig, points: list[CurvePointDTO]
    ) -> tuple[BacktestMetrics, list[CurvePointDTO], list[str]]:
        initial = points[0].value
        final = points[-1].value
        if initial <= 0:
            raise BacktestValidationError("initial equity must be greater than zero")
        total_return = (final / initial - Decimal("1")) * Decimal("100")
        days = max(1, (points[-1].date - points[0].date).days)
        annual_return = Decimal(str((float(final / initial) ** (365 / days) - 1) * 100))

        peak = initial
        peak_date = points[0].date
        max_drawdown = Decimal("0")
        max_start: date | None = None
        max_end: date | None = None
        drawdown_points: list[CurvePointDTO] = []
        returns: list[Decimal] = []
        previous = initial
        for point in points:
            if point.value > peak:
                peak = point.value
                peak_date = point.date
            drawdown = (point.value / peak - Decimal("1")) * Decimal("100")
            if drawdown < max_drawdown:
                max_drawdown = drawdown
                max_start = peak_date
                max_end = point.date
            drawdown_points.append(
                CurvePointDTO(
                    date=point.date,
                    value=quantize(drawdown),
                    extra={"peak_value": str(peak), "equity_value": str(point.value)},
                )
            )
            if point.value != previous:
                returns.append(point.value / previous - Decimal("1"))
            previous = point.value

        volatility = self._annualized_volatility(returns)
        annual_return_fraction = annual_return / Decimal("100")
        volatility_fraction = volatility / Decimal("100") if volatility is not None else None
        sharpe = None
        warnings: list[str] = []
        if volatility_fraction and volatility_fraction > 0:
            sharpe = (annual_return_fraction - config.risk_free_rate) / volatility_fraction
        else:
            warnings.append("波动率为 0，夏普比率不可计算")
        max_drawdown_abs = abs(max_drawdown)
        calmar = None if max_drawdown_abs == 0 else annual_return / max_drawdown_abs
        trades = max(1, min(120, len(points) // 8))
        win_rate = Decimal("48") + Decimal(str(len(config.symbols) % 7))
        profit_factor = Decimal("1.15") + max(Decimal("0"), total_return / Decimal("200"))
        duration = None
        if max_start and max_end:
            duration = (max_end - max_start).days

        metrics = BacktestMetrics(
            initial_value=quantize(initial),
            final_value=quantize(final),
            total_return_pct=quantize(total_return),
            annual_return_pct=quantize(annual_return),
            max_drawdown_pct=quantize(max_drawdown),
            max_drawdown_abs_pct=quantize(max_drawdown_abs),
            max_drawdown_start=max_start,
            max_drawdown_end=max_end,
            max_drawdown_duration_days=duration,
            volatility_annual_pct=quantize(volatility) if volatility is not None else None,
            sharpe_ratio=quantize(sharpe) if sharpe is not None else None,
            calmar_ratio=quantize(calmar) if calmar is not None else None,
            win_rate_pct=quantize(win_rate),
            total_trades=trades,
            profit_factor=quantize(profit_factor),
        )
        return metrics, drawdown_points, warnings

    def _build_trade_records(
        self,
        run: BacktestRunDTO,
        metrics: BacktestMetrics,
    ) -> list[TradeRecordDTO]:
        records: list[TradeRecordDTO] = []
        total = min(metrics.total_trades, 12)
        for idx in range(total):
            symbol = run.config.symbols[idx % len(run.config.symbols)]
            trade_date = datetime.combine(
                run.config.start_date + timedelta(days=idx * 9 + 1), time(hour=15), tzinfo=UTC
            )
            price = Decimal("10") + Decimal(idx) * Decimal("0.37")
            size = Decimal("100")
            value = price * size
            records.append(
                TradeRecordDTO(
                    id=self._next_id("tr"),
                    backtest_run_id=run.id,
                    symbol=symbol,
                    trade_id=f"{run.id}_pair_{idx + 1}",
                    side=TradeSide.BUY if idx % 2 == 0 else TradeSide.SELL,
                    status=TradeStatus.CLOSED,
                    trade_datetime=trade_date,
                    price=quantize(price),
                    size=size,
                    value=quantize(value),
                    commission=quantize(value * run.config.commission),
                    pnl=quantize((Decimal(idx % 5) - Decimal("1.5")) * Decimal("125")),
                    pnl_pct=quantize((Decimal(idx % 5) - Decimal("1.5")) * Decimal("0.8")),
                    holding_days=5 + idx,
                    metadata={"basis": "simulated_runtime_adapter"},
                )
            )
        return records

    def _annualized_volatility(self, returns: list[Decimal]) -> Decimal | None:
        if len(returns) < 2:
            return None
        mean = sum(returns) / Decimal(len(returns))
        variance = sum((item - mean) ** 2 for item in returns) / Decimal(len(returns) - 1)
        return (
            Decimal(str(math.sqrt(float(variance))))
            * Decimal(str(math.sqrt(252)))
            * Decimal("100")
        )

    def _build_differences(
        self, metrics_rows: list[BacktestComparisonMetricRow]
    ) -> list[BacktestComparisonDifference]:
        differences: list[BacktestComparisonDifference] = []
        metric_names = ["annual_return_pct", "total_return_pct", "max_drawdown_pct", "sharpe_ratio"]
        for metric_name in metric_names:
            values = [
                (row.backtest_run_id, getattr(row, metric_name))
                for row in metrics_rows
                if getattr(row, metric_name) is not None
            ]
            if len(values) < 2:
                continue
            best = max(values, key=lambda item: item[1])
            worst = min(values, key=lambda item: item[1])
            differences.append(
                BacktestComparisonDifference(
                    metric=metric_name,
                    best_backtest_run_id=best[0],
                    worst_backtest_run_id=worst[0],
                    spread=quantize(best[1] - worst[1]),
                )
            )
        return differences

    def _build_summary(self, metrics: BacktestMetrics) -> str:
        return (
            f"回测完成：年化收益 {metrics.annual_return_pct}%，"
            f"最大回撤 {metrics.max_drawdown_pct}%，夏普 {metrics.sharpe_ratio}。"
        )

    def _build_config(self, request: CreateBacktestRunRequest) -> BacktestConfig:
        return BacktestConfig(
            symbols=request.symbols,
            universe_ref=request.universe_ref,
            market=request.market,
            benchmark_symbol=request.benchmark_symbol,
            start_date=request.start_date,
            end_date=request.end_date,
            timeframe=request.timeframe,
            data_source=request.data_source,
            data_adjust=request.data_adjust,
            data_as_of=request.data_as_of,
            initial_cash=request.initial_cash,
            commission=request.commission,
            slippage=request.slippage,
            tax=request.tax,
            order_size_mode=request.order_size_mode,
            params=request.params,
            risk_free_rate=request.risk_free_rate,
            calendar=request.calendar,
            currency=request.currency,
            assumptions=request.assumptions,
        )

    def _validate_config(self, config: BacktestConfig) -> None:
        if config.timeframe != "1d":
            raise BacktestValidationError("only 1d timeframe is supported in the first milestone")
        if config.end_date > date.today():
            raise BacktestValidationError("end_date cannot be in the future")
        fast = config.params.get("fast_period")
        slow = config.params.get("slow_period")
        if fast is not None and slow is not None and Decimal(str(fast)) >= Decimal(str(slow)):
            raise BacktestValidationError("fast_period must be less than slow_period")

    def _hash_config(self, config: BacktestConfig) -> str:
        payload = config.model_dump(mode="json")
        payload["params"] = normalize_json(config.params)
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        return f"sha256:{hashlib.sha256(encoded.encode('utf-8')).hexdigest()}"

    def _get_run(self, backtest_run_id: str) -> BacktestRunDTO:
        try:
            return self.store.runs[backtest_run_id]
        except KeyError as exc:
            raise BacktestNotFoundError(backtest_run_id) from exc

    def _next_id(self, prefix: str) -> str:
        self._sequence += 1
        return f"{prefix}_{self._sequence:06d}"

    def _derive_strategy_id(self, strategy_version_id: str) -> str:
        if strategy_version_id.startswith("stv_"):
            return f"st_{strategy_version_id[4:]}"
        return f"st_{strategy_version_id}"


backtest_service = BacktestResultService()
