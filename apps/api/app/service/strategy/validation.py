from __future__ import annotations

import ast
import csv
import math
from datetime import date, timedelta
from pathlib import Path

import backtrader as bt

from app.core.config import get_settings
from app.schema.strategy import StrategyMode, StrategyValidationIssue
from app.service.strategy.protocol import (
    StrategyProtocolError,
    StrategyProtocolSpec,
    parse_strategy_source,
    with_backtrader_params,
)

_BANNED_IMPORT_PREFIXES = {
    "aiohttp",
    "akshare",
    "httpx",
    "os",
    "pathlib",
    "requests",
    "socket",
    "subprocess",
    "tushare",
    "urllib",
}
_BANNED_CALL_NAMES = {"__import__", "compile", "eval", "exec", "input", "open"}
_BANNED_ATTRIBUTE_CALLS = {
    ("os", "popen"),
    ("os", "remove"),
    ("os", "rename"),
    ("os", "system"),
    ("pathlib", "Path"),
    ("subprocess", "call"),
    ("subprocess", "check_call"),
    ("subprocess", "check_output"),
    ("subprocess", "Popen"),
    ("subprocess", "run"),
}


class StrategyAvailabilityError(Exception):
    def __init__(self, issues: list[StrategyValidationIssue]) -> None:
        self.issues = issues
        self.message = _format_issue_summary(issues)
        super().__init__(self.message)


def validate_strategy_availability(
    source_code: str,
    *,
    strategy_mode: StrategyMode,
) -> StrategyProtocolSpec:
    issues = _inspect_source_rules(source_code)
    if issues:
        raise StrategyAvailabilityError(issues)

    try:
        spec = parse_strategy_source(source_code)
    except StrategyProtocolError as exc:
        raise StrategyAvailabilityError(
            [
                StrategyValidationIssue(
                    code=exc.error_code,
                    message=exc.message,
                )
            ]
        ) from exc

    lifecycle_issue = _inspect_strategy_lifecycle(spec.strategy_cls)
    if lifecycle_issue is not None:
        raise StrategyAvailabilityError([lifecycle_issue])

    try:
        _run_smoke_backtest(spec, strategy_mode=strategy_mode)
    except Exception as exc:
        raise StrategyAvailabilityError(
            [
                StrategyValidationIssue(
                    code="STRATEGY_SMOKE_RUN_FAILED",
                    message=f"Strategy smoke backtest failed: {exc}",
                    detail={"exception_type": type(exc).__name__},
                )
            ]
        ) from exc

    return spec


