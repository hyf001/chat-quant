import asyncio
import json
from pathlib import Path

from app.agent_runtime.custom_tools.chatq_visualization import (
    handle_chatq_visualization_tool,
    visualization_asset_url,
)
from app.schema.agent_runtime import AgentExecutionCommand


def test_visualization_renders_candlestick_chart(tmp_path: Path) -> None:
    asyncio.run(_run_candlestick_render_assertions(tmp_path))


def test_visualization_renders_cards(tmp_path: Path) -> None:
    asyncio.run(_run_card_render_assertions(tmp_path))


def test_visualization_reports_validation_details(tmp_path: Path) -> None:
    asyncio.run(_run_validation_error_assertions(tmp_path))


def test_visualization_rejects_invalid_render_without_output(tmp_path: Path) -> None:
    asyncio.run(_run_invalid_render_assertions(tmp_path))


def test_visualization_renders_enhanced_report_ui(tmp_path: Path) -> None:
    asyncio.run(_run_enhanced_report_ui_assertions(tmp_path))


def test_visualization_rejects_invalid_metadata_types(tmp_path: Path) -> None:
    asyncio.run(_run_invalid_metadata_type_assertions(tmp_path))


async def _run_candlestick_render_assertions(project_dir: Path) -> None:
    spec_file = project_dir / "kline.json"
    output_file = project_dir / "dashboard" / "kline.html"
    spec_file.write_text(
        json.dumps(
            {
                "kind": "chart",
                "title": "股票K线",
                "type": "candlestick",
                "data": {
                    "columns": ["date", "open", "close", "low", "high"],
                    "rows": [
                        ["2026-08-21", 101.2, 103.5, 100.8, 104.1],
                        ["2026-08-24", 103.7, 102.9, 101.6, 104.4],
                    ],
                },
                "x": {"field": "date"},
                "series": [
                    {
                        "name": "价格",
                        "fields": {
                            "open": "open",
                            "close": "close",
                            "low": "low",
                            "high": "high",
                        },
                    }
                ],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    result = await handle_chatq_visualization_tool(
        _command(project_dir),
        {"command": "chart render --file kline.json --output-file dashboard/kline.html --json"},
    )

    assert result.is_error is False
    payload = json.loads(result.text)
    assert payload["ok"] is True
    assert payload["data"]["output_file"] == "dashboard/kline.html"
    assert (
        payload["data"]["iframe_url"]
        == "/api/projects/project_test/visualization-html/dashboard/kline.html"
    )
    assert payload["data"]["asset_base_url"] == visualization_asset_url()
    html = output_file.read_text(encoding="utf-8")
    assert '"type": "candlestick"' in html
    assert '"scale": true' in html
    assert f'{visualization_asset_url()}/echarts.5.6.0.min.js' in html


async def _run_card_render_assertions(project_dir: Path) -> None:
    spec_file = project_dir / "cards.json"
    output_file = project_dir / "dashboard" / "cards.html"
    spec_file.write_text(
        json.dumps(
            {
                "kind": "card",
                "title": "核心指标",
                "cards": [
                    {
                        "label": "最新收盘价",
                        "value": 103.5,
                        "unit": "元",
                        "format": "number",
                        "decimals": 2,
                    }
                ],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    result = await handle_chatq_visualization_tool(
        _command(project_dir),
        {"command": "card render --file cards.json --output-file dashboard/cards.html"},
    )

    assert result.is_error is False
    assert "Visualization HTML generated." in result.text
    assert (
        "iframe_url: /api/projects/project_test/visualization-html/dashboard/cards.html"
        in result.text
    )
    html = output_file.read_text(encoding="utf-8")
    assert "最新收盘价" in html
    assert "103.50" in html


async def _run_validation_error_assertions(project_dir: Path) -> None:
    spec_file = project_dir / "bad.json"
    spec_file.write_text(
        json.dumps(
            {
                "kind": "chart",
                "title": "坏数据",
                "type": "line",
                "data": {
                    "columns": ["date", "close"],
                    "rows": [["2026-08-21", "not-a-number"], ["2026-08-24"]],
                },
                "x": {"field": "trade_date"},
                "series": [{"name": "收盘价", "field": "close"}],
                "unexpected": True,
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    result = await handle_chatq_visualization_tool(
        _command(project_dir),
        {"command": "validate --file bad.json --kind chart --json"},
    )

    assert result.is_error is True
    payload = json.loads(result.text)
    errors = payload["detail"]["errors"]
    codes = {error["code"] for error in errors}
    assert {
        "UNKNOWN_FIELD",
        "ROW_LENGTH_MISMATCH",
        "FIELD_NOT_FOUND",
        "NUMBER_INVALID",
    }.issubset(codes)


async def _run_invalid_render_assertions(project_dir: Path) -> None:
    spec_file = project_dir / "bad_kline.json"
    output_file = project_dir / "dashboard" / "bad_kline.html"
    spec_file.write_text(
        json.dumps(
            {
                "kind": "chart",
                "title": "坏K线",
                "type": "candlestick",
                "data": {
                    "columns": ["date", "open", "close", "low", "high"],
                    "rows": [["2026-08-21", 101.2, None, 100.8, 104.1]],
                },
                "x": {"field": "date"},
                "series": [
                    {
                        "name": "价格",
                        "fields": {
                            "open": "open",
                            "close": "close",
                            "low": "low",
                            "high": "high",
                        },
                    }
                ],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    result = await handle_chatq_visualization_tool(
        _command(project_dir),
        {"command": "chart render --file bad_kline.json --output-file dashboard/bad_kline.html"},
    )

    assert result.is_error is True
    assert "NUMBER_INVALID" in result.text
    assert not output_file.exists()


async def _run_enhanced_report_ui_assertions(project_dir: Path) -> None:
    spec_file = project_dir / "report.json"
    output_file = project_dir / "visualization" / "report.html"
    spec_file.write_text(
        json.dumps(
            {
                "kind": "report",
                "title": "增强报表",
                "subtitle": "近10个交易日走势与关键指标",
                "source": "a_stock_daily_price / 前复权",
                "cards": [
                    {
                        "label": "收益率",
                        "value": 0.126,
                        "format": "percent",
                        "icon": "trending-up",
                    }
                ],
                "charts": [
                    {
                        "title": "行业占比",
                        "subtitle": "行业权重分布",
                        "source": "derived_sector_weight",
                        "type": "pie",
                        "data": {
                            "columns": ["sector", "weight"],
                            "rows": [["金融", 32.1], ["消费", 18.4]],
                        },
                        "series": [
                            {
                                "name": "权重",
                                "name_field": "sector",
                                "value_field": "weight",
                            }
                        ],
                    }
                ],
                "tables": [
                    {
                        "title": "明细",
                        "subtitle": "行情逐日明细",
                        "source": "a_stock_daily_price",
                        "data": {
                            "columns": ["date", "close"],
                            "rows": [["2026-08-21", 103.5], ["2026-08-24", 102.9]],
                        },
                    }
                ],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    result = await handle_chatq_visualization_tool(
        _command(project_dir),
        {"command": "report render --file report.json --output-file visualization/report.html"},
    )

    assert result.is_error is False
    html = output_file.read_text(encoding="utf-8")
    assert "近10个交易日走势与关键指标" in html
    assert "数据源：a_stock_daily_price / 前复权" in html
    assert "行业权重分布" in html
    assert "数据源：derived_sector_weight" in html
    assert "行情逐日明细" in html
    assert "title-indicator" in html
    assert "card-icon" in html
    assert 'data-lucide="trending-up"' in html
    assert "data-chart-zoom" in html
    assert 'id="chart-modal"' in html
    assert "ResizeObserver" in html
    assert "sortTable" in html
    assert "sort-arrows" in html
    assert "#316a9e" in html
    assert "lineStyle" in html


async def _run_invalid_metadata_type_assertions(project_dir: Path) -> None:
    spec_file = project_dir / "bad_metadata.json"
    spec_file.write_text(
        json.dumps(
            {
                "kind": "report",
                "title": "元信息错误",
                "subtitle": 123,
                "source": False,
                "cards": [{"label": "最新收盘价", "value": 23.1}],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    result = await handle_chatq_visualization_tool(
        _command(project_dir),
        {"command": "validate --file bad_metadata.json --kind report --json"},
    )

    assert result.is_error is True
    payload = json.loads(result.text)
    errors = payload["detail"]["errors"]
    assert {
        ("root.subtitle", "TYPE_INVALID"),
        ("root.source", "TYPE_INVALID"),
    }.issubset({(error["path"], error["code"]) for error in errors})


def _command(project_dir: Path) -> AgentExecutionCommand:
    return AgentExecutionCommand(
        project_id="project_test",
        chat_session_id="chat_1",
        user_message_id="msg_1",
        project_dir=str(project_dir),
        sdk_session_id=None,
        request_id="req_1",
        user_prompt="生成可视化",
    )
