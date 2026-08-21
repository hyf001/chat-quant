from __future__ import annotations

import json
import logging
from pathlib import Path

from app.core.config import Settings
from app.core.logging import (
    REQUEST_ID_HEADER,
    JsonLogFormatter,
    RequestIdFilter,
    RequestLoggingMiddleware,
    configure_logging,
    current_request_id,
)
from app.service.log import LogService, log_service
from fastapi import FastAPI
from fastapi.responses import JSONResponse
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


def test_request_logging_middleware_logs_successful_requests(capsys) -> None:
    configure_logging(Settings(log_level="INFO"))
    app = FastAPI()
    app.add_middleware(RequestLoggingMiddleware, slow_threshold_ms=10_000)

    @app.get("/probe")
    async def probe() -> dict[str, bool]:
        return {"ok": True}

    response = TestClient(app).get("/probe", headers={REQUEST_ID_HEADER: "req_fast"})

    assert response.status_code == 200
    payloads = [json.loads(line) for line in capsys.readouterr().out.splitlines()]
    request_payload = next(payload for payload in payloads if payload["logger"] == "app.request")
    assert request_payload["message"] == "request completed"
    assert request_payload["level"] == "INFO"
    assert request_payload["category"] == "access"
    assert request_payload["request_id"] == "req_fast"
    assert request_payload["method"] == "GET"
    assert request_payload["path"] == "/probe"
    assert request_payload["status_code"] == 200


def test_request_logging_middleware_warns_for_handled_error_status(capsys) -> None:
    configure_logging(Settings(log_level="INFO"))
    app = FastAPI()
    app.add_middleware(RequestLoggingMiddleware, slow_threshold_ms=10_000)

    @app.get("/probe")
    async def probe() -> JSONResponse:
        return JSONResponse({"ok": False}, status_code=502)

    response = TestClient(app).get("/probe", headers={REQUEST_ID_HEADER: "req_error"})

    assert response.status_code == 502
    payloads = [json.loads(line) for line in capsys.readouterr().out.splitlines()]
    request_payload = next(payload for payload in payloads if payload["logger"] == "app.request")
    assert request_payload["message"] == "request completed with error status"
    assert request_payload["level"] == "WARNING"
    assert request_payload["category"] == "access"
    assert request_payload["request_id"] == "req_error"
    assert request_payload["status_code"] == 502
    assert request_payload["error"] == "request returned HTTP 502"


def test_log_service_reads_json_lines_and_filters_categories(tmp_path: Path) -> None:
    log_file = tmp_path / "web-api.log"
    _write_log_lines(
        log_file,
        [
            'INFO:     127.0.0.1:1 - "GET /api/config HTTP/1.1" 200 OK',
            {
                "timestamp": "2026-08-13T08:00:00+00:00",
                "level": "INFO",
                "logger": "app.service.strategy.strategy_service",
                "message": "strategy created",
            },
            {
                "timestamp": "2026-08-13T08:00:01+00:00",
                "level": "INFO",
                "logger": "uvicorn.access",
                "message": '127.0.0.1:1 - "GET /api/config HTTP/1.1" 200',
            },
        ],
    )

    business = LogService(log_file).list_logs(category="business", limit=5)
    access = LogService(log_file).list_logs(category="access", limit=5)

    assert [item.logger for item in business.items] == ["app.service.strategy.strategy_service"]
    assert business.items[0].category == "business"
    assert [item.logger for item in access.items] == ["uvicorn.access"]
    assert access.items[0].category == "access"


def test_logs_api_filters_by_category(client: TestClient, tmp_path: Path) -> None:
    log_file = tmp_path / "web-api.log"
    _write_log_lines(
        log_file,
        [
            {
                "timestamp": "2026-08-13T08:00:00+00:00",
                "level": "WARNING",
                "logger": "app.request",
                "message": "request event",
                "category": "access",
                "path": "/api/probe",
            },
            {
                "timestamp": "2026-08-13T08:00:01+00:00",
                "level": "WARNING",
                "logger": "app.tests.logs_api",
                "message": "business event",
                "category": "business",
            },
        ],
    )
    from app.api.v1 import log_api

    client.app.dependency_overrides[log_api.log_service] = lambda: LogService(log_file)
    try:
        response = client.get("/api/logs?category=access&limit=5")
    finally:
        client.app.dependency_overrides.pop(log_api.log_service, None)
    assert response.status_code == 200
    payload = response.json()
    assert payload["items"]
    assert all(item["category"] == "access" for item in payload["items"])
    assert any(item["logger"] == "app.request" for item in payload["items"])


def test_log_service_filters_entries() -> None:
    response = log_service().list_logs(category="business", limit=5)

    assert all(item.category == "business" for item in response.items)


def test_warning_and_error_logs_include_error_and_stack_context(capsys) -> None:
    configure_logging(Settings(log_level="DEBUG"))
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

    items = [json.loads(line) for line in capsys.readouterr().out.splitlines()]
    warning = next(item for item in items if item["logger"] == "app.tests.warning")
    error = next(item for item in items if item["logger"] == "app.tests.error")
    assert warning["level"] == "WARNING"
    assert warning["error"] == "threshold exceeded"
    assert warning["stack"]
    assert error["level"] == "ERROR"
    assert error["error"] == "boom"
    assert "RuntimeError: boom" in error["exception"]


def _write_log_lines(log_file: Path, lines: list[str | dict[str, object]]) -> None:
    log_file.write_text(
        "".join(
            f"{line}\n" if isinstance(line, str) else f"{json.dumps(line)}\n" for line in lines
        ),
        encoding="utf-8",
    )
