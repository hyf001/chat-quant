from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.contracts.json_types import JsonObject

RuntimeArtifactType = Literal[
    "json_result",
    "chart",
    "curve",
    "table",
    "image",
    "html",
    "log",
    "file",
]
RuntimeStatus = Literal["succeeded", "failed", "timeout", "canceled"]
RuntimeErrorPhase = Literal[
    "prepare",
    "execute",
    "timeout",
    "collect",
    "schema_validation",
    "persist",
]


class RuntimeArtifact(BaseModel):
    type: RuntimeArtifactType
    path: str
    name: str | None = None
    mime_type: str | None = None
    size_bytes: int | None = None
    checksum: str | None = None
    metadata: JsonObject = Field(default_factory=dict)


class RuntimeErrorInfo(BaseModel):
    code: str
    message: str
    detail: str | None = None
    traceback: str | None = None
    phase: RuntimeErrorPhase


class ExecutionResult(BaseModel):
    id: str | None = None
    run_id: str
    status: RuntimeStatus
    exit_code: int | None
    stdout: str
    stderr: str
    artifacts: list[RuntimeArtifact] = Field(default_factory=list)
    error: RuntimeErrorInfo | None = None
    duration_ms: int
    started_at: datetime
    completed_at: datetime
    python_version: str
    command: list[str]
    cwd: str
    output_dir: str
    schema_validation: JsonObject = Field(default_factory=dict)
    metadata: JsonObject = Field(default_factory=dict)


class ExecutionResultEnvelope(BaseModel):
    execution_result: ExecutionResult
