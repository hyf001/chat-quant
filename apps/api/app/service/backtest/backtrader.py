from __future__ import annotations

import sys
from decimal import Decimal
from uuid import uuid4

import backtrader as bt
import pandas as pd

from app.schema.backtest import (
    CurveType,
    StrategyBacktestMetrics,
    StrategyBacktestRecord,
    StrategyBacktestResultRecord,
    StrategyBenchmarkPoint,
    StrategyBenchmarkSeries,
    StrategyCurve,
    StrategyCurvePoint,
    StrategyDailyPortfolioSnapshot,
    StrategyDailyPosition,
    StrategyMarketCandle,
    StrategyMarketSeries,
    StrategyTradeRecord,
    TradeSide,
    TradeStatus,
)
from app.schema.strategy import StrategyVersionRecord
from app.service.backtest.execution import StrategyBacktestError
from app.service.chatq_engine import (
    ChatQBacktraderStrategyBase,
    ClosedTradeAnalyzer,
    DailyPortfolioAnalyzer,
    EquityCurveAnalyzer,
    OrderExecutionAnalyzer,
    drawdown_analysis,
    equity_returns,
    quantize,
    sharpe_ratio,
    win_rate_pct,
)
from app.service.market_data import (
    MarketDataError,
    load_benchmark,
    load_market,
    market_data_source_metadata,
)
from app.service.strategy.protocol import (
    ChatQStrategyModule,
    StrategyProtocolError,
    load_strategy_module,
)
from app.service.strategy.runtime import (
    ChatQStrategyRuntime,
    ChatQStrategyRuntimeError,
)


