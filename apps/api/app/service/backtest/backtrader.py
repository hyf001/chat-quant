from __future__ import annotations

import math
import sys
from collections.abc import Callable
from datetime import date, datetime, time
from decimal import ROUND_HALF_UP, Decimal
from types import ModuleType
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


class BacktraderStrategyBacktestEngine:
    name = "backtrader"
    protocol_name = "chatq_backtrader_strategy_v1"

    def execute(
        self,
        *,
        backtest: StrategyBacktestRecord,
        version: StrategyVersionRecord,
    ) -> StrategyBacktestResultRecord:
        module_name = f"chatq_strategy_{uuid4().hex}"
        try:
            strategy_cls = self._load_strategy_class(version, module_name)
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
            data_source={
                "mode": "akshare_ohlcv",
                "asset_class": backtest.config.asset_class,
                "market": backtest.config.market,
                "symbols": backtest.config.symbols,
                "timeframe": backtest.config.timeframe,
                "data_adjust": backtest.config.data_adjust,
            },
        )

    def _load_strategy_class(
        self,
        version: StrategyVersionRecord,
        module_name: str,
    ) -> type[bt.Strategy]:
        module = ModuleType(module_name)
        module.__file__ = f"<{module_name}>"
        sys.modules[module_name] = module
        try:
            compiled = compile(version.source_code, module.__file__, "exec")
            exec(compiled, module.__dict__)
        except StrategyBacktestError:
            raise
        except Exception as exc:
            raise StrategyBacktestError(
                "STRATEGY_IMPORT_FAILED",
                str(exc),
                detail={"exception_type": type(exc).__name__},
            ) from exc

        strategy_classes = [
            value
            for value in module.__dict__.values()
            if (
                isinstance(value, type)
                and issubclass(value, bt.Strategy)
                and value is not bt.Strategy
            )
        ]
        if not strategy_classes:
            raise StrategyBacktestError(
                "STRATEGY_PROTOCOL_INVALID",
                "Source code must define a backtrader.Strategy subclass",
            )
        if len(strategy_classes) > 1:
            raise StrategyBacktestError(
                "STRATEGY_PROTOCOL_INVALID",
                "Source code must define exactly one backtrader.Strategy subclass",
            )
        return strategy_classes[0]


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
        raw_frame = _fetch_akshare_history(
            symbol=symbol,
            market=backtest.config.market,
            asset_class=backtest.config.asset_class,
            start_date=backtest.config.start_date,
            end_date=backtest.config.end_date,
            adjust=backtest.config.data_adjust,
        )
        frame = _normalize_ohlcv_frame(raw_frame)
    except StrategyBacktestError:
        raise
    except Exception as exc:
        raise StrategyBacktestError(
            "STRATEGY_DATA_FETCH_FAILED",
            f"Failed to load market data for {symbol}: {exc}",
            detail={
                "symbol": symbol,
                "market": backtest.config.market,
                "asset_class": backtest.config.asset_class,
                "exception_type": type(exc).__name__,
            },
        ) from exc

    if frame.empty:
        raise StrategyBacktestError(
            "STRATEGY_DATA_EMPTY",
            f"No market data returned for {symbol}",
            detail={
                "symbol": symbol,
                "market": backtest.config.market,
                "asset_class": backtest.config.asset_class,
                "start_date": backtest.config.start_date.isoformat(),
                "end_date": backtest.config.end_date.isoformat(),
            },
        )
    return bt.feeds.PandasData(dataname=frame), frame


