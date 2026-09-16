"""出口脱敏：字段白名单 + 序号轴（设计方案 §5.2）。

数据库该存什么就存什么；脱敏只发生在 API 出口。训练期响应一律走这里的
``scrub_*``，保证 ``symbol`` / ``name`` / 真实日期不会被带出去。
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Any

INSTRUMENT_ALIAS = "标的A"

#: 训练期响应里不允许出现的字段名（finish / report 才揭晓）。
SENSITIVE_KEYS = frozenset(
    {
        "symbol",
        "symbols",
        "name",
        "trade_date",
        "date",
        "datetime",
        "slice_start",
        "slice_end",
        "started_date",
        "finished_date",
    }
)


def instrument_alias() -> str:
    return INSTRUMENT_ALIAS


def bar_payload(index: int, bar: Any) -> dict[str, Any]:
    """K 线 → 训练期白名单字段 ``{i, o, h, l, c, v}``。"""
    return {
        "i": index,
        "o": float(bar.open),
        "h": float(bar.high),
        "l": float(bar.low),
        "c": float(bar.close),
        "v": float(bar.volume),
    }


def revealed_bar_payload(index: int, bar: Any) -> dict[str, Any]:
    """复盘用 K 线（会话已揭晓）：在白名单字段之外补真实日期。"""
    payload = bar_payload(index, bar)
    payload["date"] = bar.trade_date.isoformat()
    return {"i": payload["i"], "date": payload["date"], **payload}


def marker_payload(fills: list[dict[str, Any]]) -> list[dict[str, Any]]:
    markers: list[dict[str, Any]] = []
    for fill in fills:
        side = str(fill["side"])
        markers.append(
            {
                "i": int(fill["i"]),
                "side": "buy" if side == "buy" else "sell",
                "text": "B" if side == "buy" else "S",
            }
        )
    return markers


def scrub_mapping(value: Any) -> Any:
    """递归剔掉敏感字段；出口的最后一道保险（响应模型本身已不含这些字段）。"""
    if isinstance(value, dict):
        return {
            key: scrub_mapping(item) for key, item in value.items() if key not in SENSITIVE_KEYS
        }
    if isinstance(value, list):
        return [scrub_mapping(item) for item in value]
    if isinstance(value, Decimal):
        return value
    if isinstance(value, date | datetime):
        return value.isoformat()
    return value


def find_leaks(value: Any, *, path: str = "") -> list[str]:
    """返回仍然暴露敏感字段的路径（测试与自检用）。"""
    leaks: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            current = f"{path}.{key}" if path else str(key)
            if key in SENSITIVE_KEYS:
                leaks.append(current)
            leaks.extend(find_leaks(item, path=current))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            leaks.extend(find_leaks(item, path=f"{path}[{index}]"))
    return leaks
