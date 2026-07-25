from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

type JsonValue = str | int | float | bool | None | list[JsonValue] | dict[str, JsonValue]
type JsonObject = dict[str, JsonValue]


class ArtifactType(StrEnum):
    QUERY_SCRIPT = "query_script"
    ANALYSIS_SCRIPT = "analysis_script"
    STRATEGY_SCRIPT = "strategy_script"
    BACKTEST_SCRIPT = "backtest_script"
    JSON_RESULT = "json_result"
    CHART_FILE = "chart_file"


class ArtifactFileRole(StrEnum):
    QUERY_SCRIPT = "query_script"
    ANALYSIS_SCRIPT = "analysis_script"
    STRATEGY_SCRIPT = "strategy_script"
    BACKTEST_SCRIPT = "backtest_script"
    JSON_RESULT = "json_result"
    CHART_FILE = "chart_file"
    LOG_FILE = "log_file"
    DATA_FILE = "data_file"


class ArtifactStatus(StrEnum):
    CREATED = "created"
    VALIDATED = "validated"
    INVALID = "invalid"
    ARCHIVED = "archived"


class ArtifactLinkTargetType(StrEnum):
    MESSAGE = "message"
    STRATEGY_VERSION = "strategy_version"
    BACKTEST_RUN = "backtest_run"
    BACKTEST_RESULT = "backtest_result"


class ArtifactLinkRelation(StrEnum):
    SOURCE = "source"
    USES = "uses"
    OUTPUT = "output"
    PREVIEW = "preview"


SCRIPT_ARTIFACT_TYPES = {
    ArtifactType.QUERY_SCRIPT,
    ArtifactType.ANALYSIS_SCRIPT,
    ArtifactType.STRATEGY_SCRIPT,
    ArtifactType.BACKTEST_SCRIPT,
}


@dataclass(slots=True)
class ArtifactFile:
    id: str
    artifact_id: str
    file_role: ArtifactFileRole
    relative_path: str
    storage_uri: str
    mime_type: str
    size_bytes: int
    checksum: str
    is_entrypoint: bool
    render_metadata_json: JsonObject = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(slots=True)
class ArtifactVersion:
    id: str
    artifact_id: str
    version: int
    root_path: str
    checksum: str
    entrypoint: str | None
    manifest_json: JsonObject
    created_by_sdk_tool_use_id: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(slots=True)
class ArtifactLink:
    id: str
    artifact_id: str
    target_type: ArtifactLinkTargetType
    target_id: str
    relation: ArtifactLinkRelation
    file_id: str | None = None
    metadata_json: JsonObject = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(slots=True)
class CodeArtifact:
    id: str
    user_id: str
    project_id: str
    chat_session_id: str
    artifact_type: ArtifactType
    title: str
    version: int
    root_path: str
    checksum: str
    status: ArtifactStatus = ArtifactStatus.CREATED
    description: str | None = None
    source_sdk_session_id: str | None = None
    source_sdk_message_uuid: str | None = None
    source_sdk_tool_use_id: str | None = None
    entrypoint: str | None = None
    main_file_id: str | None = None
    metadata_json: JsonObject = field(default_factory=dict)
    files: list[ArtifactFile] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
