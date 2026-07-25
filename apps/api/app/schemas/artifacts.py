from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from app.domain.artifacts.models import ArtifactFileRole, ArtifactStatus, ArtifactType

type JsonValue = str | int | float | bool | None | list[JsonValue] | dict[str, JsonValue]
type JsonObject = dict[str, JsonValue]


class CodeArtifactFileCreate(BaseModel):
    relative_path: str
    content: str
    file_role: ArtifactFileRole
    checksum: str | None = None
    render_metadata: JsonObject = Field(default_factory=dict)


class SaveCodeArtifactRequest(BaseModel):
    chat_session_id: str
    artifact_type: ArtifactType
    title: str
    files: list[CodeArtifactFileCreate]
    user_id: str = "local_user"
    project_id: str = "local_project"
    source_sdk_session_id: str | None = None
    source_sdk_message_uuid: str | None = None
    source_sdk_tool_use_id: str | None = None
    parent_artifact_id: str | None = None
    description: str | None = None
    entrypoint: str | None = None
    metadata: JsonObject = Field(default_factory=dict)


class GeneratedFileCreate(BaseModel):
    source_path: str
    file_role: ArtifactFileRole
    title: str | None = None
    render_metadata: JsonObject = Field(default_factory=dict)
    checksum: str | None = None


class SaveGeneratedFilesRequest(BaseModel):
    chat_session_id: str
    source_base_dir: str
    files: list[GeneratedFileCreate]
    user_id: str = "local_user"
    project_id: str = "local_project"
    parent_artifact_id: str | None = None
    source_sdk_session_id: str | None = None
    source_sdk_message_uuid: str | None = None
    source_sdk_tool_use_id: str | None = None
    backtest_run_id: str | None = None
    title: str | None = None
    metadata: JsonObject = Field(default_factory=dict)


class ArtifactFileResponse(BaseModel):
    file_id: str
    artifact_id: str
    relative_path: str
    file_role: ArtifactFileRole
    storage_uri: str
    mime_type: str
    size_bytes: int
    checksum: str
    is_entrypoint: bool
    render_metadata: JsonObject
    download_url: str
    preview_url: str | None
    created_at: str

    model_config = ConfigDict(from_attributes=True)


class CodeArtifactResponse(BaseModel):
    artifact_id: str
    user_id: str
    project_id: str
    chat_session_id: str
    artifact_type: ArtifactType
    title: str
    version: int
    entrypoint: str | None
    checksum: str
    root_path: str
    status: ArtifactStatus
    files: list[ArtifactFileResponse]
    description: str | None = None
    source_sdk_session_id: str | None = None
    source_sdk_message_uuid: str | None = None
    source_sdk_tool_use_id: str | None = None
    main_file_id: str | None = None
    metadata: JsonObject
    created_at: str
    updated_at: str

    model_config = ConfigDict(from_attributes=True)


class ArtifactListResponse(BaseModel):
    items: list[CodeArtifactResponse]


class ArtifactEntrypointResponse(BaseModel):
    artifact_id: str
    artifact_type: ArtifactType
    entrypoint: str
    absolute_root_path: str
    main_file: str
    checksum: str
