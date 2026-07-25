from __future__ import annotations

import json
import logging

from app.core.config import Settings
from app.core.logging import (
    REQUEST_ID_HEADER,
    JsonLogFormatter,
    RequestIdFilter,
    RequestLoggingMiddleware,
    configure_logging,
    current_request_id,
)
from fastapi import FastAPI
from fastapi.testclient import TestClient


def test_json_logging_includes_extra_fields() -> None:
    configure_logging(Settings(log_format="json", log_level="DEBUG"))

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
    configure_logging(Settings(log_format="text", log_level="INFO"))
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
    assert "slow request completed" in captured
    assert "request_id=req_test" in captured
