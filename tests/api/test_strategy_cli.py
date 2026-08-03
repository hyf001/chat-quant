from __future__ import annotations

import json
from argparse import Namespace
from pathlib import Path

import pytest

from cli import chatq_strategy, config


class FakeClient:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str, object | None, dict[str, object] | None]] = []
        self.base_url = "http://test/api"
        self.user_id: str | None = None
        self.project_id: str | None = None

    def request(
        self,
        method: str,
        path: str,
        payload: object | None = None,
        *,
        query: dict[str, object] | None = None,
    ) -> object:
        self.calls.append((method, path, payload, query))
        if method == "GET" and path == "/strategies/str_1":
            return {
                "strategy": {
                    "id": "str_1",
                    "user_id": "user_a",
                    "project_id": "project_a",
                    "current_version_id": "stv_1",
                }
            }
        if method == "GET" and path == "/strategies/str_1/versions":
            return [
                {"id": "stv_1", "strategy_mode": "single_symbol"},
                {"id": "stv_2", "strategy_mode": "multi_symbol"},
            ]
        return {"method": method, "path": path, "payload": payload, "query": query}

    def with_strategy_context(self, strategy_id: str) -> tuple[FakeClient, dict[str, object]]:
        detail = self.request("GET", f"/strategies/{strategy_id}")
        self.user_id = detail["strategy"]["user_id"]
        self.project_id = detail["strategy"]["project_id"]
        return self, detail


def test_create_strategy_uses_source_file_without_request_custom_params(tmp_path: Path) -> None:
    source_file = tmp_path / "strategy.py"
    source_file.write_text("import backtrader as bt\n", encoding="utf-8")
    client = FakeClient()

    result = chatq_strategy.create_strategy(
        client,
        Namespace(
            name="均线策略",
            description="测试策略",
            source_file=str(source_file),
            mode="single_symbol",
            risk_notes=["历史回测不代表未来收益"],
        ),
    )

    assert result["path"] == "/strategies"
    payload = result["payload"]
    assert payload == {
        "name": "均线策略",
        "description": "测试策略",
        "source_code": "import backtrader as bt\n",
        "strategy_mode": "single_symbol",
        "risk_notes": ["历史回测不代表未来收益"],
    }
    assert "custom_params" not in payload


def test_modify_can_update_metadata_and_create_version(tmp_path: Path) -> None:
    source_file = tmp_path / "strategy.py"
    source_file.write_text("class GeneratedStrategy:\n    pass\n", encoding="utf-8")
    client = FakeClient()

    result = chatq_strategy.modify_strategy(
        client,
        Namespace(
            strategy_id="str_1",
            name="新版策略",
            description=None,
            tags=["沪深300", "稳健版"],
            status=None,
            source_file=str(source_file),
            mode="single_symbol",
            risk_notes=[],
        ),
    )

    assert result["actions"] == ["metadata_updated", "version_created"]
    assert client.calls[0] == (
        "GET",
        "/strategies/str_1",
        None,
        None,
    )
    assert client.calls[1] == (
        "PATCH",
        "/strategies/str_1",
        {"name": "新版策略", "tags": ["沪深300", "稳健版"]},
        None,
    )
    assert client.calls[2] == (
        "GET",
        "/strategies/str_1/versions",
        None,
        None,
    )
    assert client.calls[3][0:2] == ("POST", "/strategies/str_1/versions")
    assert client.calls[3][2] == {
        "source_code": "class GeneratedStrategy:\n    pass\n",
        "strategy_mode": "single_symbol",
        "risk_notes": [],
    }


def test_backtest_params_are_runtime_config_overrides() -> None:
    args = Namespace(
        asset_class="stock",
        market="CN",
        symbols=["600519.SH"],
        symbol_source=None,
        universe=None,
        benchmark_symbol=None,
        start_date="2024-01-01",
        end_date="2024-04-30",
        timeframe=None,
        initial_cash="100000",
        commission="0.001",
        slippage=None,
        data_adjust=None,
        currency=None,
        rebalance_frequency=None,
        position_sizing=None,
        max_position_count=None,
        allow_short=False,
        risk_control_enabled=False,
        stop_loss_pct=None,
        take_profit_pct=None,
        max_drawdown_stop_pct=None,
        notes=None,
        params=["fast_period=20", "enabled=true", "label=medium"],
    )

    config = chatq_strategy.build_backtest_config(args)

    assert config["params"] == {
        "fast_period": 20,
        "enabled": True,
        "label": "medium",
    }
    assert config["symbols"] == ["600519.SH"]


