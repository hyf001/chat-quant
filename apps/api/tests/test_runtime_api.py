from __future__ import annotations

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_runtime_execute_collects_json_and_table_artifacts() -> None:
    response = client.post(
        "/api/runtime/execute",
        json={
            "chat_session_id": "conv_test",
            "code_artifact_id": "code_inline",
            "entrypoint": "analysis.py",
            "stdin_json": {"symbols": ["AAA", "BBB"]},
            "expected_outputs": ["result.json", "tables/candidates.csv"],
            "code_files": [
                {
                    "path": "analysis.py",
                    "content": "\n".join(
                        [
                            "import csv",
                            "import json",
                            "import os",
                            "from pathlib import Path",
                            "output_dir = Path(os.environ['CHATQ_OUTPUT_DIR'])",
                            "tables_dir = output_dir / 'tables'",
                            "tables_dir.mkdir(parents=True, exist_ok=True)",
                            "with (tables_dir / 'candidates.csv').open('w', newline='') as f:",
                            "    writer = csv.writer(f)",
                            "    writer.writerow(['symbol', 'score'])",
                            "    writer.writerow(['AAA', 90])",
                            "payload = {'status': 'succeeded', 'rows': 1}",
                            "target = output_dir / 'result.json'",
                            "target.write_text(json.dumps(payload), encoding='utf-8')",
                            "print('ok')",
                        ]
                    ),
                }
            ],
        },
    )

    assert response.status_code == 200
    result = response.json()["execution_result"]
    assert result["status"] == "succeeded"
    assert result["stdout"].strip() == "ok"
    assert {artifact["path"] for artifact in result["artifacts"]} == {
        "result.json",
        "tables/candidates.csv",
    }


def test_runtime_execute_rejects_out_of_bounds_entrypoint() -> None:
    response = client.post(
        "/api/runtime/execute",
        json={
            "chat_session_id": "conv_test",
            "code_artifact_id": "code_inline",
            "entrypoint": "../analysis.py",
            "code_files": [{"path": "analysis.py", "content": "print('nope')"}],
        },
    )

    assert response.status_code == 200
    result = response.json()["execution_result"]
    assert result["status"] == "failed"
    assert result["error"]["code"] == "PATH_OUT_OF_BOUNDS"


def test_runtime_execute_timeout_returns_stable_error() -> None:
    response = client.post(
        "/api/runtime/execute",
        json={
            "chat_session_id": "conv_test",
            "code_artifact_id": "code_inline",
            "entrypoint": "slow.py",
            "timeout_seconds": 1,
            "code_files": [
                {
                    "path": "slow.py",
                    "content": "import time\ntime.sleep(10)\n",
                }
            ],
        },
    )

    assert response.status_code == 200
    result = response.json()["execution_result"]
    assert result["status"] == "timeout"
    assert result["error"]["code"] == "PROCESS_TIMEOUT"


def test_runtime_backtest_execute_returns_standard_payload_artifacts() -> None:
    response = client.post(
        "/api/runtime/backtests/execute",
        json={
            "backtest_run_id": "bt_test",
            "strategy_version_id": "sv_test",
            "code_artifact_id": "code_strategy",
            "entrypoint": "strategy.py:GeneratedStrategy",
            "symbols": ["000300.SH"],
            "market": "CN",
            "start_date": "2026-01-01",
            "end_date": "2026-02-01",
            "initial_cash": 100000,
            "commission": 0.0003,
            "params": {"short_window": 20, "long_window": 60},
            "code_files": [
                {
                    "path": "strategy.py",
                    "content": "class GeneratedStrategy:\n    pass\n",
                }
            ],
        },
    )

    assert response.status_code == 200
    result = response.json()
    assert result["status"] == "succeeded"
    assert result["schema_validation"]["schema"] == "BacktestResultPayload"
    assert result["schema_validation"]["passed"] is True
    assert {artifact["path"] for artifact in result["artifacts"]} >= {
        "result.json",
        "equity_curve.json",
        "drawdown_curve.json",
    }
