from fastapi.testclient import TestClient


def test_dataset_api_creates_and_lists_dataset_metadata(client: TestClient) -> None:
    response = client.post(
        "/api/datasets",
        json={
            "name": "a_stock_daily_price_pre_adjusted",
            "description": "A股前复权日行情",
            "category_path": ["A股", "股票", "日", "行情数据（前复权）"],
            "exposed_to_agent": True,
            "create_sql": (
                "CREATE VIEW a_stock_daily_price_pre_adjusted AS "
                "SELECT '000001.SZ' AS symbol, 10.0 AS close"
            ),
        },
    )

    assert response.status_code == 201
    dataset = response.json()
    assert dataset["id"] == "a_stock_daily_price_pre_adjusted"
    assert dataset["name"] == "a_stock_daily_price_pre_adjusted"
    assert dataset["name_zh"] == "A股前复权日行情"
    assert dataset["name_en"] == "a_stock_daily_price_pre_adjusted"
    assert dataset["description"] == "A股前复权日行情"
    assert dataset["category_path"] == ["A股", "股票", "日", "行情数据（前复权）"]
    assert dataset["category_path_en"] == [
        "a",
        "stock",
        "daily",
        "price_pre_adjusted",
    ]
    assert dataset["exposed_to_agent"] is True
    assert dataset["create_sql"].startswith(
        "CREATE VIEW a_stock_daily_price_pre_adjusted AS"
    )
    assert dataset["created_at"]
    assert dataset["updated_at"]

    list_response = client.get("/api/datasets?exposed_to_agent=true")

    assert list_response.status_code == 200
    assert [item["id"] for item in list_response.json()["datasets"]] == [
        "a_stock_daily_price_pre_adjusted"
    ]


def test_dataset_api_returns_naming_options(client: TestClient) -> None:
    response = client.get("/api/datasets/naming-options")

    assert response.status_code == 200
    payload = response.json()
    assert {"value": "A股", "label": "A股", "name_en": "a"} in payload["markets"]
    assert {"value": "股票", "label": "股票", "name_en": "stock"} in payload[
        "asset_classes"
    ]
    assert {"value": "日", "label": "日", "name_en": "daily"} in payload["frequencies"]


def test_dataset_api_updates_and_deletes_dataset_metadata(client: TestClient) -> None:
    client.post(
        "/api/datasets",
        json={
            "name": "a_stock_daily_adjust_factor",
            "description": "A股复权因子",
            "category_path": ["A股", "股票", "日", "复权因子"],
            "exposed_to_agent": False,
            "create_sql": (
                "CREATE VIEW a_stock_daily_adjust_factor AS "
                "SELECT '000001.SZ' AS symbol, 1.0 AS adjust_factor"
            ),
        },
    )

    update_response = client.put(
        "/api/datasets/a_stock_daily_adjust_factor",
        json={
            "description": "A股日频复权因子",
            "category_path": ["A股", "股票", "日", "行情数据"],
            "exposed_to_agent": True,
        },
    )

    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["name"] == "a_stock_daily_adjust_factor"
    assert updated["description"] == "A股日频复权因子"
    assert updated["name_zh"] == "A股日频复权因子"
    assert updated["name_en"] == "a_stock_daily_adjust_factor"
    assert updated["category_path"] == ["A股", "股票", "日", "行情数据"]
    assert updated["category_path_en"] == ["a", "stock", "daily", "adjust_factor"]
    assert updated["exposed_to_agent"] is True

    delete_response = client.delete("/api/datasets/a_stock_daily_adjust_factor")

    assert delete_response.status_code == 204
    assert client.get("/api/datasets/a_stock_daily_adjust_factor").status_code == 404


