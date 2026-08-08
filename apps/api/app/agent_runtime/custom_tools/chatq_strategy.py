from __future__ import annotations

import argparse
import io
import json
import shlex
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from claude_agent_sdk import McpSdkServerConfig
from mcp.server import Server
from mcp.types import CallToolResult, TextContent, Tool
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from app.db.session import get_session_factory
from app.schema.agent_runtime import AgentExecutionCommand
from app.schema.backtest import StrategyBacktestConfig, StrategyBacktestProtocol
from app.schema.strategy import (
    StrategyCreate,
    StrategyMode,
    StrategyStatus,
    StrategyVersionCreate,
)
from app.service import backtest as backtest_service
from app.service import project as project_service
from app.service import strategy as strategy_service
from app.service.backtest import BacktestError
from app.service.project import ProjectNotFoundError
from app.service.strategy import StrategyError

CHATQ_STRATEGY_SERVER_NAME = "chatq"
CHATQ_STRATEGY_MCP_TOOL_NAME = "strategy"
CHATQ_STRATEGY_TOOL_NAME = f"mcp__{CHATQ_STRATEGY_SERVER_NAME}__{CHATQ_STRATEGY_MCP_TOOL_NAME}"

Operator = Literal[
    "list_strategies",
    "get_strategy",
    "list_versions",
    "get_version",
    "get_backtest_protocol",
    "create_strategy",
    "update_strategy",
    "create_version",
    "switch_version",
    "archive_strategy",
    "delete_strategy",
    "run_backtest",
    "list_backtests",
    "get_backtest",
]


class ChatqStrategyCommandRequest(BaseModel):
    command: str = Field(min_length=1)

    model_config = ConfigDict(extra="forbid")


class EmptyParams(BaseModel):
    model_config = ConfigDict(extra="forbid")


class StrategyIdParams(BaseModel):
    strategy_id: str = Field(min_length=1)

    model_config = ConfigDict(extra="forbid")


class VersionIdParams(BaseModel):
    version_id: str = Field(min_length=1)

    model_config = ConfigDict(extra="forbid")


class ListVersionsParams(StrategyIdParams):
    include_source_code: bool = False


class BacktestIdParams(BaseModel):
    backtest_id: str = Field(min_length=1)

    model_config = ConfigDict(extra="forbid")


class ListBacktestsParams(BaseModel):
    strategy_version_id: str | None = Field(default=None, min_length=1)
    limit: int = Field(default=20, ge=1, le=100)

    model_config = ConfigDict(extra="forbid")


class CreateStrategyParams(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    source_code: str = Field(min_length=1)
    description: str | None = None
    strategy_mode: StrategyMode = StrategyMode.SINGLE_SYMBOL
    risk_notes: list[str] = Field(default_factory=list)

    model_config = ConfigDict(extra="forbid")


class UpdateStrategyParams(StrategyIdParams):
    name: str | None = Field(default=None, min_length=1, max_length=128)
    description: str | None = None
    tags: list[str] | None = None
    status: StrategyStatus | None = None
    source_code: str | None = Field(default=None, min_length=1)
    strategy_mode: StrategyMode | None = None
    risk_notes: list[str] = Field(default_factory=list)


class CreateVersionParams(StrategyIdParams):
    source_code: str = Field(min_length=1)
    strategy_mode: StrategyMode | None = None
    risk_notes: list[str] = Field(default_factory=list)


class SwitchVersionParams(StrategyIdParams):
    strategy_version_id: str = Field(min_length=1)


class RunBacktestParams(StrategyIdParams):
    strategy_version_id: str | None = Field(default=None, min_length=1)
    config: dict[str, Any] = Field(default_factory=dict)


class ToolExecutionError(Exception):
    def __init__(
        self,
        error_code: str,
        message: str,
        *,
        detail: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.error_code = error_code
        self.message = message
        self.detail = detail or {}


@dataclass(frozen=True)
class ToolTextResult:
    text: str
    is_error: bool = False


def build_chatq_strategy_mcp_server(command: AgentExecutionCommand) -> object:
    server = Server(CHATQ_STRATEGY_SERVER_NAME, version="1.0.0")
    input_schema = {
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": (
                    "chatq-strategy style command line, for example: "
                    "strategy create --name '均线策略' --source-file strategy.py"
                ),
            },
        },
        "required": ["command"],
        "additionalProperties": False,
    }

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool.model_validate(
                {
                    "name": CHATQ_STRATEGY_MCP_TOOL_NAME,
                    "description": (
                        "Operate Chat-Quant strategies and backtests using a CLI-style "
                        "command string. Supports --help and normal --flag arguments. "
                        "The current project is supplied by Chat-Quant; do not pass "
                        "project_id, user_id, or project_path."
                    ),
                    "inputSchema": input_schema,
                }
            )
        ]

    @server.call_tool(validate_input=False)
    async def call_tool(name: str, arguments: dict[str, Any]) -> CallToolResult:
        if name != CHATQ_STRATEGY_MCP_TOOL_NAME:
            raise ValueError(f"Tool not found: {name}")
        result = await handle_chatq_strategy_tool(command, arguments)
        return CallToolResult(
            content=[TextContent(type="text", text=result.text)],
            isError=result.is_error,
        )

    return McpSdkServerConfig(
        type="sdk",
        name=CHATQ_STRATEGY_SERVER_NAME,
        instance=server,
    )