class BacktraderStrategyBacktestEngine:
    name = "backtrader"
    protocol_name = "chatq_signal_strategy_v1"

    def execute(
        self,
        *,
        backtest: StrategyBacktestRecord,
        version: StrategyVersionRecord,
    ) -> StrategyBacktestResultRecord:
        module_name = f"chatq_strategy_{uuid4().hex}"
        try:
            strategy_module = self._load_strategy_module(version, module_name)
            cerebro = bt.Cerebro(stdstats=False)
            cerebro.broker.setcash(float(backtest.config.initial_cash))
            cerebro.broker.setcommission(commission=float(backtest.config.commission))
            cerebro.broker.set_coc(backtest.config.execution_mode == "current_close")
            if backtest.config.slippage > 0:
                cerebro.broker.set_slippage_perc(float(backtest.config.slippage))

            if not backtest.config.symbols:
                raise StrategyBacktestError(
                    "STRATEGY_DATA_UNAVAILABLE",
                    "Backtest execution requires resolved symbols",
                    detail={"strategy_mode": backtest.config.strategy_mode.value},
                )

            market_frames: dict[str, pd.DataFrame] = {}
            for symbol in backtest.config.symbols:
                data, frame = _load_market_data_feed(
                    symbol=symbol,
                    backtest=backtest,
                )
                market_frames[symbol] = frame
                cerebro.adddata(data, name=symbol)

            params = _strategy_param_values(version, backtest.config.params)
            cerebro.addstrategy(
                ChatQBacktraderStrategyBase,
                strategy_module=strategy_module,
                chatq_param_values=params,
                symbols=backtest.config.symbols,
                history=market_frames,
                services=ChatQStrategyRuntime(),
                execution_mode=backtest.config.execution_mode,
            )
            cerebro.addanalyzer(EquityCurveAnalyzer, _name="equity_curve")
            cerebro.addanalyzer(ClosedTradeAnalyzer, _name="closed_trades")
            cerebro.addanalyzer(OrderExecutionAnalyzer, _name="orders")
            cerebro.addanalyzer(DailyPortfolioAnalyzer, _name="daily_portfolio")
            executed = cerebro.run()
        except StrategyBacktestError:
            raise
        except StrategyProtocolError as exc:
            raise StrategyBacktestError(exc.error_code, exc.message) from exc
        except ChatQStrategyRuntimeError as exc:
            raise StrategyBacktestError(
                _strategy_runtime_error_code(exc),
                exc.message,
                detail={"source": "context['chatq'].sql", **exc.detail},
            ) from exc
        except Exception as exc:
            raise StrategyBacktestError(
                "STRATEGY_EXECUTION_FAILED",
                str(exc),
                detail={"exception_type": type(exc).__name__},
            ) from exc
        finally:
            sys.modules.pop(module_name, None)

        strategy = executed[0]
        equity_points = strategy.analyzers.equity_curve.get_analysis()
        closed_trade_items = strategy.analyzers.closed_trades.get_analysis()
        order_items = strategy.analyzers.orders.get_analysis()
        daily_portfolio_items = strategy.analyzers.daily_portfolio.get_analysis()
        metrics, drawdown_points = _build_metrics(backtest, equity_points, closed_trade_items)

        result_id = _new_id("srr")
        trades = [
            StrategyTradeRecord(
                id=_new_id("strd"),
                strategy_backtest_id=backtest.id,
                symbol=item["symbol"],
                side=TradeSide.BUY if item["side"] == "buy" else TradeSide.SELL,
                status=TradeStatus.OPENED,
                trade_datetime=item["datetime"],
                price=quantize(item["price"]),
                size=quantize(abs(item["size"]), "0.000001"),
                value=quantize(abs(item["value"])),
                commission=quantize(item["commission"]),
                metadata={"basis": "backtrader_order_execution"},
            )
            for item in order_items
        ]
        equity_curve = _build_curve(
            backtest_id=backtest.id,
            result_id=result_id,
            curve_type=CurveType.EQUITY,
            points=equity_points,
        )
        drawdown_curve = _build_curve(
            backtest_id=backtest.id,
            result_id=result_id,
            curve_type=CurveType.DRAWDOWN,
            points=drawdown_points,
        )
        market_data = [
            _build_market_series(symbol=symbol, frame=frame)
            for symbol, frame in market_frames.items()
        ]
        daily_positions = _build_daily_positions(daily_portfolio_items)
        warnings: list[str] = []
        benchmark = _build_benchmark_series(backtest, warnings)
        return StrategyBacktestResultRecord(
            id=result_id,
            strategy_backtest_id=backtest.id,
            summary=(
                f"策略回测完成：总收益 {metrics.total_return_pct}%，"
                f"最大回撤 {metrics.max_drawdown_pct}%，交易 {metrics.total_trades} 笔。"
            ),
            metrics=metrics,
            trades=trades,
            curves=[equity_curve, drawdown_curve],
            market_data=market_data,
            benchmark=benchmark,
            daily_positions=daily_positions,
            warnings=warnings,
            engine=self.name,
            protocol=self.protocol_name,
            data_source=_backtest_data_source_metadata(backtest.config.symbols),
        )

    def _load_strategy_module(
        self,
        version: StrategyVersionRecord,
        module_name: str,
    ) -> ChatQStrategyModule:
        try:
            return load_strategy_module(version.source_code, module_name=module_name)
        except StrategyProtocolError as exc:
            raise StrategyBacktestError(exc.error_code, exc.message) from exc


def _strategy_runtime_error_code(exc: ChatQStrategyRuntimeError) -> str:
    if exc.error_code == "DATASET_NOT_EXPOSED":
        return "STRATEGY_DATA_QUERY_FORBIDDEN"
    return "STRATEGY_DATA_QUERY_FAILED"


def _strategy_param_values(
    version: StrategyVersionRecord,
    overrides: dict[str, object],
) -> dict[str, object]:
    params = {param.name_en: param.default for param in version.custom_params}
    params.update(overrides)
    return params


