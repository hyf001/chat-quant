from fastapi.testclient import TestClient


def test_stock_pool_api_manages_pools_and_stocks(
    client: TestClient,
    project_test: None,
) -> None:
    listed_empty = client.get("/api/stock-pools?project_id=project_test")

    assert listed_empty.status_code == 200
    assert listed_empty.json() == {"items": [], "total": 0}

    created = client.post(
        "/api/stock-pools",
        json={
            "project_id": "project_test",
            "name": "核心资产",
            "description": "长期跟踪",
        },
    )

    assert created.status_code == 201
    pool = created.json()
    assert pool["id"].startswith("sp_")
    assert pool["project_id"] == "project_test"
    assert pool["name"] == "核心资产"
    assert pool["description"] == "长期跟踪"
    assert pool["stock_count"] == 0

    duplicate = client.post(
        "/api/stock-pools",
        json={
            "project_id": "project_test",
            "name": "核心资产",
        },
    )
    assert duplicate.status_code == 409

    added = client.post(
        f"/api/stock-pools/{pool['id']}/stocks",
        json={
            "symbol": "600519.sh",
            "name": " 贵州茅台 ",
            "tags": ["白酒", "消费", "白酒", ""],
            "note": "核心观察",
        },
    )

    assert added.status_code == 201
    stock = added.json()
    assert stock["id"].startswith("sps_")
    assert stock["symbol"] == "600519.SH"
    assert stock["name"] == "贵州茅台"
    assert stock["tags"] == ["白酒", "消费"]

    duplicate_stock = client.post(
        f"/api/stock-pools/{pool['id']}/stocks",
        json={"symbol": "600519.SH"},
    )
    assert duplicate_stock.status_code == 409

    bulk = client.post(
        f"/api/stock-pools/{pool['id']}/stocks/bulk",
        json={"symbols": "300750.sz，000001.SZ; 600519.SH\n601318.sh"},
    )

    assert bulk.status_code == 201
    assert bulk.json()["created"] == 3
    assert bulk.json()["skipped"] == 1

    detail = client.get(f"/api/stock-pools/{pool['id']}")

    assert detail.status_code == 200
    detail_payload = detail.json()
    assert detail_payload["stock_count"] == 4
    assert detail_payload["symbols"] == [
        "600519.SH",
        "300750.SZ",
        "000001.SZ",
        "601318.SH",
    ]

    updated_stock = client.patch(
        f"/api/stock-pools/stocks/{stock['id']}",
        json={
            "symbol": "600519.SH",
            "name": "贵州茅台",
            "tags": ["白酒", "核心"],
            "note": "",
        },
    )

    assert updated_stock.status_code == 200
    assert updated_stock.json()["tags"] == ["白酒", "核心"]
    assert updated_stock.json()["note"] is None

    updated_pool = client.patch(
        f"/api/stock-pools/{pool['id']}",
        json={"name": "核心资产池", "description": None},
    )

    assert updated_pool.status_code == 200
    assert updated_pool.json()["name"] == "核心资产池"
    assert updated_pool.json()["description"] is None
    assert updated_pool.json()["stock_count"] == 4

    stocks = client.get(f"/api/stock-pools/{pool['id']}/stocks")
    assert stocks.status_code == 200
    assert stocks.json()["total"] == 4

    summary = client.get(
        f"/api/stock-pools/{pool['id']}",
        params={"include_stocks": "false"},
    )
    assert summary.status_code == 200
    assert summary.json()["stock_count"] == 4
    assert summary.json()["stocks"] == []
    assert summary.json()["symbols"] == []

    first_stock_page = client.get(
        f"/api/stock-pools/{pool['id']}/stocks",
        params={"limit": 2, "offset": 0},
    )
    second_stock_page = client.get(
        f"/api/stock-pools/{pool['id']}/stocks",
        params={"limit": 2, "offset": 2},
    )
    assert first_stock_page.json()["total"] == 4
    assert [item["symbol"] for item in first_stock_page.json()["items"]] == [
        "600519.SH",
        "300750.SZ",
    ]
    assert [item["symbol"] for item in second_stock_page.json()["items"]] == [
        "000001.SZ",
        "601318.SH",
    ]

    searched_stock = client.get(
        f"/api/stock-pools/{pool['id']}/stocks",
        params={"query": "核心", "limit": 10, "offset": 0},
    )
    assert searched_stock.status_code == 200
    assert searched_stock.json()["total"] == 1
    assert searched_stock.json()["items"][0]["symbol"] == "600519.SH"

    deleted_stock = client.delete(f"/api/stock-pools/stocks/{stock['id']}")
    assert deleted_stock.status_code == 204
    assert client.get(f"/api/stock-pools/{pool['id']}").json()["stock_count"] == 3

    deleted_pool = client.delete(f"/api/stock-pools/{pool['id']}")
    assert deleted_pool.status_code == 204
    assert client.get(f"/api/stock-pools/{pool['id']}").status_code == 404