async def handle_chatq_strategy_tool(
    command: AgentExecutionCommand,
    args: dict[str, Any],
) -> ToolTextResult:
    try:
        request = ChatqStrategyCommandRequest.model_validate(args)
        return await execute_chatq_strategy_command(command, request.command)
    except ValidationError as exc:
        return ToolTextResult(
            _format_cli_error(
                "chatq_strategy input is invalid",
                detail=_jsonable(exc.errors()),
            ),
            is_error=True,
        )
    except (StrategyError, BacktestError) as exc:
        return ToolTextResult(_format_cli_error(exc.message, getattr(exc, "detail", None)), True)
    except ProjectNotFoundError:
        return ToolTextResult(_format_cli_error("Project not found"), True)
    except ToolExecutionError as exc:
        return ToolTextResult(_format_cli_error(exc.message, exc.detail), True)


async def execute_chatq_strategy_command(
    command: AgentExecutionCommand,
    command_line: str,
) -> ToolTextResult:
    try:
        argv = shlex.split(command_line)
    except ValueError as exc:
        return ToolTextResult(_format_cli_error(f"Failed to parse command: {exc}"), True)
    return await execute_chatq_strategy_argv(command, argv)


async def execute_chatq_strategy_argv(
    command: AgentExecutionCommand,
    argv: list[str],
) -> ToolTextResult:
    parser = build_command_parser()
    stdout = io.StringIO()
    stderr = io.StringIO()
    try:
        with redirect_stdout(stdout), redirect_stderr(stderr):
            args = parser.parse_args(argv)
    except SystemExit as exc:
        output = stdout.getvalue() or stderr.getvalue()
        code = exc.code if isinstance(exc.code, int) else 1
        return ToolTextResult(output.rstrip(), code != 0)

    result = await run_cli_command(command, args)
    return ToolTextResult(format_cli_result(_command_name(args), result))


