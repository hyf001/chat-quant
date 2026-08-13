from __future__ import annotations

import json
import logging
import sys
import time
import traceback
from contextvars import ContextVar
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from starlette.datastructures import MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from app.core.config import Settings

REQUEST_ID_HEADER = "X-Request-Id"
_request_id: ContextVar[str | None] = ContextVar("request_id", default=None)
_MANAGED_HANDLER_ATTR = "_chatq_managed_handler"
_RESERVED_LOG_RECORD_FIELDS = frozenset(logging.makeLogRecord({}).__dict__)
LogCategory = str


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


def current_request_id() -> str | None:
    return _request_id.get()


def configure_logging(settings: Settings) -> None:
    level = _coerce_log_level(settings.log_level)
    root_logger = logging.getLogger()

    for handler in list(root_logger.handlers):
        if getattr(handler, _MANAGED_HANDLER_ATTR, False):
            root_logger.removeHandler(handler)

    handler = logging.StreamHandler(sys.stdout)
    setattr(handler, _MANAGED_HANDLER_ATTR, True)
    handler.addFilter(RequestIdFilter())
    handler.setFormatter(JsonLogFormatter())

    root_logger.addHandler(handler)
    root_logger.setLevel(level)

    for logger_name in (
        "app",
        "app.request",
        "uvicorn",
        "uvicorn.error",
        "uvicorn.access",
        "fastapi",
    ):
        logger = logging.getLogger(logger_name)
        logger.disabled = False
        logger.propagate = True
        logger.setLevel(level)


class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = current_request_id() or "-"
        return True


class TextLogFormatter(logging.Formatter):
    def __init__(self) -> None:
        super().__init__(
            fmt="%(asctime)s %(levelname)s [%(name)s] [request_id=%(request_id)s] %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S%z",
        )

    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)
        if record.levelno < logging.WARNING:
            return message
        extra = _record_extra(record)
        error = _record_error(record, extra)
        if error and f"error={error}" not in message:
            message = f"{message}\nerror={error}"
        if record.exc_info or record.stack_info:
            return message
        stack = _record_stack(self, record)
        return f"{message}\n{stack}" if stack else message


class JsonLogFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        extra = _record_extra(record)
        payload: dict[str, Any] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "request_id": getattr(record, "request_id", "-"),
            "category": _log_category(record),
        }
        payload.update(extra)
        if record.levelno >= logging.WARNING:
            payload.setdefault("error", _record_error(record, extra))
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        stack = _record_stack(self, record)
        if stack:
            payload["stack"] = stack
        return json.dumps(payload, ensure_ascii=False, default=str)


class RequestLoggingMiddleware:
    def __init__(
        self,
        app: ASGIApp,
        *,
        enabled: bool = True,
        slow_threshold_ms: int = 1000,
    ) -> None:
        self.app = app
        self.enabled = enabled
        self.slow_threshold_ms = slow_threshold_ms
        self.logger = get_logger("app.request")

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request_id = _request_header(scope, REQUEST_ID_HEADER) or f"req_{uuid4().hex}"
        token = _request_id.set(request_id)
        started_at = time.perf_counter()
        status_code = 500

        async def send_with_request_id(message: Message) -> None:
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = int(message["status"])
                headers = MutableHeaders(scope=message)
                headers[REQUEST_ID_HEADER] = request_id
            await send(message)

        try:
            await self.app(scope, receive, send_with_request_id)
        except Exception:
            duration_ms = _duration_ms(started_at)
            if self.enabled:
                self.logger.exception(
                    "request failed",
                    extra={
                        "method": str(scope.get("method") or ""),
                        "path": str(scope.get("path") or ""),
                        "status_code": 500,
                        "duration_ms": duration_ms,
                        "client_host": _client_host(scope),
                    },
                )
            raise
        else:
            duration_ms = _duration_ms(started_at)
            if self.enabled:
                request_extra = {
                    "method": str(scope.get("method") or ""),
                    "path": str(scope.get("path") or ""),
                    "status_code": status_code,
                    "duration_ms": duration_ms,
                    "client_host": _client_host(scope),
                }
                if status_code >= 400:
                    self.logger.warning(
                        "request completed with error status",
                        extra={
                            **request_extra,
                            "error": f"request returned HTTP {status_code}",
                        },
                        stack_info=True,
                    )
                elif duration_ms >= self.slow_threshold_ms:
                    self.logger.warning(
                        "slow request completed",
                        extra={
                            **request_extra,
                            "error": (
                                f"request duration {duration_ms}ms exceeded "
                                f"{self.slow_threshold_ms}ms threshold"
                            ),
                        },
                        stack_info=True,
                    )
                else:
                    self.logger.info("request completed", extra=request_extra)
        finally:
            _request_id.reset(token)


def _duration_ms(started_at: float) -> int:
    return int((time.perf_counter() - started_at) * 1000)


def _client_host(scope: Scope) -> str | None:
    client = scope.get("client")
    if not isinstance(client, tuple) or not client:
        return None
    return str(client[0])


def _request_header(scope: Scope, header_name: str) -> str | None:
    target = header_name.lower().encode()
    for key, value in scope.get("headers", []):
        if key.lower() == target:
            return value.decode("latin-1")
    return None


def _coerce_log_level(level_name: str) -> int:
    level = logging.getLevelName(level_name.upper())
    if isinstance(level, int):
        return level
    return logging.INFO


def _log_category(record: logging.LogRecord) -> LogCategory:
    if record.name in {"app.request", "uvicorn.access"}:
        return "access"
    if record.name.startswith("app."):
        return "business"
    return "system"


def _record_extra(record: logging.LogRecord) -> dict[str, Any]:
    return {
        key: value
        for key, value in record.__dict__.items()
        if key not in _RESERVED_LOG_RECORD_FIELDS and key != "request_id"
    }


def _record_error(record: logging.LogRecord, extra: dict[str, Any]) -> str:
    error = extra.get("error")
    if error is not None:
        return str(error)
    if record.exc_info and record.exc_info[1] is not None:
        return str(record.exc_info[1])
    return record.getMessage()


def _record_stack(formatter: logging.Formatter, record: logging.LogRecord) -> str | None:
    if record.stack_info:
        return formatter.formatStack(record.stack_info)
    if record.levelno < logging.WARNING:
        return None
    return "".join(
        traceback.StackSummary.from_list(
            [
                traceback.FrameSummary(
                    record.pathname,
                    record.lineno,
                    record.funcName,
                )
            ]
        ).format()
    )


def _log_extra_value(value: Any) -> Any:
    try:
        json.dumps(value)
    except TypeError:
        return str(value)
    return value