def test_dataset_api_rejects_duplicate_duckdb_view_name(client: TestClient) -> None:
    payload = {
        "name": "a_stock_daily_price_pre_adjusted",
        "description": "A股前复权日行情",
        "category_path": ["A股", "股票", "日", "行情数据"],
        "exposed_to_agent": True,
        "create_sql": (
            "CREATE VIEW a_stock_daily_price_pre_adjusted AS "
            "SELECT '000001.SZ' AS symbol, 10.0 AS close"
        ),
    }
    first_response = client.post("/api/datasets", json=payload)
    second_response = client.post(
        "/api/datasets",
        json={
            **payload,
            "name": "a_stock_daily_price_pre_adjusted",
        },
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409


def test_dataset_api_stores_category_path_as_submitted(client: TestClient) -> None:
    response = client.post(
        "/api/datasets",
        json={
            "name": "a_stock_daily_price_legacy_path",
            "description": "A股旧路径兼容",
            "category_path": ["股票", "A股", "行情数据"],
            "exposed_to_agent": True,
            "create_sql": (
                "CREATE VIEW a_stock_daily_price_legacy_path AS "
                "SELECT '000001.SZ' AS symbol, 10.0 AS close"
            ),
        },
    )

    assert response.status_code == 201
    assert response.json()["category_path"] == ["股票", "A股", "行情数据"]
    assert response.json()["category_path_en"] == []


def test_dataset_api_accepts_custom_category_topic(client: TestClient) -> None:
    response = client.post(
        "/api/datasets",
        json={
            "name": "a_stock_daily_adjust_factor",
            "description": "A股英文路径兼容",
            "category_path": ["A股", "股票", "日", "自定义因子"],
            "exposed_to_agent": True,
            "create_sql": (
                "CREATE VIEW a_stock_daily_adjust_factor AS "
                "SELECT '000001.SZ' AS symbol, 1.0 AS factor"
            ),
        },
    )

    assert response.status_code == 201
    assert response.json()["category_path"] == ["A股", "股票", "日", "自定义因子"]
    assert response.json()["category_path_en"] == [
        "a",
        "stock",
        "daily",
        "adjust_factor",
    ]


def test_dataset_api_accepts_short_category_path(client: TestClient) -> None:
    response = client.post(
        "/api/datasets",
        json={
            "name": "a_stock_daily_price_unknown_path",
            "description": "A股未知路径",
            "category_path": ["股票", "A股"],
            "exposed_to_agent": True,
            "create_sql": (
                "CREATE VIEW a_stock_daily_price_unknown_path AS "
                "SELECT '000001.SZ' AS symbol, 10.0 AS close"
            ),
        },
    )

    assert response.status_code == 201
    assert response.json()["category_path"] == ["股票", "A股"]
    assert response.json()["category_path_en"] == []


def test_dataset_api_gets_duckdb_create_view_sql(client: TestClient) -> None:
    create_sql = (
        "CREATE VIEW a_stock_daily_price_forward_adjusted AS "
        "SELECT '000001.SZ' AS symbol, 11.0 AS close"
    )
    response = client.post(
        "/api/datasets",
        json={
            "name": "a_stock_daily_price_forward_adjusted",
            "description": "A股前复权日行情",
            "category_path": ["A股", "股票", "日", "行情数据"],
            "exposed_to_agent": True,
            "create_sql": create_sql,
        },
    )

    assert response.status_code == 201

    detail_response = client.get("/api/datasets/a_stock_daily_price_forward_adjusted")

    assert detail_response.status_code == 200
    detail = detail_response.json()
    assert detail["name"] == "a_stock_daily_price_forward_adjusted"
    assert detail["create_sql"].startswith(
        "CREATE VIEW a_stock_daily_price_forward_adjusted AS"
    )


def test_dataset_api_queries_dataset_views_with_sql(client: TestClient) -> None:
    response = client.post(
        "/api/datasets",
        json={
            "name": "a_stock_daily_price_queryable",
            "description": "A股行情查询视图",
            "category_path": ["A股", "股票", "日", "行情数据"],
            "exposed_to_agent": True,
            "create_sql": (
                "CREATE VIEW a_stock_daily_price_queryable AS "
                "SELECT '000001.SZ' AS symbol, 10.0 AS close "
                "UNION ALL SELECT '000002.SZ' AS symbol, 12.0 AS close"
            ),
        },
    )
    assert response.status_code == 201

    query_response = client.post(
        "/api/datasets/query",
        json={
            "sql": (
                "SELECT symbol, close FROM a_stock_daily_price_queryable "
                "ORDER BY symbol"
            ),
            "page": 1,
            "page_size": 1,
        },
    )

    assert query_response.status_code == 200
    result = query_response.json()
    assert result["total"] == 2
    assert result["total_pages"] == 2
    assert [column["name"] for column in result["columns"]] == ["symbol", "close"]
    assert result["rows"] == [{"symbol": "000001.SZ", "close": 10.0}]


def test_dataset_api_rejects_non_select_sql_query(client: TestClient) -> None:
    query_response = client.post(
        "/api/datasets/query",
        json={"sql": "DROP VIEW missing_view", "page": 1, "page_size": 50},
    )

    assert query_response.status_code == 400