def build_command_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="chatq-strategy",
        description="Operate Chat-Quant strategies in the current project.",
    )
    subparsers = parser.add_subparsers(dest="command_group", required=True)

    def group(name: str, **kwargs: object) -> argparse.ArgumentParser:
        return subparsers.add_parser(name, **kwargs)

    strategy = group("strategy", help="Manage strategies.")
    strategy_subparsers = strategy.add_subparsers(dest="command", required=True)
    strategy_subparsers.add_parser("list", help="List strategies in the current project.")

    show = strategy_subparsers.add_parser("show", help="Show one strategy by id.")
    show.add_argument("--strategy-id", required=True)

    versions = strategy_subparsers.add_parser("versions", help="List versions for a strategy.")
    versions.add_argument("--strategy-id", required=True)

    create = strategy_subparsers.add_parser(
        "create",
        help="Create a strategy and its first version.",
    )
    create.add_argument("--name", required=True)
    create.add_argument("--description")
    add_source_args(create)
    add_mode_arg(create)
    add_risk_note_arg(create)

    modify = strategy_subparsers.add_parser(
        "modify",
        help="Update strategy metadata and/or create a new source-code version.",
    )
    modify.add_argument("--strategy-id", required=True)
    modify.add_argument("--name")
    modify.add_argument("--description")
    modify.add_argument("--tag", action="append", dest="tags", default=None)
    modify.add_argument("--status", choices=["active", "archived"])
    modify.add_argument("--source-file")
    add_mode_arg(modify, default=None)
    add_risk_note_arg(modify)

    switch_version = strategy_subparsers.add_parser("switch-version", help="Switch current version.")
    switch_version.add_argument("--strategy-id", required=True)
    switch_version.add_argument("--strategy-version-id", required=True)

    archive = strategy_subparsers.add_parser("archive", help="Archive a strategy.")
    archive.add_argument("--strategy-id", required=True)

    delete = strategy_subparsers.add_parser("delete", help="Soft-delete a strategy.")
    delete.add_argument("--strategy-id", required=True)

    protocol = group("protocol", help="Show protocols.")
    protocol_subparsers = protocol.add_subparsers(dest="command", required=True)
    protocol_subparsers.add_parser("strategy", help="Show the strategy backtest source protocol.")

    backtest = group("backtest", help="Run and inspect backtests.")
    backtest_subparsers = backtest.add_subparsers(dest="command", required=True)

    run = backtest_subparsers.add_parser("run", help="Run a strategy backtest.")
    run.add_argument("--strategy-id", required=True)
    run.add_argument("--strategy-version-id")
    add_backtest_args(run)

    list_backtests = backtest_subparsers.add_parser("list", help="List backtest records.")
    list_backtests.add_argument("--strategy-version-id")
    list_backtests.add_argument("--limit", type=int, default=20)

    show_backtest = backtest_subparsers.add_parser("show", help="Show one backtest result.")
    show_backtest.add_argument("--backtest-id", required=True)

    return parser


def add_source_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--source-file",
        required=True,
        help="Path to strategy Python source, relative to the current project directory.",
    )


def add_mode_arg(
    parser: argparse.ArgumentParser,
    *,
    default: str | None = "single_symbol",
) -> None:
    parser.add_argument(
        "--mode",
        choices=["single_symbol", "multi_symbol", "portfolio", "universe_selection"],
        default=default,
        help="Strategy mode. Defaults to single_symbol when creating a strategy.",
    )


def add_risk_note_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--risk-note", action="append", dest="risk_notes", default=[])


def add_backtest_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--asset-class", choices=["stock", "etf", "index", "crypto", "futures"])
    parser.add_argument("--market", choices=["CN", "US", "HK"])
    parser.add_argument("--symbol", action="append", dest="symbols")
    parser.add_argument("--symbol-source", choices=["manual", "strategy_fixed", "universe"])
    parser.add_argument("--universe")
    parser.add_argument("--benchmark-symbol")
    parser.add_argument("--start", dest="start_date")
    parser.add_argument("--end", dest="end_date")
    parser.add_argument("--timeframe", choices=["1d"])
    parser.add_argument("--cash", dest="initial_cash")
    parser.add_argument("--commission")
    parser.add_argument("--slippage")
    parser.add_argument("--data-adjust")
    parser.add_argument("--currency", choices=["CNY", "USD", "HKD"])
    parser.add_argument(
        "--rebalance-frequency",
        choices=["none", "daily", "weekly", "monthly", "quarterly"],
    )
    parser.add_argument(
        "--position-sizing",
        choices=["fixed_percent", "equal_weight", "target_weight", "cash_per_order"],
    )
    parser.add_argument("--max-position-count", type=int)
    parser.add_argument("--allow-short", action="store_true")
    parser.add_argument("--risk-control-enabled", action="store_true")
    parser.add_argument("--stop-loss-pct", type=float)
    parser.add_argument("--take-profit-pct", type=float)
    parser.add_argument("--max-drawdown-stop-pct", type=float)
    parser.add_argument("--note", action="append", dest="notes")
    parser.add_argument(
        "--param",
        action="append",
        dest="params",
        default=[],
        help="Runtime override in key=value form. Only valid for backtesting.",
    )


