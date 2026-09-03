from fastapi.testclient import TestClient


def test_stock_preview_uses_pre_adjusted_price_dataset(client: TestClient) -> None:
    _create_snapshot_info_dataset(client)
    _create_pre_adjusted_price_dataset(client)

    response = client.get(
        "/api/market/stocks/000001.sz/preview",
        params={"period": "daily", "limit": 3},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["symbol"] == "000001.SZ"
    assert payload["name"] == "平安银行"
    assert payload["period"] == "daily"
    assert payload["trade_date"] == "2026-09-03"
    assert payload["close"] == 11.0
    assert payload["prev_close"] == 10.5
    assert payload["change"] == 0.5
    assert round(payload["pct_change"], 4) == 4.7619
    assert payload["source_dataset"] == "a_stock_daily_price_pre_adjusted"
    assert [item["date"] for item in payload["candles"]] == [
        "2026-09-01",
        "2026-09-02",
        "2026-09-03",
    ]


def test_stock_preview_returns_error_without_pre_adjusted_dataset(
    client: TestClient,
) -> None:
    _create_snapshot_info_dataset(client)
    _create_unadjusted_price_dataset(client)

    response = client.get("/api/market/stocks/000001.SZ/preview")

    assert response.status_code == 422
    assert response.json()["detail"]["error_code"] == "STOCK_PREVIEW_PRICE_UNAVAILABLE"
    assert response.json()["detail"]["dataset"] == "a_stock_daily_price_pre_adjusted"


def test_stock_preview_aggregates_monthly_from_pre_adjusted_daily(
    client: TestClient,
) -> None:
    _create_snapshot_info_dataset(client)
    _create_pre_adjusted_price_dataset(client)

    response = client.get(
        "/api/market/stocks/000001.SZ/preview",
        params={"period": "monthly", "limit": 2},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["period"] == "monthly"
    assert [item["date"] for item in payload["candles"]] == ["2026-08-29", "2026-09-03"]
    assert payload["candles"][0]["open"] == 8.0
    assert payload["candles"][0]["high"] == 9.4
    assert payload["candles"][0]["low"] == 7.8
    assert payload["candles"][0]["close"] == 9.2


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
                "SELECT '000001.SZ' AS symbol, '平安银行' AS name"
            ),
        },
    )
    assert response.status_code == 201


def _create_pre_adjusted_price_dataset(client: TestClient) -> None:
    response = client.post(
        "/api/datasets",
        json={
            "name": "a_stock_daily_price_pre_adjusted",
            "description": "A股前复权日行情",
            "category_path": ["A股", "股票", "日", "行情数据（前复权）"],
            "exposed_to_agent": True,
            "create_sql": (
                "CREATE VIEW a_stock_daily_price_pre_adjusted AS "
                "SELECT '000001.SZ' AS symbol, '20260828' AS trade_date, "
                "8.0 AS open, 9.0 AS high, 7.8 AS low, 8.8 AS close, "
                "1000.0 AS volume, 8000.0 AS turnover "
                "UNION ALL SELECT '000001.SZ', '20260829', "
                "8.9, 9.4, 8.6, 9.2, 1200.0, 11000.0 "
                "UNION ALL SELECT '000001.SZ', '20260901', "
                "10.0, 10.3, 9.8, 10.2, 1300.0, 13000.0 "
                "UNION ALL SELECT '000001.SZ', '20260902', "
                "10.2, 10.6, 10.1, 10.5, 1400.0, 15000.0 "
                "UNION ALL SELECT '000001.SZ', '20260903', "
                "10.6, 11.2, 10.4, 11.0, 1500.0, 17000.0"
            ),
        },
    )
    assert response.status_code == 201


def _create_unadjusted_price_dataset(client: TestClient) -> None:
    response = client.post(
        "/api/datasets",
        json={
            "name": "a_stock_daily_price",
            "description": "A股未复权日行情",
            "category_path": ["A股", "股票", "日", "行情数据"],
            "exposed_to_agent": True,
            "create_sql": (
                "CREATE VIEW a_stock_daily_price AS "
                "SELECT '000001.SZ' AS symbol, '20260903' AS trade_date, 11.0 AS close"
            ),
        },
    )
    assert response.status_code == 201
