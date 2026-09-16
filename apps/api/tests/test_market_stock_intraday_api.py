from fastapi.testclient import TestClient


def test_stock_intraday_returns_minute_points(client: TestClient) -> None:
    _create_minute_price_dataset(client)

    response = client.get(
        "/api/market/stocks/000001.sz/intraday",
        params={"date": "2026-09-14"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["symbol"] == "000001.SZ"
    assert payload["trade_date"] == "2026-09-14"
    assert payload["source_dataset"] == "a_stock_minute_price"
    assert payload["points"] == [
        {"t": "09:31", "p": 10.1, "v": 1000.0},
        {"t": "09:32", "p": 10.2, "v": 2000.0},
        {"t": "14:59", "p": 10.05, "v": 1500.0},
    ]


def test_stock_intraday_only_returns_the_requested_day(client: TestClient) -> None:
    _create_minute_price_dataset(client)

    response = client.get(
        "/api/market/stocks/000001.SZ/intraday",
        params={"date": "2026-09-13"},
    )

    assert response.status_code == 200
    assert response.json()["trade_date"] == "2026-09-13"
    assert response.json()["points"] == []


def test_stock_intraday_returns_empty_points_without_minute_dataset(client: TestClient) -> None:
    response = client.get(
        "/api/market/stocks/000001.SZ/intraday",
        params={"date": "2026-09-14"},
    )

    assert response.status_code == 200
    assert response.json()["points"] == []


def test_stock_intraday_rejects_empty_symbol_and_bad_date(client: TestClient) -> None:
    _create_minute_price_dataset(client)

    empty_symbol = client.get("/api/market/stocks/%20/intraday", params={"date": "2026-09-14"})
    assert empty_symbol.status_code == 422
    assert empty_symbol.json()["detail"]["error_code"] == "STOCK_SYMBOL_EMPTY"

    bad_date = client.get("/api/market/stocks/000001.SZ/intraday", params={"date": "2026-09-14x"})
    assert bad_date.status_code == 422

    missing_date = client.get("/api/market/stocks/000001.SZ/intraday")
    assert missing_date.status_code == 422


def _create_minute_price_dataset(client: TestClient) -> None:
    rows = [
        "SELECT '000001.SZ' AS symbol, '2026-09-14 09:31:00' AS trade_date, "
        "10.1 AS open, 10.2 AS high, 10.0 AS low, 10.1 AS close, 1000.0 AS volume",
        "SELECT '000001.SZ', '2026-09-14 09:32:00', 10.1, 10.3, 10.1, 10.2, 2000.0",
        "SELECT '000001.SZ', '2026-09-14 14:59:00', 10.0, 10.1, 9.9, 10.05, 1500.0",
        "SELECT '600000.SH', '2026-09-14 09:31:00', 8.0, 8.1, 7.9, 8.05, 500.0",
    ]
    response = client.post(
        "/api/datasets",
        json={
            "name": "a_stock_minute_price",
            "description": "A股1分钟行情",
            "category_path": ["A股", "股票", "分钟", "行情数据"],
            "exposed_to_agent": True,
            "create_sql": "CREATE VIEW a_stock_minute_price AS " + " UNION ALL ".join(rows),
        },
    )
    assert response.status_code == 201
