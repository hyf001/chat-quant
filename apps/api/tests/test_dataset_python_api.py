import asyncio
import shlex
from pathlib import Path

import pytest
from app.agent_runtime.custom_tools.chatq_python import handle_chatq_python_tool
from app.schema.agent_runtime import AgentExecutionCommand
from app.service.dataset.python_api import (
    DatasetPythonApiError,
    describe_dataset,
    list_datasets,
    preview_dataset,
    query_dataset,
)
from fastapi.testclient import TestClient


def test_dataset_python_api_lists_describes_and_queries_exposed_dataset(
    client: TestClient,
) -> None:
    _create_dataset(
        client,
        name="stock_a_daily_price",
        exposed_to_agent=True,
        create_sql=(
            "CREATE VIEW stock_a_daily_price AS "
            "SELECT '600519.SH' AS symbol, DATE '2024-01-02' AS trade_date, 1688.5 AS close "
            "UNION ALL SELECT '000001.SZ' AS symbol, DATE '2024-01-02' AS trade_date, 10.2 AS close"
        ),
    )

    datasets = list_datasets()
    assert datasets["id"].tolist() == ["stock_a_daily_price"]

    detail = describe_dataset("stock_a_daily_price")
    assert detail["id"] == "stock_a_daily_price"
    assert [column["name"] for column in detail["columns"]] == [
        "symbol",
        "trade_date",
        "close",
    ]

    preview = preview_dataset("stock_a_daily_price", limit=1)
    assert preview.shape == (1, 3)

    queried = query_dataset(
        """
        SELECT symbol, close
        FROM stock_a_daily_price
        WHERE symbol = '600519.SH'
        """
    )
    assert queried.to_dict(orient="records") == [
        {"symbol": "600519.SH", "close": 1688.5}
    ]


def test_dataset_python_api_hides_non_exposed_dataset(client: TestClient) -> None:
    _create_dataset(
        client,
        name="private_factor_dataset",
        exposed_to_agent=False,
        create_sql="CREATE VIEW private_factor_dataset AS SELECT '600519.SH' AS symbol",
    )

    assert list_datasets().empty
    with pytest.raises(DatasetPythonApiError, match="DATASET_NOT_EXPOSED"):
        describe_dataset("private_factor_dataset")
    with pytest.raises(DatasetPythonApiError, match="DATASET_NOT_EXPOSED"):
        query_dataset("SELECT * FROM private_factor_dataset")
    with pytest.raises(DatasetPythonApiError, match="DATASET_NOT_EXPOSED"):
        query_dataset('SELECT * FROM "private_factor_dataset"')


def test_dataset_python_api_query_dataset_does_not_auto_limit(client: TestClient) -> None:
    _create_dataset(
        client,
        name="large_dataset",
        exposed_to_agent=True,
        create_sql="CREATE VIEW large_dataset AS SELECT i AS value FROM range(6001) AS rows(i)",
    )

    queried = query_dataset("SELECT value FROM large_dataset ORDER BY value")

    assert queried.shape == (6001, 1)
    assert queried["value"].iloc[-1] == 6000


def test_chatq_python_can_import_dataset_python_api(
    client: TestClient,
    tmp_path: Path,
) -> None:
    _create_dataset(
        client,
        name="stock_a_daily_price",
        exposed_to_agent=True,
        create_sql=(
            "CREATE VIEW stock_a_daily_price AS "
            "SELECT '600519.SH' AS symbol, 1688.5 AS close"
        ),
    )
    code = """
from app.service.dataset.python_api import query_dataset

df = query_dataset("SELECT symbol, close FROM stock_a_daily_price")
print(df.to_dict(orient="records"))
"""

    result = asyncio.run(
        handle_chatq_python_tool(
            _command(tmp_path),
            {"command": f"run --code {shlex.quote(code)}"},
        )
    )

    assert result.is_error is False
    assert "600519.SH" in result.text
    assert "1688.5" in result.text


def _create_dataset(
    client: TestClient,
    *,
    name: str,
    exposed_to_agent: bool,
    create_sql: str,
) -> None:
    response = client.post(
        "/api/datasets",
        json={
            "name": name,
            "description": name,
            "category_path": ["股票", "A股"],
            "exposed_to_agent": exposed_to_agent,
            "create_sql": create_sql,
        },
    )
    assert response.status_code == 201


def _command(project_dir: Path) -> AgentExecutionCommand:
    return AgentExecutionCommand(
        project_id="project_test",
        chat_session_id="chat_1",
        user_message_id="msg_1",
        project_dir=str(project_dir),
        sdk_session_id=None,
        request_id="req_1",
        user_prompt="执行 Python",
    )
