from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from cli.config import get_config

CONTEXT_COMMANDS = {
    "list",
    "create",
}


class CliError(Exception):
    pass


class ApiError(CliError):
    def __init__(self, status: int, detail: object) -> None:
        super().__init__(f"API request failed with status {status}")
        self.status = status
        self.detail = detail


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = run(args)
    except CliError as exc:
        print_error(exc)
        return 1
    if result is not None:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="chatq-strategy",
        description="Operate Chat-Quant strategies through business-level API actions.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    def command(name: str, **kwargs: object) -> argparse.ArgumentParser:
        return subparsers.add_parser(name, **kwargs)

    list_command = command("list", help="List strategies in the current local project.")
    add_project_path_arg(list_command)
    show = command("show", help="Show one strategy by id.")
    show.add_argument("strategy_id")

    versions = command("versions", help="List versions for a strategy.")
    versions.add_argument("strategy_id")

    command("protocol", help="Show the strategy backtest source protocol.")

    create = command(
        "create",
        help="Create a strategy and its first version.",
    )
    create.add_argument("--name", required=True)
    create.add_argument("--description")
    add_project_path_arg(create)
    add_source_args(create)
    add_mode_arg(create)
    add_risk_note_arg(create)

    modify = command(
        "modify",
        help="Update strategy metadata and/or create a new source-code version.",
    )
    modify.add_argument("strategy_id")
    modify.add_argument("--name")
    modify.add_argument("--description")
    modify.add_argument("--tag", action="append", dest="tags", default=None)
    modify.add_argument("--status", choices=["active", "archived"])
    modify.add_argument("--source-file")
    add_risk_note_arg(modify)

    switch_version = command("switch-version", help="Switch current version.")
    switch_version.add_argument("strategy_id")
    switch_version.add_argument("strategy_version_id")

    archive = command("archive", help="Archive a strategy.")
    archive.add_argument("strategy_id")

    delete = command("delete", help="Soft-delete a strategy.")
    delete.add_argument("strategy_id")

    backtest = command("backtest", help="Run a strategy backtest.")
    backtest.add_argument("strategy_id")
    backtest.add_argument("--version", dest="strategy_version_id")
    add_backtest_args(backtest)

    backtests = command("backtests", help="List backtest records.")
    backtests.add_argument("--version", dest="strategy_version_id")
    backtests.add_argument("--limit", type=int, default=20)

    backtest_show = command("backtest-show", help="Show one backtest result.")
    backtest_show.add_argument("backtest_id")

    return parser


def add_source_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--source-file",
        required=True,
        help="Path to strategy Python source. The CLI submits file content as source_code.",
    )


def add_project_path_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--project-path",
        help=(
            "Business project directory to resolve as Chat-Quant project. "
            "Defaults to the current working directory."
        ),
    )


