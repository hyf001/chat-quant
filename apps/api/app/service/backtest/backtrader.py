from __future__ import annotations

import math
import sys
from datetime import date, datetime, time
from decimal import ROUND_HALF_UP, Decimal
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
from app.service.backtest.market_data import (
    backtest_dataset_source_metadata,
    load_backtest_benchmark_frame,
    load_backtest_market_frame,
)
from app.service.strategy.protocol import (
    StrategyProtocolError,
    load_strategy_class,
    with_backtrader_params,
)


class BacktraderStrategyBacktestEngine:
    name = "backtrader"
    protocol_name = "chatq_backtrader_strategy_v2"

    def execute(
        self,
        *,
        backtest: StrategyBacktestRecord,
        version: StrategyVersionRecord,
    ) -> StrategyBacktestResultRecord:
        module_name = f"chatq_strategy_{uuid4().hex}"
        try:
            strategy_cls = self._load_strategy_class(version, module_name)
            strategy_cls = with_backtrader_params(strategy_cls, version.custom_params)
            cerebro = bt.Cerebro(stdstats=False)
            cerebro.broker.setcash(float(backtest.config.initial_cash))
            cerebro.broker.setcommission(commission=float(backtest.config.commission))
            if backtest.config.slippage > 0:
                cerebro.broker.set_slippage_perc(float(backtest.config.slippage))

            if not backtest.config.symbols:
                raise StrategyBacktestError(
                    "STRATEGY_DATA_UNAVAILABLE",
                    "Backtest execution requires resolved symbols",
                    detail={"symbol_source": backtest.config.symbol_source},
                )

            market_frames: dict[str, pd.DataFrame] = {}
            for symbol in backtest.config.symbols:
                data, frame = _load_market_data_feed(
                    symbol=symbol,
                    backtest=backtest,
                )
                market_frames[symbol] = frame
                cerebro.adddata(data, name=symbol)

            params = {key: value for key, value in backtest.config.params.items()}
            cerebro.addstrategy(strategy_cls, **params)
            cerebro.addanalyzer(_EquityCurveAnalyzer, _name="equity_curve")
            cerebro.addanalyzer(_ClosedTradeAnalyzer, _name="closed_trades")
            cerebro.addanalyzer(_OrderExecutionAnalyzer, _name="orders")
            cerebro.addanalyzer(_DailyPortfolioAnalyzer, _name="daily_portfolio")
            executed = cerebro.run()
        except StrategyBacktestError:
            raise
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
                price=_quantize(item["price"]),
                size=_quantize(abs(item["size"]), "0.000001"),
                value=_quantize(abs(item["value"])),
                commission=_quantize(item["commission"]),
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
            data_source=backtest_dataset_source_metadata(backtest.config.symbols),
        )

    def _load_strategy_class(
        self,
        version: StrategyVersionRecord,
        module_name: str,
    ) -> type[bt.Strategy]:
        try:
            return load_strategy_class(version.source_code, module_name=module_name)
        except StrategyProtocolError as exc:
            raise StrategyBacktestError(exc.error_code, exc.message) from exc


class _EquityCurveAnalyzer(bt.Analyzer):
    def start(self) -> None:
        self.points: list[dict[str, object]] = []

    def next(self) -> None:
        point_date = self.strategy.datas[0].datetime.date(0)
        self.points.append(
            {
                "date": point_date,
                "value": self.strategy.broker.getvalue(),
                "cash": self.strategy.broker.getcash(),
            }
        )

    def get_analysis(self) -> list[dict[str, object]]:
        return self.points


class _ClosedTradeAnalyzer(bt.Analyzer):
    def start(self) -> None:
        self.trades: list[dict[str, object]] = []

    def notify_trade(self, trade: bt.Trade) -> None:
        if not trade.isclosed:
            return
        close_date = bt.num2date(trade.dtclose).date()
        value = abs(float(trade.value))
        pnl = float(trade.pnlcomm)
        self.trades.append(
            {
                "symbol": trade.data._name,
                "date": close_date,
                "size": float(trade.size),
                "price": float(trade.price),
                "value": value,
                "pnl": pnl,
                "pnl_pct": (pnl / value * 100) if value else None,
            }
        )

    def get_analysis(self) -> list[dict[str, object]]:
        return self.trades


class _OrderExecutionAnalyzer(bt.Analyzer):
    def start(self) -> None:
        self.orders: list[dict[str, object]] = []

    def notify_order(self, order: bt.Order) -> None:
        if order.status != order.Completed:
            return
        executed_at = (
            bt.num2date(order.executed.dt)
            if order.executed.dt
            else datetime.combine(order.data.datetime.date(0), time(hour=15))
        )
        self.orders.append(
            {
                "symbol": order.data._name,
                "side": "buy" if order.isbuy() else "sell",
                "datetime": executed_at,
                "price": float(order.executed.price),
                "size": float(order.executed.size),
                "value": float(order.executed.value),
                "commission": float(order.executed.comm),
            }
        )

    def get_analysis(self) -> list[dict[str, object]]:
        return self.orders