def _inspect_source_rules(source_code: str) -> list[StrategyValidationIssue]:
    try:
        tree = ast.parse(source_code)
    except SyntaxError as exc:
        return [
            StrategyValidationIssue(
                code="STRATEGY_SYNTAX_INVALID",
                message=exc.msg,
                detail={"line": exc.lineno or 0, "offset": exc.offset or 0},
            )
        ]

    issues: list[StrategyValidationIssue] = []
    aliases = _import_aliases(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if _is_banned_module(alias.name):
                    issues.append(_banned_import_issue(alias.name, node.lineno))
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if _is_banned_module(module):
                issues.append(_banned_import_issue(module, node.lineno))
        elif isinstance(node, ast.Call):
            issue = _inspect_call(node, aliases)
            if issue is not None:
                issues.append(issue)
    return issues


def _inspect_strategy_lifecycle(strategy_cls: type[bt.Strategy]) -> StrategyValidationIssue | None:
    trading_methods = {"next", "next_open", "nextstart", "prenext"}
    for cls in strategy_cls.__mro__:
        if cls is bt.Strategy:
            break
        if any(name in cls.__dict__ for name in trading_methods):
            return None
    return StrategyValidationIssue(
        code="STRATEGY_NO_TRADING_METHOD",
        message="Strategy must implement next, next_open, nextstart, or prenext",
    )


def _run_smoke_backtest(spec: StrategyProtocolSpec, *, strategy_mode: StrategyMode) -> None:
    strategy_cls = with_backtrader_params(spec.strategy_cls, spec.custom_params)
    symbols = _symbols_for_mode(strategy_mode)
    bar_count = _bar_count_for_params(spec)
    data_dir = _sample_data_dir()
    cerebro = bt.Cerebro(stdstats=False)
    cerebro.broker.setcash(100000.0)
    cerebro.broker.setcommission(commission=0.001)

    for index, symbol in enumerate(symbols):
        path = _ensure_sample_csv(data_dir, symbol=symbol, profile_index=index, bar_count=bar_count)
        cerebro.adddata(
            bt.feeds.GenericCSVData(
                dataname=str(path),
                dtformat="%Y-%m-%d",
                datetime=0,
                open=1,
                high=2,
                low=3,
                close=4,
                volume=5,
                openinterest=6,
                headers=True,
            ),
            name=symbol,
        )

    cerebro.addstrategy(strategy_cls)
    result = cerebro.run(runonce=False)
    if not result:
        raise RuntimeError("Backtrader returned no strategy instances")


def _import_aliases(tree: ast.AST) -> dict[str, str]:
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                aliases[alias.asname or alias.name.split(".")[0]] = alias.name
        elif isinstance(node, ast.ImportFrom) and node.module:
            for alias in node.names:
                aliases[alias.asname or alias.name] = f"{node.module}.{alias.name}"
    return aliases


def _inspect_call(node: ast.Call, aliases: dict[str, str]) -> StrategyValidationIssue | None:
    if isinstance(node.func, ast.Name) and node.func.id in _BANNED_CALL_NAMES:
        return StrategyValidationIssue(
            code="STRATEGY_DANGEROUS_CALL",
            message=f"Strategy source cannot call {node.func.id}",
            detail={"line": node.lineno, "call": node.func.id},
        )
    if isinstance(node.func, ast.Attribute):
        root_name = _attribute_root_name(node.func)
        attr_name = node.func.attr
        resolved_root = aliases.get(root_name, root_name).split(".")[0] if root_name else ""
        if (resolved_root, attr_name) in _BANNED_ATTRIBUTE_CALLS:
            return StrategyValidationIssue(
                code="STRATEGY_DANGEROUS_CALL",
                message=f"Strategy source cannot call {resolved_root}.{attr_name}",
                detail={"line": node.lineno, "call": f"{resolved_root}.{attr_name}"},
            )
    return None


def _attribute_root_name(node: ast.Attribute) -> str | None:
    value = node.value
    while isinstance(value, ast.Attribute):
        value = value.value
    return value.id if isinstance(value, ast.Name) else None


def _is_banned_module(module_name: str) -> bool:
    root = module_name.split(".")[0]
    return root in _BANNED_IMPORT_PREFIXES


def _banned_import_issue(module_name: str, line: int) -> StrategyValidationIssue:
    root = module_name.split(".")[0]
    code = (
        "STRATEGY_EXTERNAL_DATA_ACCESS"
        if root in {"akshare", "tushare"}
        else "STRATEGY_DANGEROUS_IMPORT"
    )
    return StrategyValidationIssue(
        code=code,
        message=f"Strategy source cannot import {module_name}",
        detail={"line": line, "module": module_name},
    )


def _symbols_for_mode(strategy_mode: StrategyMode) -> list[str]:
    if strategy_mode == StrategyMode.SINGLE_SYMBOL:
        return ["600519.SH"]
    if strategy_mode == StrategyMode.UNIVERSE_SELECTION:
        return ["600519.SH", "000001.SZ", "000858.SZ", "300750.SZ", "601318.SH"]
    return ["600519.SH", "000001.SZ", "000858.SZ"]


def _bar_count_for_params(spec: StrategyProtocolSpec) -> int:
    max_period = 0
    for param in spec.custom_params:
        if param.type in {"integer", "number"} and isinstance(param.default, int | float):
            max_period = max(max_period, int(param.default))
    return min(max(260, max_period + 40), 520)


def _sample_data_dir() -> Path:
    settings = get_settings()
    return settings.database_path.parent / "strategy-validation" / "market-data"


def _ensure_sample_csv(
    data_dir: Path,
    *,
    symbol: str,
    profile_index: int,
    bar_count: int,
) -> Path:
    data_dir.mkdir(parents=True, exist_ok=True)
    path = data_dir / f"{symbol.replace('.', '_')}_{bar_count}.csv"
    if path.exists():
        return path

    start = date(2023, 1, 2)
    base = 40.0 + profile_index * 17.0
    drift = 0.025 + profile_index * 0.004
    amplitude = 1.5 + profile_index * 0.35
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["date", "open", "high", "low", "close", "volume", "openinterest"])
        previous_close = base
        for index in range(bar_count):
            current_date = start + timedelta(days=index)
            close = base + drift * index + amplitude * math.sin(index / (7.0 + profile_index))
            open_price = previous_close
            high = max(open_price, close) * 1.01
            low = min(open_price, close) * 0.99
            volume = 1_000_000 + profile_index * 100_000 + index * 1000
            writer.writerow(
                [
                    current_date.isoformat(),
                    f"{open_price:.4f}",
                    f"{high:.4f}",
                    f"{low:.4f}",
                    f"{close:.4f}",
                    volume,
                    0,
                ]
            )
            previous_close = close
    return path


def _format_issue_summary(issues: list[StrategyValidationIssue]) -> str:
    if not issues:
        return "Strategy availability check failed"
    first = issues[0]
    if len(issues) == 1:
        return first.message
    return f"{first.message}; and {len(issues) - 1} more issue(s)"