async def run_cli_command(
    command: AgentExecutionCommand,
    args: argparse.Namespace,
) -> dict[str, Any]:
    command_name = _command_name(args)
    if command_name == "strategy list":
        return await execute_chatq_strategy(command, "list_strategies", {})
    if command_name == "strategy show":
        return await execute_chatq_strategy(
            command,
            "get_strategy",
            {"strategy_id": args.strategy_id},
        )
    if command_name == "strategy versions":
        return await execute_chatq_strategy(
            command,
            "list_versions",
            {"strategy_id": args.strategy_id},
        )
    if command_name == "protocol strategy":
        return await execute_chatq_strategy(command, "get_backtest_protocol", {})
    if command_name == "strategy create":
        return await execute_chatq_strategy(
            command,
            "create_strategy",
            compact(
                {
                    "name": args.name,
                    "description": args.description,
                    "source_code": read_source_file(args.source_file, command.project_dir),
                    "strategy_mode": args.mode,
                    "risk_notes": args.risk_notes,
                }
            ),
        )
    if command_name == "strategy modify":
        payload = compact(
            {
                "strategy_id": args.strategy_id,
                "name": args.name,
                "description": args.description,
                "tags": args.tags,
                "status": args.status,
                "strategy_mode": args.mode,
                "risk_notes": args.risk_notes,
            }
        )
        if args.source_file is not None:
            payload["source_code"] = read_source_file(args.source_file, command.project_dir)
        return await execute_chatq_strategy(command, "update_strategy", payload)
    if command_name == "strategy switch-version":
        return await execute_chatq_strategy(
            command,
            "switch_version",
            {
                "strategy_id": args.strategy_id,
                "strategy_version_id": args.strategy_version_id,
            },
        )
    if command_name == "strategy archive":
        return await execute_chatq_strategy(
            command,
            "archive_strategy",
            {"strategy_id": args.strategy_id},
        )
    if command_name == "strategy delete":
        return await execute_chatq_strategy(
            command,
            "delete_strategy",
            {"strategy_id": args.strategy_id},
        )
    if command_name == "backtest run":
        return await execute_chatq_strategy(
            command,
            "run_backtest",
            compact(
                {
                    "strategy_id": args.strategy_id,
                    "strategy_version_id": args.strategy_version_id,
                    "config": build_backtest_config(args),
                }
            ),
        )
    if command_name == "backtest list":
        return await execute_chatq_strategy(
            command,
            "list_backtests",
            compact(
                {
                    "strategy_version_id": args.strategy_version_id,
                    "limit": args.limit,
                }
            ),
        )
    if command_name == "backtest show":
        return await execute_chatq_strategy(
            command,
            "get_backtest",
            {"backtest_id": args.backtest_id},
        )
    raise ToolExecutionError("CHATQ_COMMAND_UNSUPPORTED", f"Unsupported command: {command_name}")


def _command_name(args: argparse.Namespace) -> str:
    return f"{args.command_group} {args.command}"


def read_source_file(source_file: str, project_dir: str) -> str:
    path = Path(source_file).expanduser()
    if not path.is_absolute():
        path = Path(project_dir) / path
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ToolExecutionError(
            "CHATQ_SOURCE_FILE_READ_FAILED",
            f"Failed to read --source-file {source_file}: {exc}",
        ) from exc


def build_backtest_config(args: argparse.Namespace) -> dict[str, object]:
    raw_config = {
        "asset_class": args.asset_class,
        "market": args.market,
        "symbols": args.symbols,
        "symbol_source": args.symbol_source,
        "universe": args.universe,
        "benchmark_symbol": args.benchmark_symbol,
        "start_date": args.start_date,
        "end_date": args.end_date,
        "timeframe": args.timeframe,
        "initial_cash": args.initial_cash,
        "commission": args.commission,
        "slippage": args.slippage,
        "data_adjust": args.data_adjust,
        "currency": args.currency,
        "rebalance_frequency": args.rebalance_frequency,
        "position_sizing": args.position_sizing,
        "max_position_count": args.max_position_count,
        "stop_loss_pct": args.stop_loss_pct,
        "take_profit_pct": args.take_profit_pct,
        "max_drawdown_stop_pct": args.max_drawdown_stop_pct,
        "notes": args.notes,
        "params": parse_params(args.params),
    }
    config = compact(raw_config)
    if args.allow_short:
        config["allow_short"] = True
    if args.risk_control_enabled:
        config["risk_control_enabled"] = True
    return config


