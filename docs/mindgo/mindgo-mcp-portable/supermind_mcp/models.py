"""Pydantic models used by tools and tests."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class ImageArtifact(BaseModel):
    id: int
    mime: str
    path: str


class ExecutionResult(BaseModel):
    stdout: list[str] = Field(default_factory=list)
    stderr: list[str] = Field(default_factory=list)
    result: Any = None
    error: dict[str, Any] | None = None
    images: list[ImageArtifact] = Field(default_factory=list)


class FileTransferItem(BaseModel):
    path: str
    size: int = 0
    type: Literal["text", "base64", "directory"] | None = None
    action: str | None = None
    local_path: str | None = None
    error: str | None = None


class SyncResult(BaseModel):
    success: bool
    synced: int = 0
    skipped: int = 0
    failed: int = 0
    total: int = 0
    directories_created: int = 0
    dry_run: bool = False
    files: list[FileTransferItem] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)


class DownloadResult(BaseModel):
    success: bool
    total: int = 0
    downloaded: int = 0
    skipped: int = 0
    failed: int = 0
    files: list[FileTransferItem] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
