from __future__ import annotations

import importlib.util
import math
import sys
import tempfile
from datetime import date, datetime, time, timedelta
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path
from uuid import uuid4

import backtrader as bt
import pandas as pd

from app.domain.backtests.execution import StrategyBacktestError
from app.domain.backtests.models import (
    CurveType,
    StrategyBacktestMetrics,
    StrategyBacktestRecord,
    StrategyBacktestResultRecord,
    StrategyCurve,
    StrategyCurvePoint,
    StrategyTradeRecord,
    TradeSide,
    TradeStatus,
)
from app.domain.strategies.models import StrategyVersionRecord


class BacktraderStrategyBacktestEngine:
    name = "backtrader"
    protocol_name = "chatq_backtrader_strategy_v1"

    def execute(
        self,
        *,
        backtest: StrategyBacktestRecord,
        version: StrategyVersionRecord,
    ) -> StrategyBacktestResultRecord:
        if not version.code_files:
            raise StrategyBacktestError(
                "STRATEGY_CODE_MISSING",
                "Strategy version does not contain executable code_files",
            )

        module_name = f"chatq_strategy_{uuid4().hex}"
        try:
            with tempfile.TemporaryDirectory(prefix="chatq_strategy_") as tmp_dir_text:
                strategy_cls = self._load_strategy_class(version, Path(tmp_dir_text), module_name)
                cerebro = bt.Cerebro(stdstats=False)
                cerebro.broker.setcash(float(backtest.config.initial_cash))
                cerebro.broker.setcommission(commission=float(backtest.config.commission))
                if backtest.config.slippage > 0:
                    cerebro.broker.set_slippage_perc(float(backtest.config.slippage))

                for symbol in backtest.config.symbols:
                    data = _build_synthetic_daily_feed(
                        symbol=symbol,
                        start_date=backtest.config.start_date,
                        end_date=backtest.config.end_date,
                    )
                    cerebro.adddata(data, name=symbol)

                params = {key: value for key, value in backtest.config.params.items()}
                cerebro.addstrategy(strategy_cls, **params)
                cerebro.addanalyzer(_EquityCurveAnalyzer, _name="equity_curve")
                cerebro.addanalyzer(_ClosedTradeAnalyzer, _name="closed_trades")
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
        trade_items = strategy.analyzers.closed_trades.get_analysis()
        metrics, drawdown_points = _build_metrics(backtest, equity_points, trade_items)

        result_id = _new_id("srr")
        trades = [
            StrategyTradeRecord(
                id=_new_id("strd"),
                strategy_backtest_id=backtest.id,
                symbol=item["symbol"],
                side=TradeSide.SELL if item["size"] >= 0 else TradeSide.COVER,
                status=TradeStatus.CLOSED,
                trade_datetime=datetime.combine(item["date"], time(hour=15)),
                price=_quantize(item["price"]),
                size=_quantize(abs(item["size"]), "0.000001"),
                value=_quantize(abs(item["value"])),
                pnl=_quantize(item["pnl"]),
                pnl_pct=_quantize(item["pnl_pct"]) if item["pnl_pct"] is not None else None,
                metadata={"basis": "backtrader_trade_notification"},
            )
            for item in trade_items
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
            warnings=[],
            engine=self.name,
            protocol=self.protocol_name,
            data_source={
                "mode": "synthetic_daily_ohlcv",
                "symbols": backtest.config.symbols,
                "timeframe": backtest.config.timeframe,
            },
        )

    def _load_strategy_class(
        self,
        version: StrategyVersionRecord,
        tmp_dir: Path,
        module_name: str,
    ) -> type[bt.Strategy]:
        module_path_text, class_name = version.entrypoint.split(":", maxsplit=1)
        for code_file in version.code_files:
            destination = tmp_dir / code_file.path
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(code_file.content, encoding="utf-8")

        source_path = tmp_dir / module_path_text
        if not source_path.is_file():
            raise StrategyBacktestError(
                "STRATEGY_ENTRYPOINT_NOT_FOUND",
                "Strategy entrypoint file was not found",
            )

        sys.path.insert(0, str(tmp_dir))
        try:
            spec = importlib.util.spec_from_file_location(module_name, source_path)
            if spec is None or spec.loader is None:
                raise StrategyBacktestError(
                    "STRATEGY_IMPORT_FAILED",
                    "Strategy entrypoint could not be imported",
                )
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
        finally:
            try:
                sys.path.remove(str(tmp_dir))
            except ValueError:
                pass

        strategy_cls = getattr(module, class_name, None)
        if not isinstance(strategy_cls, type) or not issubclass(strategy_cls, bt.Strategy):
            raise StrategyBacktestError(
                "STRATEGY_PROTOCOL_INVALID",
                "Entrypoint class must subclass backtrader.Strategy",
            )
        return strategy_cls


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


def _build_synthetic_daily_feed(
    *,
    symbol: str,
    start_date: date,
    end_date: date,
) -> bt.feeds.PandasData:
    rows: list[dict[str, float]] = []
    dates: list[datetime] = []
    days = max(1, (end_date - start_date).days)
    symbol_factor = (sum(ord(char) for char in symbol) % 11) / 10000
    close = 100 + (sum(ord(char) for char in symbol) % 17)
    for offset in range(days + 1):
        current_date = start_date + timedelta(days=offset)
        seasonal = math.sin(offset / 4) * 0.008
        trend = 0.0015 + symbol_factor
        shock = -0.012 if offset and offset % 19 == 0 else 0.002
        open_price = close
        close = max(1, close * (1 + trend + seasonal + shock))
        high = max(open_price, close) * 1.006
        low = min(open_price, close) * 0.994
        rows.append(
            {
                "open": open_price,
                "high": high,
                "low": low,
                "close": close,
                "volume": 1000000 + offset * 100,
                "openinterest": 0,
            }
        )
        dates.append(datetime.combine(current_date, time()))
    frame = pd.DataFrame(rows, index=pd.DatetimeIndex(dates))
    return bt.feeds.PandasData(dataname=frame)


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