def parse_params(values: list[str]) -> dict[str, object]:
    params: dict[str, object] = {}
    for value in values:
        if "=" not in value:
            raise ToolExecutionError(
                "CHATQ_PARAM_INVALID",
                f"--param must use key=value form: {value}",
            )
        key, raw_value = value.split("=", 1)
        key = key.strip()
        if not key:
            raise ToolExecutionError(
                "CHATQ_PARAM_INVALID",
                f"--param key cannot be empty: {value}",
            )
        params[key] = parse_param_value(raw_value)
    return params


def parse_param_value(value: str) -> object:
    stripped = value.strip()
    lowered = stripped.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered == "null":
        return None
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        return stripped


def compact(payload: dict[str, object]) -> dict[str, object]:
    return {key: value for key, value in payload.items() if value is not None}


def format_cli_result(command_name: str, payload: dict[str, Any]) -> str:
    if not payload.get("ok"):
        return _format_cli_error(
            str(payload.get("message") or "chatq_strategy command failed"),
            payload,
        )
    data = payload.get("data")
    summary = payload.get("summary")
    if command_name == "strategy list" and isinstance(data, list):
        return _format_strategy_list(data)
    if command_name == "strategy versions" and isinstance(data, list):
        return _format_version_list(data)
    if command_name == "backtest list" and isinstance(data, list):
        return _format_backtest_list(data)
    if command_name in {
        "strategy create",
        "strategy modify",
        "strategy switch-version",
        "strategy archive",
        "strategy delete",
    }:
        return _format_mutation_result(summary, data)
    if command_name in {"backtest run", "backtest show"} and isinstance(data, dict):
        return _format_backtest_detail(summary, data)
    return _format_data(data)


def _format_strategy_list(records: list[object]) -> str:
    if not records:
        return "No strategies."
    lines = ["Strategies:"]
    for record in records:
        if not isinstance(record, dict):
            continue
        lines.append(
            "  {strategy_id}  v{version}  {strategy_mode}  {status}  {name}".format(
                strategy_id=record.get("strategy_id", "-"),
                version=record.get("version", "-"),
                strategy_mode=record.get("strategy_mode", "-"),
                status=record.get("status", "-"),
                name=record.get("name", "-"),
            )
        )
    return "\n".join(lines)


def _format_version_list(records: list[object]) -> str:
    if not records:
        return "No strategy versions."
    lines = ["Strategy versions:"]
    for record in records:
        if not isinstance(record, dict):
            continue
        lines.append(
            "  {id}  v{version}  {strategy_mode}  created_at={created_at}".format(
                id=record.get("id", "-"),
                version=record.get("version", "-"),
                strategy_mode=record.get("strategy_mode", "-"),
                created_at=record.get("created_at", "-"),
            )
        )
    return "\n".join(lines)


def _format_backtest_list(records: list[object]) -> str:
    if not records:
        return "No backtests."
    lines = ["Backtests:"]
    for record in records:
        if not isinstance(record, dict):
            continue
        lines.append(
            "  {id}  {status}  strategy={strategy_id} version={strategy_version_id} "
            "created_at={created_at}".format(
                id=record.get("id", "-"),
                status=record.get("status", "-"),
                strategy_id=record.get("strategy_id", "-"),
                strategy_version_id=record.get("strategy_version_id", "-"),
                created_at=record.get("created_at", "-"),
            )
        )
    return "\n".join(lines)


def _format_mutation_result(summary: object, data: object) -> str:
    lines = [str(summary or "Done.")]
    if isinstance(data, dict):
        for key in (
            "strategy_id",
            "strategy_version_id",
            "backtest_id",
            "actions",
        ):
            if key in data:
                lines.append(f"{key}: {data[key]}")
        version = data.get("version")
        if isinstance(version, dict):
            lines.append(f"strategy_version_id: {version.get('id')}")
        metadata = data.get("metadata")
        if isinstance(metadata, dict):
            lines.append(f"strategy_id: {metadata.get('id')}")
    return "\n".join(lines)


