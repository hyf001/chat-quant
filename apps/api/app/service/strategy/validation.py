from __future__ import annotations

import ast

from app.schema.strategy import StrategyMode, StrategyValidationIssue
from app.service.strategy.protocol import (
    StrategyProtocolError,
    StrategyProtocolSpec,
    parse_strategy_source,
)

_BANNED_IMPORT_PREFIXES = {
    "aiohttp",
    "akshare",
    "backtrader",
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
    del strategy_mode
    issues = _inspect_source_rules(source_code)
    if issues:
        raise StrategyAvailabilityError(issues)

    try:
        return parse_strategy_source(source_code)
    except StrategyProtocolError as exc:
        raise StrategyAvailabilityError(
            [
                StrategyValidationIssue(
                    code=exc.error_code,
                    message=exc.message,
                )
            ]
        ) from exc


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
    if root in {"akshare", "tushare"}:
        code = "STRATEGY_EXTERNAL_DATA_ACCESS"
    elif root == "backtrader":
        code = "STRATEGY_BACKTRADER_IMPORT_FORBIDDEN"
    else:
        code = "STRATEGY_DANGEROUS_IMPORT"
    return StrategyValidationIssue(
        code=code,
        message=f"Strategy source cannot import {module_name}",
        detail={"line": line, "module": module_name},
    )


def _format_issue_summary(issues: list[StrategyValidationIssue]) -> str:
    if not issues:
        return "Strategy availability check failed"
    first = issues[0]
    if len(issues) == 1:
        return first.message
    return f"{first.message}; and {len(issues) - 1} more issue(s)"