class _DailyPortfolioAnalyzer(bt.Analyzer):
    def start(self) -> None:
        self.snapshots: list[dict[str, object]] = []
        self.previous_value = float(
            getattr(self.strategy.broker, "startingcash", self.strategy.broker.getvalue())
        )

    def next(self) -> None:
        current_date = self.strategy.datas[0].datetime.date(0)
        total_value = float(self.strategy.broker.getvalue())
        positions: list[dict[str, object]] = []
        for data in self.strategy.datas:
            position = self.strategy.getposition(data)
            size = float(position.size)
            if size == 0:
                continue
            close_price = float(data.close[0])
            positions.append(
                {
                    "symbol": data._name,
                    "size": size,
                    "close_price": close_price,
                    "market_value": size * close_price,
                    "unrealized_pnl": (close_price - float(position.price)) * size,
                }
            )
        self.snapshots.append(
            {
                "date": current_date,
                "cash": float(self.strategy.broker.getcash()),
                "total_value": total_value,
                "daily_pnl": total_value - self.previous_value,
                "positions": positions,
            }
        )
        self.previous_value = total_value

    def get_analysis(self) -> list[dict[str, object]]:
        return self.snapshots


def _load_market_data_feed(
    *,
    symbol: str,
    backtest: StrategyBacktestRecord,
) -> tuple[bt.feeds.PandasData, pd.DataFrame]:
    try:
        result = load_backtest_market_frame(
            symbol=symbol,
            start_date=backtest.config.start_date,
            end_date=backtest.config.end_date,
        )
    except StrategyBacktestError:
        raise
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

    peak = Decimal(str(equity_points[0]["value"]))
    peak_date = equity_points[0]["date"]
    max_drawdown = Decimal("0")
    max_start: date | None = None
    max_end: date | None = None
    drawdown_points: list[dict[str, object]] = []
    returns: list[Decimal] = []
    previous = Decimal(str(equity_points[0]["value"]))
    for point in equity_points:
        current_date = point["date"]
        value = Decimal(str(point["value"]))
        if value > peak:
            peak = value
            peak_date = current_date
        drawdown = (value / peak - Decimal("1")) * Decimal("100")
        if drawdown < max_drawdown:
            max_drawdown = drawdown
            max_start = current_date if not isinstance(peak_date, date) else peak_date
            max_end = current_date if isinstance(current_date, date) else None
        drawdown_points.append(
            {
                "date": current_date,
                "value": drawdown,
                "peak_value": peak,
                "equity_value": value,
            }
        )
        if value != previous:
            returns.append(value / previous - Decimal("1"))
        previous = value

    sharpe = _sharpe_ratio(returns)
    winning = [item for item in trade_items if float(item["pnl"]) > 0]
    win_rate = (
        Decimal(len(winning)) / Decimal(len(trade_items)) * Decimal("100")
        if trade_items
        else None
    )
    duration = (max_end - max_start).days if max_start is not None and max_end is not None else None
    metrics = StrategyBacktestMetrics(
        initial_value=_quantize(initial),
        final_value=_quantize(final),
        total_return_pct=_quantize(total_return),
        annual_return_pct=_quantize(annual_return),
        max_drawdown_pct=_quantize(max_drawdown),
        max_drawdown_start=max_start,
        max_drawdown_end=max_end,
        max_drawdown_duration_days=duration,
        sharpe_ratio=_quantize(sharpe) if sharpe is not None else None,
        win_rate_pct=_quantize(win_rate) if win_rate is not None else None,
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
            value=_quantize(point["value"]),
            normalized_value=None,
            extra={
                key: str(_quantize(value))
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
            open=_quantize(row["open"]),
            high=_quantize(row["high"]),
            low=_quantize(row["low"]),
            close=_quantize(row["close"]),
            volume=_quantize(row["volume"], "0.000001"),
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
                size=_quantize(position["size"], "0.000001"),
                close_price=_quantize(position["close_price"]),
                market_value=_quantize(position["market_value"]),
                unrealized_pnl=_quantize(position["unrealized_pnl"]),
            )
            for position in item["positions"]
            if isinstance(position, dict)
        ]
        snapshots.append(
            StrategyDailyPortfolioSnapshot(
                date=item["date"],
                cash=_quantize(item["cash"]),
                total_value=_quantize(item["total_value"]),
                daily_pnl=_quantize(item["daily_pnl"]),
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
        result = load_backtest_benchmark_frame(
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
            value=_quantize(row["close"]),
            normalized_value=_quantize(
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


def _sharpe_ratio(returns: list[Decimal]) -> Decimal | None:
    if len(returns) < 2:
        return None
    mean = sum(returns) / Decimal(len(returns))
    variance = sum((item - mean) ** 2 for item in returns) / Decimal(len(returns) - 1)
    stddev = Decimal(str(math.sqrt(float(variance))))
    if stddev == 0:
        return None
    return mean / stddev * Decimal(str(math.sqrt(252)))


def _quantize(value: Decimal | float | int | str | object, scale: str = "0.0001") -> Decimal:
    return Decimal(str(value)).quantize(Decimal(scale), rounding=ROUND_HALF_UP)


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"
