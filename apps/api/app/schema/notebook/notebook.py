from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


class NotebookFileEntry(BaseModel):
    name: str
    relative_path: str
    size: int
    modified_at: str


class NotebookFileListResponse(BaseModel):
    project_id: str
    root_dir: str
    files: list[NotebookFileEntry]


class NotebookCreateRequest(BaseModel):
    name: str | None = None


class NotebookDeleteRequest(BaseModel):
    path: str


class NotebookRenameRequest(BaseModel):
    path: str
    name: str


class NotebookSessionRequest(BaseModel):
    path: str


class NotebookSessionResponse(BaseModel):
    path: str
    session_id: str | None = None
    kernel_id: str | None = None
    kernel_name: str | None = None


class NotebookServerResponse(BaseModel):
    project_id: str
    status: Literal["starting", "running", "stopped", "error"]
    url: str
    base_url: str
    token: str
    root_dir: str
    pid: int
    runtime_id: str
    detail: str | None = None


class NotebookServerStatusResponse(BaseModel):
    project_id: str
    status: Literal["running", "stopped"]
    url: str | None = None
    base_url: str | None = None
    root_dir: str | None = None
    pid: int | None = None
    runtime_id: str | None = None
