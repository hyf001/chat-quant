from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ProjectResponse(BaseModel):
    id: str
    local_path: str
    name: str
    description: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProjectListResponse(BaseModel):
    items: list[ProjectResponse]
    total: int
    limit: int
    offset: int


class ProjectFileEntry(BaseModel):
    name: str
    relative_path: str
    type: Literal["directory", "file"]
    size: int | None = None
    modified_at: datetime
    extension: str | None = None


class ProjectDirectoryResponse(BaseModel):
    project_id: str
    root_name: str
    current_path: str
    parent_path: str | None = None
    items: list[ProjectFileEntry]


class ProjectFileContentResponse(BaseModel):
    project_id: str
    name: str
    relative_path: str
    size: int
    modified_at: datetime
    extension: str | None = None
    content: str
    truncated: bool


class ProjectCreateRequest(BaseModel):
    local_path: str = Field(min_length=1)
    name: str | None = Field(default=None, min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=1000)


class ProjectOpenRequest(BaseModel):
    local_path: str = Field(min_length=1)
    name: str | None = Field(default=None, min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=1000)


class ProjectResolveRequest(BaseModel):
    local_path: str = Field(min_length=1)
    name: str | None = Field(default=None, min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=1000)


class ProjectUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=1000)
