from __future__ import annotations

from typing import Any

import pandas as pd

from app.service.dataset.python_api import DatasetPythonApiError, query_dataset


class ChatQStrategyRuntimeError(RuntimeError):
    def __init__(
        self,
        error_code: str,
        message: str,
        *,
        detail: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.error_code = error_code
        self.message = message
        self.detail = detail or {}

    def __str__(self) -> str:
        if not self.detail:
            return f"{self.error_code}: {self.message}"
        return f"{self.error_code}: {self.message} ({self.detail})"


class ChatQStrategyRuntime:
    """Read-only platform services exposed to generated Backtrader strategies."""

    def sql(self, sql: str) -> pd.DataFrame:
        return self.query_dataset(sql)

    def query_dataset(self, sql: str) -> pd.DataFrame:
        try:
            return query_dataset(sql)
        except DatasetPythonApiError as exc:
            raise ChatQStrategyRuntimeError(
                exc.error_code,
                exc.message,
                detail=exc.detail,
            ) from exc