def _fetch_akshare_history(
    *,
    symbol: str,
    market: str,
    asset_class: str,
    start_date: date,
    end_date: date,
    adjust: str,
) -> pd.DataFrame:
    import akshare as ak

    start = start_date.strftime("%Y%m%d")
    end = end_date.strftime("%Y%m%d")
    normalized_symbol = _normalize_akshare_symbol(symbol, market=market, asset_class=asset_class)
    normalized_adjust = "" if adjust == "none" else adjust

    if market == "CN" and asset_class == "stock":
        return _fetch_cn_stock_history(
            ak=ak,
            symbol=symbol,
            normalized_symbol=normalized_symbol,
            start_date=start,
            end_date=end,
            adjust=normalized_adjust,
        )
    if market == "CN" and asset_class == "etf":
        return ak.fund_etf_hist_em(
            symbol=normalized_symbol,
            period="daily",
            start_date=start,
            end_date=end,
            adjust=normalized_adjust,
        )
    if market == "CN" and asset_class == "index":
        return _fetch_cn_index_history(
            ak=ak,
            symbol=symbol,
            normalized_symbol=normalized_symbol,
            start_date=start,
            end_date=end,
        )
    if market == "HK" and asset_class == "stock":
        return ak.stock_hk_hist(
            symbol=normalized_symbol,
            period="daily",
            start_date=start,
            end_date=end,
            adjust=normalized_adjust,
        )
    if market == "US" and asset_class == "stock":
        if "." not in normalized_symbol:
            raise StrategyBacktestError(
                "STRATEGY_DATA_SYMBOL_UNSUPPORTED",
                "US stocks require an AKShare stock_us_hist code, for example 105.MSFT",
                detail={"symbol": symbol},
            )
        return ak.stock_us_hist(
            symbol=normalized_symbol,
            period="daily",
            start_date=start,
            end_date=end,
            adjust=normalized_adjust,
        )
    raise StrategyBacktestError(
        "STRATEGY_DATA_SOURCE_UNSUPPORTED",
        "No real market data adapter is configured for this market and asset class",
        detail={"market": market, "asset_class": asset_class},
    )


def _fetch_cn_stock_history(
    *,
    ak: object,
    symbol: str,
    normalized_symbol: str,
    start_date: str,
    end_date: str,
    adjust: str,
) -> pd.DataFrame:
    exchange_symbol = _cn_exchange_symbol(symbol)
    attempts: list[tuple[str, Callable[[], pd.DataFrame]]] = [
        (
            "stock_zh_a_hist",
            lambda: ak.stock_zh_a_hist(
                symbol=normalized_symbol,
                period="daily",
                start_date=start_date,
                end_date=end_date,
                adjust=adjust,
                timeout=15,
            ),
        ),
        (
            "stock_zh_a_hist_tx",
            lambda: ak.stock_zh_a_hist_tx(
                symbol=exchange_symbol,
                start_date=start_date,
                end_date=end_date,
                adjust=adjust,
                timeout=15,
            ),
        ),
        (
            "stock_zh_a_daily",
            lambda: ak.stock_zh_a_daily(
                symbol=exchange_symbol,
                start_date=start_date,
                end_date=end_date,
                adjust=adjust,
            ),
        ),
    ]
    errors: list[dict[str, str]] = []
    for source_name, fetch in attempts:
        try:
            frame = fetch()
        except Exception as exc:  # noqa: BLE001 - collect provider failures and try the next source.
            errors.append(
                {
                    "source": source_name,
                    "exception_type": type(exc).__name__,
                    "message": str(exc),
                }
            )
            continue
        if not frame.empty:
            return frame
        errors.append({"source": source_name, "exception_type": "EmptyDataFrame", "message": ""})

    raise StrategyBacktestError(
        "STRATEGY_DATA_FETCH_FAILED",
        f"Failed to load CN stock market data for {symbol}",
        detail={"symbol": symbol, "attempts": errors},
    )


def _fetch_cn_index_history(
    *,
    ak: object,
    symbol: str,
    normalized_symbol: str,
    start_date: str,
    end_date: str,
) -> pd.DataFrame:
    exchange_symbol = _cn_exchange_symbol(symbol)
    attempts: list[tuple[str, Callable[[], pd.DataFrame]]] = [
        (
            "index_zh_a_hist",
            lambda: ak.index_zh_a_hist(
                symbol=normalized_symbol,
                period="daily",
                start_date=start_date,
                end_date=end_date,
            ),
        ),
        (
            "stock_zh_index_daily_tx",
            lambda: ak.stock_zh_index_daily_tx(
                symbol=exchange_symbol,
                start_date=start_date,
                end_date=end_date,
            ),
        ),
    ]
    errors: list[dict[str, str]] = []
    for source_name, fetch in attempts:
        try:
            frame = fetch()
        except Exception as exc:  # noqa: BLE001 - collect provider failures and try the next source.
            errors.append(
                {
                    "source": source_name,
                    "exception_type": type(exc).__name__,
                    "message": str(exc),
                }
            )
            continue
        if not frame.empty:
            return frame
        errors.append({"source": source_name, "exception_type": "EmptyDataFrame", "message": ""})

    raise StrategyBacktestError(
        "STRATEGY_DATA_FETCH_FAILED",
        f"Failed to load CN index market data for {symbol}",
        detail={"symbol": symbol, "attempts": errors},
    )


