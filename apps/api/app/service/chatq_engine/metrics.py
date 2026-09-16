"""收益 / 回撤 / Sharpe / 胜率口径，回测与训练共用。

这里只放纯数字函数，不引入任何 schema、数据库或 HTTP 依赖；调用方负责把结果
装进自己的响应模型（回测用 ``StrategyBacktestMetrics``，训练用单局报告）。
"""

from __future__ import annotations

import math
from datetime import date
from decimal import ROUND_HALF_UP, Decimal
from typing import Any


def quantize(value: Decimal | float | int | str | object, scale: str = "0.0001") -> Decimal:
    return Decimal(str(value)).quantize(Decimal(scale), rounding=ROUND_HALF_UP)


def sharpe_ratio(returns: list[Decimal]) -> Decimal | None:
    if len(returns) < 2:
        return None
    mean = sum(returns) / Decimal(len(returns))
    variance = sum((item - mean) ** 2 for item in returns) / Decimal(len(returns) - 1)
    stddev = Decimal(str(math.sqrt(float(variance))))
    if stddev == 0:
        return None
    return mean / stddev * Decimal(str(math.sqrt(252)))


def equity_returns(equity_points: list[dict[str, Any]]) -> list[Decimal]:
    """逐点收益（只在权益变化时计入，与回测口径一致）。"""
    returns: list[Decimal] = []
    previous = Decimal(str(equity_points[0]["value"])) if equity_points else Decimal("0")
    for point in equity_points[1:]:
        value = Decimal(str(point["value"]))
        if value != previous:
            returns.append(value / previous - Decimal("1"))
        previous = value
    return returns


def drawdown_analysis(
    equity_points: list[dict[str, Any]],
) -> tuple[Decimal, date | None, date | None, list[dict[str, Any]]]:
    """最大回撤 + 回撤曲线，口径与回测一致。"""
    if not equity_points:
        return Decimal("0"), None, None, []

    peak = Decimal(str(equity_points[0]["value"]))
    peak_date = equity_points[0]["date"]
    max_drawdown = Decimal("0")
    max_start: date | None = None
    max_end: date | None = None
    drawdown_points: list[dict[str, Any]] = []
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
    return max_drawdown, max_start, max_end, drawdown_points


def win_rate_pct(
    trade_items: list[dict[str, Any]],
    *,
    pnl_key: str = "pnl",
) -> Decimal | None:
    if not trade_items:
        return None
    winning = [item for item in trade_items if float(item[pnl_key]) > 0]
    return Decimal(len(winning)) / Decimal(len(trade_items)) * Decimal("100")


def total_return_pct(initial: Decimal | float | str, final: Decimal | float | str) -> Decimal:
    start = Decimal(str(initial))
    end = Decimal(str(final))
    return (end / start - Decimal("1")) * Decimal("100")
