from __future__ import annotations

from typing import Protocol

import pandas as pd

from app.schema.mindgo import (
    MindgoSourceQueryRequest,
    MindgoSourceSchema,
    MindgoSourceSyncRequest,
    MindgoSourceSyncResult,
)


class MindgoSourceAdapter(Protocol):
    """Protocol implemented by each MindGo source adapter."""

    source_id: str

    async def get_source_schema(self) -> MindgoSourceSchema:
        """Return the MindGo source schema used by sync and source inspection."""

    async def query_from_mindgo(self, request: MindgoSourceQueryRequest) -> pd.DataFrame:
        """Run a remote MindGo source query and return a normalized pandas DataFrame."""

    async def sync(self, request: MindgoSourceSyncRequest) -> MindgoSourceSyncResult:
        """Synchronize this MindGo source into local storage."""
