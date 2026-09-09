import pytest
from app.service.stock_pool.python_api import (
    StockPoolPythonApiError,
    add_pool_stocks,
    get_stock_pool,
    list_pool_stocks,
    list_stock_pools,
    stock_pool_symbols,
    stock_pool_symbols_by_tag,
    stock_pool_tags,
)
from fastapi.testclient import TestClient


def test_stock_pool_python_api_reads_pools_and_stocks(
    client: TestClient,
    project_test: None,
) -> None:
    pool_id = _create_pool(client, "核心资产")
    _add_stock(client, pool_id, "600519.sh", name="贵州茅台", tags=["白酒", "消费"])
    _add_stock(client, pool_id, "300750.SZ", name="宁德时代", tags=["新能源"])

    pools = list_stock_pools(project_id="project_test")
    assert pools["name"].tolist() == ["核心资产"]
    assert pools["stock_count"].tolist() == [2]

    stocks = list_pool_stocks("核心资产", project_id="project_test")
    assert stocks["symbol"].tolist() == ["600519.SH", "300750.SZ"]

    detail = get_stock_pool("核心资产", project_id="project_test")
    assert detail["id"] == pool_id
    assert detail["symbols"] == ["600519.SH", "300750.SZ"]
    assert detail["stock_count"] == 2
    assert get_stock_pool("核心资产", project_id="project_test", limit=1)["symbols"] == [
        "600519.SH"
    ]
    assert list_pool_stocks("核心资产", project_id="project_test", limit=1)["symbol"].tolist() == [
        "600519.SH"
    ]
    assert stock_pool_symbols(pool_id) == ["600519.SH", "300750.SZ"]
    assert stock_pool_symbols(pool_id, limit=1) == ["600519.SH"]
    assert stock_pool_tags("核心资产", "600519.sh", project_id="project_test") == [
        "白酒",
        "消费",
    ]
    assert stock_pool_symbols_by_tag("核心资产", "新能源", project_id="project_test") == [
        "300750.SZ"
    ]
    assert stock_pool_symbols_by_tag(
        "核心资产",
        "新能源",
        project_id="project_test",
        limit=1,
    ) == ["300750.SZ"]


def test_stock_pool_python_api_requires_project_for_ambiguous_name(
    client: TestClient,
    project_test: None,
    tmp_path,
) -> None:
    pool_a = _create_pool(client, "同名池")
    project_b = client.post(
        "/api/projects/create",
        json={"local_path": str(tmp_path / "project-b"), "name": "项目 B"},
    ).json()
    client.post(
        "/api/stock-pools",
        json={"project_id": project_b["id"], "name": "同名池"},
    )

    with pytest.raises(StockPoolPythonApiError, match="STOCK_POOL_AMBIGUOUS"):
        get_stock_pool("同名池")

    assert get_stock_pool(pool_a)["project_id"] == "project_test"


def test_add_pool_stocks_adds_symbols_from_python_api(
    client: TestClient,
    project_test: None,
) -> None:
    _create_snapshot_info_dataset(client)
    pool_id = _create_pool(client, "观察池")

    result = add_pool_stocks(
        "观察池",
        "600519.sh, 300750.SZ, 600519.SH",
        project_id="project_test",
        tags=["核心", "核心", "消费"],
        note={
            "600519.sh": "白酒龙头",
            "300750.SZ": "电池龙头",
        },
    )

    assert result["created"] == 2
    assert result["skipped"] == 0
    assert result["missing_from_dataset"] == []
    assert [(item["symbol"], item["name"], item["tags"]) for item in result["items"]] == [
        ("600519.SH", "贵州茅台", ["核心", "消费"]),
        ("300750.SZ", "宁德时代", ["核心", "消费"]),
    ]
    assert [(item["symbol"], item["note"]) for item in result["items"]] == [
        ("600519.SH", "白酒龙头"),
        ("300750.SZ", "电池龙头"),
    ]

    added_again = add_pool_stocks(pool_id, ["300750.sz", "000001.SZ"])
    assert added_again["created"] == 1
    assert added_again["skipped"] == 1

    missing = add_pool_stocks(pool_id, ["999999.SH"])
    assert missing["created"] == 0
    assert missing["skipped"] == 1
    assert missing["missing_from_dataset"] == ["999999.SH"]

    detail = get_stock_pool("观察池", project_id="project_test")
    assert detail["symbols"] == ["600519.SH", "300750.SZ", "000001.SZ"]
    assert [stock["name"] for stock in detail["stocks"]] == [
        "贵州茅台",
        "宁德时代",
        "平安银行",
    ]


def _create_pool(client: TestClient, name: str) -> str:
    response = client.post(
        "/api/stock-pools",
        json={
            "project_id": "project_test",
            "name": name,
        },
    )
    assert response.status_code == 201
    return str(response.json()["id"])


def _create_snapshot_info_dataset(client: TestClient) -> None:
    response = client.post(
        "/api/datasets",
        json={
            "name": "a_stock_snapshot_info",
            "description": "A股股票信息维表",
            "category_path": ["A股", "股票", "快照", "信息维表"],
            "exposed_to_agent": True,
            "create_sql": (
                "CREATE VIEW a_stock_snapshot_info AS "
                "SELECT '600519.SH' AS symbol, '贵州茅台' AS name "
                "UNION ALL SELECT '300750.SZ' AS symbol, '宁德时代' AS name "
                "UNION ALL SELECT '000001.SZ' AS symbol, '平安银行' AS name"
            ),
        },
    )
    assert response.status_code == 201


def _add_stock(
    client: TestClient,
    pool_id: str,
    symbol: str,
    *,
    name: str,
    tags: list[str],
) -> None:
    response = client.post(
        f"/api/stock-pools/{pool_id}/stocks",
        json={
            "symbol": symbol,
            "name": name,
            "tags": tags,
        },
    )
    assert response.status_code == 201