def _load_market_data_feed(
    *,
    symbol: str,
    backtest: StrategyBacktestRecord,
) -> tuple[bt.feeds.PandasData, pd.DataFrame]:
    try:
        result = load_market(
            symbol=symbol,
            start_date=backtest.config.start_date,
            end_date=backtest.config.end_date,
        )
    except MarketDataError as exc:
        raise _backtest_error(exc) from exc
    except Exception as exc:
        raise StrategyBacktestError(
            "BACKTEST_DATASET_LOAD_FAILED",
            f"Failed to load market data for {symbol}: {exc}",
            detail={
                "symbol": symbol,
                "exception_type": type(exc).__name__,
            },
        ) from exc

    frame = result.frame
    if frame.empty:
        raise StrategyBacktestError(
            "BACKTEST_DATASET_EMPTY",
            f"No market data returned for {symbol}",
            detail={
                "symbol": symbol,
                "start_date": backtest.config.start_date.isoformat(),
                "end_date": backtest.config.end_date.isoformat(),
            },
        )
    return bt.feeds.PandasData(dataname=frame), frame


def _build_metrics(
    backtest: StrategyBacktestRecord,
    equity_points: list[dict[str, object]],
    trade_items: list[dict[str, object]],
) -> tuple[StrategyBacktestMetrics, list[dict[str, object]]]:
    if not equity_points:
        raise StrategyBacktestError(
            "STRATEGY_RESULT_EMPTY",
            "Strategy execution did not produce an equity curve",
        )

    initial = Decimal(str(backtest.config.initial_cash))
    final = Decimal(str(equity_points[-1]["value"]))
    total_return = (final / initial - Decimal("1")) * Decimal("100")
    days = max(1, (backtest.config.end_date - backtest.config.start_date).days)
    annual_return = Decimal(str((float(final / initial) ** (365 / days) - 1) * 100))

    max_drawdown, max_start, max_end, drawdown_points = drawdown_analysis(equity_points)

    sharpe = sharpe_ratio(equity_returns(equity_points))
    win_rate = win_rate_pct(trade_items)
    duration = (max_end - max_start).days if max_start is not None and max_end is not None else None
    metrics = StrategyBacktestMetrics(
        initial_value=quantize(initial),
        final_value=quantize(final),
        total_return_pct=quantize(total_return),
        annual_return_pct=quantize(annual_return),
        max_drawdown_pct=quantize(max_drawdown),
        max_drawdown_start=max_start,
        max_drawdown_end=max_end,
        max_drawdown_duration_days=duration,
        sharpe_ratio=quantize(sharpe) if sharpe is not None else None,
        win_rate_pct=quantize(win_rate) if win_rate is not None else None,
        total_trades=len(trade_items),
    )
    return metrics, drawdown_points


def _build_curve(
    *,
    backtest_id: str,
    result_id: str,
    curve_type: CurveType,
    points: list[dict[str, object]],
) -> StrategyCurve:
    curve_points = [
        StrategyCurvePoint(
            date=point["date"],
            value=quantize(point["value"]),
            normalized_value=None,
            extra={
                key: str(quantize(value))
                for key, value in point.items()
                if key not in {"date", "value"}
            },
        )
        for point in points
    ]
    return StrategyCurve(
        id=_new_id("scv"),
        strategy_backtest_id=backtest_id,
        strategy_backtest_result_id=result_id,
        curve_type=curve_type,
        point_count=len(curve_points),
        start_date=curve_points[0].date,
        end_date=curve_points[-1].date,
        points=curve_points,
    )


def _build_market_series(*, symbol: str, frame: pd.DataFrame) -> StrategyMarketSeries:
    candles = [
        StrategyMarketCandle(
            symbol=symbol,
            date=index.date(),
            open=quantize(row["open"]),
            high=quantize(row["high"]),
            low=quantize(row["low"]),
            close=quantize(row["close"]),
            volume=quantize(row["volume"], "0.000001"),
        )
        for index, row in frame.iterrows()
    ]
    return StrategyMarketSeries(symbol=symbol, candles=candles)