def test_stock_pool_api_requires_existing_project(client: TestClient) -> None:
    response = client.post(
        "/api/stock-pools",
        json={
            "project_id": "missing_project",
            "name": "缺失项目",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"]["error_code"] == "PROJECT_NOT_FOUND"


def test_stock_pool_api_uses_snapshot_info_dataset_for_candidates_and_import(
    client: TestClient,
    project_test: None,
) -> None:
    _create_snapshot_info_dataset(client)
    pool = client.post(
        "/api/stock-pools",
        json={
            "project_id": "project_test",
            "name": "全量A股股票",
        },
    ).json()

    candidates = client.get(
        f"/api/stock-pools/{pool['id']}/stock-candidates",
        params={"query": "贵州", "limit": 10},
    )

    assert candidates.status_code == 200
    assert candidates.json()["items"] == [
        {"symbol": "600519.SH", "name": "贵州茅台", "in_pool": False}
    ]

    first_page = client.get(
        f"/api/stock-pools/{pool['id']}/stock-candidates",
        params={"limit": 2, "offset": 0},
    )
    second_page = client.get(
        f"/api/stock-pools/{pool['id']}/stock-candidates",
        params={"limit": 2, "offset": 2},
    )
    assert first_page.json()["total"] == 3
    assert [item["symbol"] for item in first_page.json()["items"]] == [
        "000001.SZ",
        "300750.SZ",
    ]
    assert [item["symbol"] for item in second_page.json()["items"]] == ["600519.SH"]

    selected_import = client.post(
        f"/api/stock-pools/{pool['id']}/stocks/import-snapshot-info",
        json={"symbols": ["600519.SH", "000001.SZ"]},
    )
    assert selected_import.status_code == 201
    assert selected_import.json()["created"] == 2
    assert selected_import.json()["skipped"] == 0

    selected_candidates_after_import = client.get(
        f"/api/stock-pools/{pool['id']}/stock-candidates",
        params={"query": "600519", "limit": 10},
    )
    assert selected_candidates_after_import.json()["items"][0]["in_pool"] is True

    imported = client.post(
        f"/api/stock-pools/{pool['id']}/stocks/import-snapshot-info",
    )

    assert imported.status_code == 201
    assert imported.json()["source_dataset"] == "a_stock_snapshot_info"
    assert imported.json()["created"] == 1
    assert imported.json()["skipped"] == 2

    detail = client.get(f"/api/stock-pools/{pool['id']}").json()
    assert detail["symbols"] == ["000001.SZ", "600519.SH", "300750.SZ"]
    assert [(stock["symbol"], stock["name"]) for stock in detail["stocks"]] == [
        ("000001.SZ", "平安银行"),
        ("600519.SH", "贵州茅台"),
        ("300750.SZ", "宁德时代"),
    ]

    imported_again = client.post(
        f"/api/stock-pools/{pool['id']}/stocks/import-snapshot-info",
    )
    assert imported_again.json()["created"] == 0
    assert imported_again.json()["skipped"] == 3


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