def _format_backtest_detail(summary: object, data: dict[str, Any]) -> str:
    lines = [str(summary or "Backtest detail:")]
    backtest = data.get("backtest")
    result = data.get("result")
    if isinstance(backtest, dict):
        lines.append(f"backtest_id: {backtest.get('id')}")
        lines.append(f"status: {backtest.get('status')}")
        lines.append(f"strategy_id: {backtest.get('strategy_id')}")
        lines.append(f"strategy_version_id: {backtest.get('strategy_version_id')}")
        if backtest.get("failure_code"):
            lines.append(f"failure_code: {backtest.get('failure_code')}")
        if backtest.get("failure_message"):
            lines.append(f"failure_message: {backtest.get('failure_message')}")
    if isinstance(result, dict):
        metrics = result.get("metrics")
        if isinstance(metrics, dict):
            lines.append("metrics:")
            for key in (
                "initial_value",
                "final_value",
                "total_return_pct",
                "annual_return_pct",
                "max_drawdown_pct",
                "sharpe_ratio",
                "win_rate_pct",
                "total_trades",
            ):
                if key in metrics:
                    lines.append(f"  {key}: {metrics[key]}")
        warnings = result.get("warnings")
        if warnings:
            lines.append(f"warnings: {warnings}")
    return "\n".join(lines)


def _format_data(data: object) -> str:
    if isinstance(data, str):
        return data
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True)


def _format_cli_error(message: str, detail: object | None = None) -> str:
    lines = [f"Error: {message}"]
    if detail:
        lines.append(_format_data(detail))
    return "\n".join(lines)