def _normalize_akshare_symbol(symbol: str, *, market: str, asset_class: str) -> str:
    value = symbol.strip().upper()
    if market == "CN":
        if value.startswith(("SH", "SZ", "BJ")):
            return value[2:]
        if value.endswith((".SH", ".SZ", ".BJ")):
            return value.split(".", 1)[0]
        return value
    if market == "HK":
        if value.startswith("HK"):
            value = value[2:]
        if value.endswith(".HK"):
            value = value[:-3]
        return value.zfill(5) if value.isdigit() else value
    return value


def _cn_exchange_symbol(symbol: str) -> str:
    value = symbol.strip().upper()
    if value.startswith(("SH", "SZ", "BJ")):
        return value.lower()
    if value.endswith((".SH", ".SZ", ".BJ")):
        code, exchange = value.split(".", 1)
        return f"{exchange.lower()}{code}"
    if value.startswith("6"):
        return f"sh{value}"
    if value.startswith(("0", "3")):
        return f"sz{value}"
    if value.startswith(("4", "8")):
        return f"bj{value}"
    return value.lower()


def _normalize_ohlcv_frame(raw_frame: pd.DataFrame) -> pd.DataFrame:
    required_columns = _ohlcv_column_mapping(raw_frame)
    missing = [column for column in required_columns if column not in raw_frame.columns]
    if missing:
        raise StrategyBacktestError(
            "STRATEGY_DATA_FORMAT_INVALID",
            "Market data does not contain required OHLCV columns",
            detail={"missing_columns": missing},
        )

    frame = raw_frame.rename(columns=required_columns)
    frame = frame[list(required_columns.values())].copy()
    frame["datetime"] = pd.to_datetime(frame["datetime"])
    for column in ["open", "high", "low", "close", "volume"]:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    frame = frame.dropna(subset=["datetime", "open", "high", "low", "close", "volume"])
    frame = frame.sort_values("datetime").set_index("datetime")
    frame["openinterest"] = 0
    return frame[["open", "high", "low", "close", "volume", "openinterest"]]


def _ohlcv_column_mapping(raw_frame: pd.DataFrame) -> dict[str, str]:
    chinese_columns = {
        "日期": "datetime",
        "开盘": "open",
        "最高": "high",
        "最低": "low",
        "收盘": "close",
        "成交量": "volume",
    }
    if all(column in raw_frame.columns for column in chinese_columns):
        return chinese_columns

    english_columns = {
        "date": "datetime",
        "open": "open",
        "high": "high",
        "low": "low",
        "close": "close",
        "volume": "volume",
    }
    if all(column in raw_frame.columns for column in english_columns):
        return english_columns

    english_amount_columns = {
        "date": "datetime",
        "open": "open",
        "high": "high",
        "low": "low",
        "close": "close",
        "amount": "volume",
    }
    if all(column in raw_frame.columns for column in english_amount_columns):
        return english_amount_columns

    return english_columns


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
        raw_frame = _fetch_akshare_history(
            symbol=benchmark_symbol,
            market=backtest.config.market,
            asset_class=_benchmark_asset_class(backtest.config.market),
            start_date=backtest.config.start_date,
            end_date=backtest.config.end_date,
            adjust=backtest.config.data_adjust,
        )
        frame = _normalize_ohlcv_frame(raw_frame)
    except Exception as exc:  # noqa: BLE001 - benchmark is comparative context, not core execution.
        warnings.append(f"基准 {benchmark_symbol} 行情加载失败：{exc}")
        return None

    if frame.empty:
        warnings.append(f"基准 {benchmark_symbol} 没有返回行情")
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


def _benchmark_asset_class(market: str) -> str:
    return "index" if market == "CN" else "stock"


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
