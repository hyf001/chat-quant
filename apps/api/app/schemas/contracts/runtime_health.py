from __future__ import annotations

from pydantic import BaseModel


class RuntimeHealthResponse(BaseModel):
    status: str
    python_version: str
    packages: dict[str, str]
    runtime_root_writable: bool
