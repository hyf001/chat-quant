from __future__ import annotations

from typing import Protocol

import pandas as pd

from app.schema.mindgo import (
    MindgoDatasetQueryRequest,
    MindgoDatasetSchema,
    MindgoDatasetSyncRequest,
    MindgoDatasetSyncResult,
)


class MindgoDatasetAdapter(Protocol):
    """Protocol implemented by each MindGo dataset adapter."""

    dataset_id: str

    async def get_schema(self) -> MindgoDatasetSchema:
        """Return the dataset schema used by frontend rendering and validation."""

    async def query_from_mindgo(self, request: MindgoDatasetQueryRequest) -> pd.DataFrame:
        """Run a remote dataset query and return a normalized pandas DataFrame."""

    async def query_from_duckdb(self, sql: str) -> pd.DataFrame:
        """Run a local DuckDB SQL query and return a pandas DataFrame."""

    async def sync(self, request: MindgoDatasetSyncRequest) -> MindgoDatasetSyncResult:
        """Execute dataset synchronization and return status, elapsed time, and count."""