def add_mode_arg(parser: argparse.ArgumentParser, *, required: bool = False) -> None:
    parser.add_argument(
        "--mode",
        choices=["single_symbol", "multi_symbol", "portfolio", "universe_selection"],
        default=None if required else "single_symbol",
        required=required,
        help="Strategy mode. Defaults to single_symbol.",
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


def run(args: argparse.Namespace) -> object:
    client = ApiClient(
        base_url=get_config().api_base_url,
    )
    if args.command in CONTEXT_COMMANDS:
        client = client.with_current_project(getattr(args, "project_path", None))

    if args.command == "list":
        return client.request(
            "GET",
            "/strategies",
            query={"project_id": _client_project_id(client)},
        )
    if args.command == "show":
        return client.request("GET", f"/strategies/{quote_path(args.strategy_id)}")
    if args.command == "versions":
        return client.request("GET", f"/strategies/{quote_path(args.strategy_id)}/versions")
    if args.command == "protocol":
        return client.request("GET", "/strategy-backtest/protocol")
    if args.command == "create":
        return create_strategy(client, args)
    if args.command == "modify":
        return modify_strategy(client, args)
    if args.command == "switch-version":
        return switch_version(client, args)
    if args.command == "archive":
        return patch_strategy_status(client, args.strategy_id, "archived")
    if args.command == "delete":
        client, _ = client.with_strategy_context(args.strategy_id)
        return client.request("DELETE", f"/strategies/{quote_path(args.strategy_id)}")
    if args.command == "backtest":
        return backtest_strategy(client, args)
    if args.command == "backtests":
        return list_backtests(client, args)
    if args.command == "backtest-show":
        return client.request("GET", f"/backtests/{quote_path(args.backtest_id)}")
    raise CliError(f"Unsupported command: {args.command}")


def create_strategy(client: ApiClient, args: argparse.Namespace) -> object:
    payload = {
        "project_id": _client_project_id(client),
        "name": args.name,
        "source_code": read_source_file(args.source_file),
        "strategy_mode": args.mode,
        "risk_notes": args.risk_notes,
    }
    if args.description is not None:
        payload["description"] = args.description
    return client.request("POST", "/strategies", payload)


def modify_strategy(client: ApiClient, args: argparse.Namespace) -> object:
    client, detail = client.with_strategy_context(args.strategy_id)
    metadata = compact(
        {
            "name": args.name,
            "description": args.description,
            "tags": args.tags,
            "status": args.status,
        }
    )
    source_file = getattr(args, "source_file", None)
    if not metadata and source_file is None:
        raise CliError("modify requires metadata flags and/or --source-file")

    result: dict[str, object] = {"strategy_id": args.strategy_id, "actions": []}
    if metadata:
        result["metadata"] = client.request(
            "PATCH",
            f"/strategies/{quote_path(args.strategy_id)}",
            metadata,
        )
        result["actions"].append("metadata_updated")
    if source_file is not None:
        result["version"] = client.request(
            "POST",
            f"/strategies/{quote_path(args.strategy_id)}/versions",
            version_payload(args, strategy_mode=current_strategy_mode(client, detail)),
        )
        result["actions"].append("version_created")
    return result


def version_payload(args: argparse.Namespace, *, strategy_mode: str) -> dict[str, object]:
    return {
        "source_code": read_source_file(args.source_file),
        "strategy_mode": strategy_mode,
        "risk_notes": args.risk_notes,
    }


def switch_version(client: ApiClient, args: argparse.Namespace) -> object:
    client, _ = client.with_strategy_context(args.strategy_id)
    return client.request(
        "PATCH",
        f"/strategies/{quote_path(args.strategy_id)}/current-version",
        {"strategy_version_id": args.strategy_version_id},
    )


def patch_strategy_status(client: ApiClient, strategy_id: str, status: str) -> object:
    client, _ = client.with_strategy_context(strategy_id)
    return client.request(
        "PATCH",
        f"/strategies/{quote_path(strategy_id)}",
        {"status": status},
    )


def backtest_strategy(client: ApiClient, args: argparse.Namespace) -> object:
    client, detail = client.with_strategy_context(args.strategy_id)
    config = build_backtest_config(args)
    if args.strategy_version_id is None:
        config["strategy_mode"] = current_strategy_mode(client, detail)
        payload = {"config": config, "project_id": _client_project_id(client)}
    else:
        config["strategy_mode"] = strategy_version_mode(
            client,
            args.strategy_id,
            args.strategy_version_id,
        )
        payload = {"config": config, "project_id": _client_project_id(client)}
        payload["strategy_version_id"] = args.strategy_version_id
    result = client.request("POST", f"/strategies/{quote_path(args.strategy_id)}/backtest", payload)
    return with_display_artifacts(result)


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


def list_backtests(client: ApiClient, args: argparse.Namespace) -> object:
    query: dict[str, object] = {"limit": args.limit}
    if args.strategy_version_id is not None:
        query["strategy_version_id"] = args.strategy_version_id
    return client.request("GET", "/backtests", query=query)


def with_display_artifacts(result: object) -> object:
    if not isinstance(result, dict):
        return result
    backtest = result.get("backtest")
    if not isinstance(backtest, dict):
        return result

    artifacts: list[dict[str, object]] = []
    backtest_id = _string_value(backtest.get("id"))
    strategy_id = _string_value(backtest.get("strategy_id"))
    strategy_version_id = _string_value(backtest.get("strategy_version_id"))
    symbols = backtest_symbols(backtest)

    if backtest_id:
        artifacts.append(
            display_artifact(
                asset_type="backtest_run",
                asset_id=backtest_id,
                title=f"{symbols} 回测结果" if symbols else "回测结果",
                display_token=f"[查看回测结果](chatq://backtest/{backtest_id})",
            )
        )
    if strategy_id:
        artifacts.append(
            display_artifact(
                asset_type="strategy",
                asset_id=strategy_id,
                title="策略",
                display_token=f"[打开策略](chatq://strategy/{strategy_id})",
            )
        )
    if strategy_version_id:
        artifacts.append(
            display_artifact(
                asset_type="strategy_version",
                asset_id=strategy_version_id,
                title="策略版本",
                display_token=f"[查看策略版本](chatq://strategy-version/{strategy_version_id})",
            )
        )

    if not artifacts:
        return result
    existing = result.get("artifacts")
    if isinstance(existing, list):
        result["artifacts"] = [*existing, *artifacts]
    else:
        result["artifacts"] = artifacts
    return result


def display_artifact(
    *,
    asset_type: str,
    asset_id: str,
    title: str,
    display_token: str,
) -> dict[str, object]:
    return {
        "asset_type": asset_type,
        "asset_id": asset_id,
        "title": title,
        "display_token": display_token,
    }


def backtest_symbols(backtest: dict[str, object]) -> str:
    config = backtest.get("config")
    if not isinstance(config, dict):
        return ""
    symbols = config.get("symbols")
    if not isinstance(symbols, list):
        return ""
    return "、".join(str(symbol) for symbol in symbols if symbol)


def _string_value(value: object) -> str | None:
    return value if isinstance(value, str) and value else None


def current_strategy_mode(client: ApiClient, detail: dict[str, object]) -> str:
    strategy = strategy_record(detail)
    current_version_id = strategy.get("current_version_id")
    if not isinstance(current_version_id, str) or not current_version_id:
        raise CliError("Strategy has no current version")
    return strategy_version_mode(client, str(strategy["id"]), current_version_id)


def strategy_version_mode(client: ApiClient, strategy_id: str, version_id: str) -> str:
    versions = client.request("GET", f"/strategies/{quote_path(strategy_id)}/versions")
    if not isinstance(versions, list):
        raise CliError("Failed to resolve strategy versions")
    for version in versions:
        if isinstance(version, dict) and version.get("id") == version_id:
            mode = version.get("strategy_mode")
            if isinstance(mode, str) and mode:
                return mode
            raise CliError(f"Strategy version {version_id} has no strategy_mode")
    raise CliError(f"Strategy version not found: {version_id}")


def strategy_record(detail: dict[str, object]) -> dict[str, object]:
    strategy = detail.get("strategy")
    if not isinstance(strategy, dict):
        raise CliError("Failed to resolve strategy detail")
    return strategy


def read_source_file(source_file: str) -> str:
    path = Path(source_file)
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise CliError(f"Failed to read --source-file {source_file}: {exc}") from exc


def parse_params(values: list[str]) -> dict[str, object]:
    params: dict[str, object] = {}
    for value in values:
        if "=" not in value:
            raise CliError(f"--param must use key=value form: {value}")
        key, raw_value = value.split("=", 1)
        key = key.strip()
        if not key:
            raise CliError(f"--param key cannot be empty: {value}")
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


def quote_path(value: str) -> str:
    return urllib.parse.quote(value, safe="")


def _client_project_id(client: object) -> str:
    require_project_id = getattr(client, "require_project_id", None)
    if callable(require_project_id):
        value = require_project_id()
    else:
        value = getattr(client, "project_id", None)
    if not isinstance(value, str) or not value:
        raise CliError("Current project could not be resolved")
    return value


class ApiClient:
    def __init__(
        self,
        *,
        base_url: str,
        project_id: str | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.project_id = project_id

    def require_project_id(self) -> str:
        if not self.project_id:
            raise CliError("Current project could not be resolved")
        return self.project_id

    def with_current_project(self, project_path: str | None = None) -> ApiClient:
        local_path = (
            Path(project_path).expanduser().resolve()
            if project_path
            else Path.cwd().resolve()
        )
        project = self.request(
            "POST",
            "/projects/resolve",
            {"local_path": str(local_path)},
        )
        if not isinstance(project, dict):
            raise CliError("Failed to resolve current project")
        project_id = project.get("id")
        if not isinstance(project_id, str) or not project_id:
            raise CliError("Resolved project has no id")
        return ApiClient(base_url=self.base_url, project_id=project_id)

    def with_strategy_context(self, strategy_id: str) -> tuple[ApiClient, dict[str, object]]:
        detail = self.request("GET", f"/strategies/{quote_path(strategy_id)}")
        if not isinstance(detail, dict):
            raise CliError("Failed to resolve strategy detail")
        strategy = strategy_record(detail)
        project_id = strategy.get("project_id")
        if not isinstance(project_id, str) or not project_id:
            raise CliError("Strategy detail has no project_id")
        return (
            ApiClient(
                base_url=self.base_url,
                project_id=project_id,
            ),
            detail,
        )

    def request(
        self,
        method: str,
        path: str,
        payload: object | None = None,
        *,
        query: dict[str, object] | None = None,
    ) -> object:
        url = f"{self.base_url}{path}"
        if query:
            url = f"{url}?{urllib.parse.urlencode(query)}"
        body = None
        headers = {"Accept": "application/json"}
        if payload is not None:
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            headers["Content-Type"] = "application/json"
        request = urllib.request.Request(url, data=body, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request) as response:
                return decode_response(response.read())
        except urllib.error.HTTPError as exc:
            raise ApiError(exc.code, decode_response(exc.read())) from exc
        except urllib.error.URLError as exc:
            raise CliError(f"Failed to connect to {url}: {exc.reason}") from exc


def decode_response(body: bytes) -> object:
    if not body:
        return None
    try:
        return json.loads(body.decode("utf-8"))
    except json.JSONDecodeError:
        return body.decode("utf-8", errors="replace")


def print_error(error: CliError) -> None:
    if isinstance(error, ApiError):
        payload = {"error": "api_error", "status": error.status, "detail": error.detail}
    else:
        payload = {"error": "cli_error", "message": str(error)}
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), file=sys.stderr)


if __name__ == "__main__":
    raise SystemExit(main())