def _build_daily_positions(
    items: list[dict[str, object]],
) -> list[StrategyDailyPortfolioSnapshot]:
    snapshots: list[StrategyDailyPortfolioSnapshot] = []
    for item in items:
        positions = [
            StrategyDailyPosition(
                symbol=str(position["symbol"]),
                size=quantize(position["size"], "0.000001"),
                close_price=quantize(position["close_price"]),
                market_value=quantize(position["market_value"]),
                unrealized_pnl=quantize(position["unrealized_pnl"]),
            )
            for position in item["positions"]
            if isinstance(position, dict)
        ]
        snapshots.append(
            StrategyDailyPortfolioSnapshot(
                date=item["date"],
                cash=quantize(item["cash"]),
                total_value=quantize(item["total_value"]),
                daily_pnl=quantize(item["daily_pnl"]),
                positions=positions,
            )
        )
    return snapshots


def _build_benchmark_series(
    backtest: StrategyBacktestRecord,
    warnings: list[str],
) -> StrategyBenchmarkSeries | None:
    benchmark_symbol = backtest.config.benchmark_symbol
    if not benchmark_symbol:
        return None

    try:
        result = load_benchmark(
            symbol=benchmark_symbol,
            start_date=backtest.config.start_date,
            end_date=backtest.config.end_date,
        )
        if result is None:
            return None
        frame = result.frame
    except Exception as exc:  # noqa: BLE001 - benchmark is comparative context, not core execution.
        warnings.append(f"基准行情加载失败：{exc}")
        return None

    if frame.empty:
        warnings.append("基准没有返回行情")
        return None

    initial_close = Decimal(str(frame.iloc[0].close))
    points = [
        StrategyBenchmarkPoint(
            date=index.date(),
            value=quantize(row["close"]),
            normalized_value=quantize(
                (Decimal(str(row["close"])) / initial_close - Decimal("1")) * Decimal("100")
            ),
        )
        for index, row in frame.iterrows()
    ]
    return StrategyBenchmarkSeries(
        symbol=benchmark_symbol,
        total_return_pct=points[-1].normalized_value if points else None,
        points=points,
    )


def _backtest_data_source_metadata(symbols: list[str]) -> dict[str, object]:
    try:
        return market_data_source_metadata(symbols)
    except MarketDataError as exc:
        raise _backtest_error(exc) from exc


def _backtest_error(error: MarketDataError) -> StrategyBacktestError:
    return StrategyBacktestError(
        _backtest_error_code(error.error_code),
        error.message,
        detail=dict(error.detail),
    )


def _backtest_error_code(error_code: str) -> str:
    mapping = {
        "MARKET_DATA_DATASET_NOT_CONFIGURED": "BACKTEST_MARKET_DATASET_NOT_CONFIGURED",
        "MARKET_DATA_BENCHMARK_NOT_CONFIGURED": "BACKTEST_BENCHMARK_DATASET_NOT_CONFIGURED",
        "MARKET_DATASET_NOT_FOUND": "BACKTEST_DATASET_NOT_FOUND",
        "MARKET_DATASET_QUERY_FAILED": "BACKTEST_DATASET_QUERY_FAILED",
        "MARKET_DATASET_FIELD_NOT_FOUND": "BACKTEST_DATASET_FIELD_NOT_FOUND",
        "MARKET_DATASET_FORMAT_INVALID": "BACKTEST_DATASET_FORMAT_INVALID",
        "MARKET_DATASET_EMPTY": "BACKTEST_DATASET_EMPTY",
        "MARKET_BENCHMARK_FORMAT_INVALID": "BACKTEST_BENCHMARK_FORMAT_INVALID",
        "MARKET_BENCHMARK_EMPTY": "BACKTEST_BENCHMARK_EMPTY",
        "MARKET_DATASET_MAPPING_INVALID": "BACKTEST_DATASET_MAPPING_INVALID",
        "MARKET_DATA_WINDOW_INVALID": "BACKTEST_DATASET_MAPPING_INVALID",
        "MARKET_DATA_LOOKBACK_INVALID": "BACKTEST_DATASET_MAPPING_INVALID",
    }
    return mapping.get(error_code, error_code.replace("MARKET_", "BACKTEST_"))


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"
