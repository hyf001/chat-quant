from __future__ import annotations

import json
import logging

from app.core.config import Settings
from app.core.logging import (
    REQUEST_ID_HEADER,
    JsonLogFormatter,
    RequestIdFilter,
    RequestLoggingMiddleware,
    clear_log_entries,
    configure_logging,
    current_request_id,
    recent_log_entries,
)
from app.service.log import log_service
from fastapi import FastAPI
from fastapi.testclient import TestClient


def test_json_logging_includes_extra_fields() -> None:
    configure_logging(Settings(log_level="DEBUG"))

    record = logging.getLogger().makeRecord(
        "app.tests.logging",
        logging.DEBUG,
        __file__,
        1,
        "structured event",
        (),
        None,
        extra={"artifact_id": "ca_1"},
    )
    RequestIdFilter().filter(record)
    payload = json.loads(JsonLogFormatter().format(record))
    assert payload["level"] == "DEBUG"
    assert payload["logger"] == "app.tests.logging"
    assert payload["message"] == "structured event"
    assert payload["artifact_id"] == "ca_1"
    assert payload["request_id"] == "-"


def test_request_logging_middleware_propagates_request_id(capsys) -> None:
    configure_logging(Settings(log_level="INFO"))
    app = FastAPI()
    app.add_middleware(RequestLoggingMiddleware, slow_threshold_ms=0)

    @app.get("/probe")
    async def probe() -> dict[str, str | None]:
        logging.getLogger("app.tests.probe").info("inside request")
        return {"request_id": current_request_id()}

    response = TestClient(app).get("/probe", headers={REQUEST_ID_HEADER: "req_test"})

    assert response.status_code == 200
    assert response.headers[REQUEST_ID_HEADER] == "req_test"
    assert response.json() == {"request_id": "req_test"}
    captured = capsys.readouterr().out
    payloads = [json.loads(line) for line in captured.splitlines()]
    request_payload = next(payload for payload in payloads if payload["logger"] == "app.request")
    assert request_payload["message"] == "slow request completed"
    assert request_payload["request_id"] == "req_test"


def test_logs_api_returns_recent_entries(client: TestClient) -> None:
    clear_log_entries()
    logging.getLogger("app.tests.logs_api").warning("visible system event")

    response = client.get("/api/logs?limit=5")

    assert response.status_code == 200
    payload = response.json()
    assert any(
        item["logger"] == "app.tests.logs_api" and item["message"] == "visible system event"
        for item in payload["items"]
    )
    assert any(item["category"] == "business" for item in payload["items"])


def test_recent_log_entries_filters_access_and_business_logs() -> None:
    clear_log_entries()
    logging.getLogger("app.request").warning(
        "slow request completed",
        extra={"path": "/api/probe", "status_code": 200, "duration_ms": 10},
    )
    logging.getLogger("app.service.probe").warning("business event")

    access_entries = recent_log_entries(category="access")
    business_entries = recent_log_entries(category="business")

    assert len(access_entries) == 1
    assert access_entries[0]["logger"] == "app.request"
    assert access_entries[0]["category"] == "access"
    assert access_entries[0]["path"] == "/api/probe"
    assert len(business_entries) == 1
    assert business_entries[0]["logger"] == "app.service.probe"
    assert business_entries[0]["category"] == "business"


def test_logs_api_filters_by_category(client: TestClient) -> None:
    clear_log_entries()
    logging.getLogger("app.request").warning("request event", extra={"path": "/api/probe"})
    logging.getLogger("app.tests.logs_api").warning("business event")

    response = client.get("/api/logs?category=access&limit=5")

    assert response.status_code == 200
    payload = response.json()
    assert payload["items"]
    assert all(item["category"] == "access" for item in payload["items"])
    assert any(item["logger"] == "app.request" for item in payload["items"])


def test_log_service_filters_entries() -> None:
    clear_log_entries()
    logging.getLogger("app.request").warning("request event", extra={"path": "/api/probe"})
    logging.getLogger("app.tests.logs_service").warning("business event")

    response = log_service().list_logs(category="business", limit=5)

    assert response.items
    assert all(item.category == "business" for item in response.items)
    assert any(item.logger == "app.tests.logs_service" for item in response.items)


def test_warning_and_error_logs_include_error_and_stack_context(client: TestClient) -> None:
    clear_log_entries()
    logging.getLogger("app.tests.warning").warning(
        "warning event",
        extra={"error": "threshold exceeded"},
        stack_info=True,
    )
    try:
        raise RuntimeError("boom")
    except RuntimeError:
        logging.getLogger("app.tests.error").exception(
            "error event",
            extra={"error": "boom"},
        )

    response = client.get("/api/logs?category=business&limit=5")

    assert response.status_code == 200
    items = response.json()["items"]
    warning = next(item for item in items if item["logger"] == "app.tests.warning")
    error = next(item for item in items if item["logger"] == "app.tests.error")
    assert warning["level"] == "WARNING"
    assert warning["error"] == "threshold exceeded"
    assert warning["stack"]
    assert error["level"] == "ERROR"
    assert error["error"] == "boom"
    assert "RuntimeError: boom" in error["exception"]