async def execute_chatq_strategy(
    command: AgentExecutionCommand,
    operator: Operator,
    params: dict[str, Any],
) -> dict[str, Any]:
    async with get_session_factory()() as db:
        await project_service.require_project(db, command.project_id)

        if operator == "list_strategies":
            EmptyParams.model_validate(params)
            records = await strategy_service.list_strategies(db, project_id=command.project_id)
            return _success(operator, [record.model_dump(mode="json") for record in records])

        if operator == "get_strategy":
            parsed = StrategyIdParams.model_validate(params)
            detail = await strategy_service.get_strategy(db, parsed.strategy_id)
            _ensure_strategy_project(detail.strategy.project_id, command.project_id)
            return _success(operator, detail.model_dump(mode="json"))

        if operator == "list_versions":
            parsed = ListVersionsParams.model_validate(params)
            await _require_strategy_in_project(db, parsed.strategy_id, command.project_id)
            versions = await strategy_service.list_versions(db, parsed.strategy_id)
            data = [
                version.model_dump(
                    mode="json",
                    exclude={"source_code"} if not parsed.include_source_code else None,
                )
                for version in versions
            ]
            return _success(operator, data)

        if operator == "get_version":
            parsed = VersionIdParams.model_validate(params)
            version = await strategy_service.get_version(db, parsed.version_id)
            await _require_strategy_in_project(db, version.strategy_id, command.project_id)
            return _success(operator, version.model_dump(mode="json"))

        if operator == "get_backtest_protocol":
            EmptyParams.model_validate(params)
            return _success(operator, StrategyBacktestProtocol().model_dump(mode="json"))

        if operator == "create_strategy":
            parsed = CreateStrategyParams.model_validate(params)
            created = await strategy_service.create_strategy(
                db,
                project_id=command.project_id,
                strategy_input=StrategyCreate.model_validate(parsed.model_dump()),
            )
            return _success(
                operator,
                created.model_dump(mode="json"),
                summary=f"策略已创建：{parsed.name}",
                artifacts=[
                    {
                        "asset_type": "strategy",
                        "asset_id": created.strategy_id,
                        "title": parsed.name,
                    }
                ],
            )

        if operator == "update_strategy":
            parsed = UpdateStrategyParams.model_validate(params)
            strategy = await _require_strategy_in_project(
                db,
                parsed.strategy_id,
                command.project_id,
            )
            if not _has_strategy_update(parsed):
                raise ToolExecutionError(
                    "CHATQ_STRATEGY_UPDATE_EMPTY",
                    "update_strategy requires metadata fields and/or source_code",
                )

            actions: list[str] = []
            data: dict[str, Any] = {
                "strategy_id": parsed.strategy_id,
                "actions": actions,
            }

            if _has_metadata_update(parsed):
                record = await strategy_service.update_strategy_metadata(
                    db,
                    parsed.strategy_id,
                    name=parsed.name,
                    description=parsed.description,
                    tags=parsed.tags,
                    status=parsed.status,
                )
                actions.append("metadata_updated")
                data["metadata"] = record.model_dump(mode="json")
                strategy = record

            if parsed.source_code is not None:
                strategy_mode = parsed.strategy_mode or await _current_strategy_mode(
                    db,
                    strategy.id,
                )
                version = await strategy_service.create_strategy_version(
                    db,
                    strategy_id=parsed.strategy_id,
                    version_input=StrategyVersionCreate(
                        source_code=parsed.source_code,
                        strategy_mode=strategy_mode,
                        risk_notes=parsed.risk_notes,
                    ),
                )
                actions.append("version_created")
                data["version"] = version.model_dump(mode="json")

            artifacts = [
                {
                    "asset_type": "strategy",
                    "asset_id": parsed.strategy_id,
                    "title": strategy.name,
                }
            ]
            if "version" in data:
                version_data = data["version"]
                if isinstance(version_data, dict):
                    artifacts.append(
                        {
                            "asset_type": "strategy_version",
                            "asset_id": str(version_data["id"]),
                            "title": f"{strategy.name} v{version_data['version']}",
                        }
                    )

            return _success(
                operator,
                data,
                summary="策略已更新",
                artifacts=artifacts,
            )

        if operator == "create_version":
            parsed = CreateVersionParams.model_validate(params)
            strategy = await _require_strategy_in_project(
                db,
                parsed.strategy_id,
                command.project_id,
            )
            strategy_mode = parsed.strategy_mode or await _current_strategy_mode(db, strategy.id)
            version = await strategy_service.create_strategy_version(
                db,
                strategy_id=parsed.strategy_id,
                version_input=StrategyVersionCreate(
                    source_code=parsed.source_code,
                    strategy_mode=strategy_mode,
                    risk_notes=parsed.risk_notes,
                ),
            )
            return _success(
                operator,
                version.model_dump(mode="json"),
                summary=f"策略版本已创建：v{version.version}",
                artifacts=[
                    {
                        "asset_type": "strategy_version",
                        "asset_id": version.id,
                        "title": f"{strategy.name} v{version.version}",
                    }
                ],
            )

        if operator == "switch_version":
            parsed = SwitchVersionParams.model_validate(params)
            await _require_strategy_in_project(db, parsed.strategy_id, command.project_id)
            summary = await strategy_service.switch_current_version(
                db,
                parsed.strategy_id,
                version_id=parsed.strategy_version_id,
            )
            return _success(operator, summary.model_dump(mode="json"), summary="当前策略版本已切换")

        if operator == "archive_strategy":
            parsed = StrategyIdParams.model_validate(params)
            await _require_strategy_in_project(db, parsed.strategy_id, command.project_id)
            record = await strategy_service.update_strategy_metadata(
                db,
                parsed.strategy_id,
                status=StrategyStatus.ARCHIVED,
            )
            return _success(operator, record.model_dump(mode="json"), summary="策略已归档")

        if operator == "delete_strategy":
            parsed = StrategyIdParams.model_validate(params)
            await _require_strategy_in_project(db, parsed.strategy_id, command.project_id)
            record = await strategy_service.update_strategy_metadata(
                db,
                parsed.strategy_id,
                status=StrategyStatus.DELETED,
            )
            return _success(operator, record.model_dump(mode="json"), summary="策略已删除")

        if operator == "run_backtest":
            parsed = RunBacktestParams.model_validate(params)
            strategy = await _require_strategy_in_project(
                db,
                parsed.strategy_id,
                command.project_id,
            )
            config = await _build_backtest_config(
                db,
                strategy_id=strategy.id,
                strategy_version_id=parsed.strategy_version_id,
                raw_config=parsed.config,
            )
            detail = await backtest_service.backtest_strategy(
                db,
                strategy_id=parsed.strategy_id,
                project_id=command.project_id,
                config=config,
                strategy_version_id=parsed.strategy_version_id,
            )
            return _success(
                operator,
                _backtest_detail_for_tool(detail),
                summary="回测已完成",
                artifacts=[
                    {
                        "asset_type": "backtest",
                        "asset_id": detail.backtest.id,
                        "title": f"{strategy.name} 回测",
                    }
                ],
            )

        if operator == "list_backtests":
            parsed = ListBacktestsParams.model_validate(params)
            if parsed.strategy_version_id is not None:
                version = await strategy_service.get_version(db, parsed.strategy_version_id)
                await _require_strategy_in_project(db, version.strategy_id, command.project_id)
            records = await backtest_service.list_records(
                db,
                strategy_version_id=parsed.strategy_version_id,
                project_id=command.project_id,
                limit=parsed.limit,
            )
            return _success(operator, [record.model_dump(mode="json") for record in records])

        if operator == "get_backtest":
            parsed = BacktestIdParams.model_validate(params)
            detail = await backtest_service.get_detail(db, parsed.backtest_id)
            _ensure_strategy_project(detail.backtest.project_id, command.project_id)
            return _success(operator, _backtest_detail_for_tool(detail))

    raise ToolExecutionError("CHATQ_OPERATOR_UNSUPPORTED", f"Unsupported operator: {operator}")