def test_backtest_omits_strategy_version_id_by_default() -> None:
    client = FakeClient()

    result = chatq_strategy.backtest_strategy(
        client,
        Namespace(
            strategy_id="str_1",
            strategy_version_id=None,
            asset_class="stock",
            market="CN",
            symbols=["600519.SH"],
            symbol_source=None,
            universe=None,
            benchmark_symbol=None,
            start_date="2024-01-01",
            end_date="2024-04-30",
            timeframe=None,
            initial_cash="100000",
            commission="0.001",
            slippage=None,
            data_adjust=None,
            currency=None,
            rebalance_frequency=None,
            position_sizing=None,
            max_position_count=None,
            allow_short=False,
            risk_control_enabled=False,
            stop_loss_pct=None,
            take_profit_pct=None,
            max_drawdown_stop_pct=None,
            notes=None,
            params=[],
        ),
    )

    assert result["path"] == "/strategies/str_1/backtest"
    assert result["payload"]["config"]["strategy_mode"] == "single_symbol"
    assert "strategy_version_id" not in result["payload"]


def test_backtest_can_target_specific_strategy_version() -> None:
    client = FakeClient()

    result = chatq_strategy.backtest_strategy(
        client,
        Namespace(
            strategy_id="str_1",
            strategy_version_id="stv_2",
            asset_class="stock",
            market="CN",
            symbols=["600519.SH"],
            symbol_source=None,
            universe=None,
            benchmark_symbol=None,
            start_date="2024-01-01",
            end_date="2024-04-30",
            timeframe=None,
            initial_cash="100000",
            commission="0.001",
            slippage=None,
            data_adjust=None,
            currency=None,
            rebalance_frequency=None,
            position_sizing=None,
            max_position_count=None,
            allow_short=False,
            risk_control_enabled=False,
            stop_loss_pct=None,
            take_profit_pct=None,
            max_drawdown_stop_pct=None,
            notes=None,
            params=[],
        ),
    )

    assert result["payload"]["strategy_version_id"] == "stv_2"
    assert result["payload"]["config"]["strategy_mode"] == "multi_symbol"


def test_project_scoped_commands_require_context() -> None:
    parser = chatq_strategy.build_parser()
    args = parser.parse_args(["list"])

    with pytest.raises(chatq_strategy.CliError, match="requires --user-id and --project-id"):
        chatq_strategy.require_context(args)


def test_context_flags_are_accepted_after_subcommand() -> None:
    parser = chatq_strategy.build_parser()
    args = parser.parse_args(["list", "--user-id", "user_a", "--project-id", "project_a"])

    assert args.command == "list"
    assert args.user_id == "user_a"
    assert args.project_id == "project_a"


def test_api_base_url_is_loaded_from_config(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CHATQ_API_BASE_URL", "http://example.test/api")

    assert config.get_config().api_base_url == "http://example.test/api"


def test_show_and_backtest_records_do_not_require_context() -> None:
    assert "show" not in chatq_strategy.CONTEXT_COMMANDS
    assert "versions" not in chatq_strategy.CONTEXT_COMMANDS
    assert "modify" not in chatq_strategy.CONTEXT_COMMANDS
    assert "backtest" not in chatq_strategy.CONTEXT_COMMANDS
    assert "backtests" not in chatq_strategy.CONTEXT_COMMANDS
    assert "backtest-show" not in chatq_strategy.CONTEXT_COMMANDS


def test_version_create_command_is_not_exposed() -> None:
    parser = chatq_strategy.build_parser()
    help_text = parser.format_help()

    assert "version-create" not in help_text
    assert "version-create" not in chatq_strategy.CONTEXT_COMMANDS


def test_api_base_url_is_not_exposed_as_cli_argument(
    capsys: pytest.CaptureFixture[str],
) -> None:
    parser = chatq_strategy.build_parser()
    root_help = parser.format_help()

    assert "--api-base-url" not in root_help
    with pytest.raises(SystemExit):
        parser.parse_args(["create", "--help"])
    captured = capsys.readouterr()
    assert "--api-base-url" not in captured.out


def test_cli_error_is_json(capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = chatq_strategy.main(["list"])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert json.loads(captured.err) == {
        "error": "cli_error",
        "message": "list requires --user-id and --project-id",
    }