async def _require_strategy_in_project(db: Any, strategy_id: str, project_id: str) -> Any:
    detail = await strategy_service.get_strategy(db, strategy_id)
    _ensure_strategy_project(detail.strategy.project_id, project_id)
    return detail.strategy


async def _current_strategy_mode(db: Any, strategy_id: str) -> StrategyMode:
    detail = await strategy_service.get_strategy(db, strategy_id)
    current_version_id = detail.strategy.current_version_id
    if not current_version_id:
        raise ToolExecutionError("STRATEGY_VERSION_NOT_FOUND", "Strategy has no current version")
    version = await strategy_service.get_version(db, current_version_id)
    return version.strategy_mode


async def _build_backtest_config(
    db: Any,
    *,
    strategy_id: str,
    strategy_version_id: str | None,
    raw_config: dict[str, Any],
) -> StrategyBacktestConfig:
    config_data = dict(raw_config)
    if "strategy_mode" not in config_data:
        version_id = strategy_version_id
        if version_id is None:
            detail = await strategy_service.get_strategy(db, strategy_id)
            version_id = detail.strategy.current_version_id
        if not version_id:
            raise ToolExecutionError(
                "STRATEGY_VERSION_NOT_FOUND",
                "Strategy has no current version",
            )
        version = await strategy_service.get_version(db, version_id)
        config_data["strategy_mode"] = version.strategy_mode
    return StrategyBacktestConfig.model_validate(config_data)


def _backtest_detail_for_tool(detail: Any) -> dict[str, Any]:
    data = detail.model_dump(mode="json")
    result = data.get("result")
    if isinstance(result, dict) and "market_data" in result:
        result.pop("market_data", None)
        result["market_data_omitted"] = True
    return data


def _ensure_strategy_project(actual_project_id: str, expected_project_id: str) -> None:
    if actual_project_id != expected_project_id:
        raise ToolExecutionError(
            "CHATQ_ASSET_OUT_OF_SCOPE",
            "Requested asset does not belong to the current project",
        )


def _has_metadata_update(params: UpdateStrategyParams) -> bool:
    return any(
        value is not None
        for value in (params.name, params.description, params.tags, params.status)
    )


def _has_strategy_update(params: UpdateStrategyParams) -> bool:
    return _has_metadata_update(params) or params.source_code is not None


def _success(
    operator: str,
    data: Any,
    *,
    summary: str | None = None,
    artifacts: list[dict[str, str]] | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "ok": True,
        "operator": operator,
        "data": data,
    }
    if summary:
        payload["summary"] = summary
    if artifacts:
        payload["artifacts"] = artifacts
    return payload


def _error_payload(
    error_code: str,
    message: str,
    detail: dict[str, Any] | None = None,
    *,
    operator: object = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "ok": False,
        "operator": operator if isinstance(operator, str) else None,
        "error_code": error_code,
        "message": message,
    }
    if detail:
        payload.update(detail)
    return payload


def _jsonable(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, tuple | list):
        return [_jsonable(item) for item in value]
    if value is None or isinstance(value, str | int | float | bool):
        return value
    return str(value)
