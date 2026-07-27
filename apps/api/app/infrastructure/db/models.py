from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.session import Base


class ProjectRow(Base):
    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(128), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        Index("idx_projects_user_updated", "user_id", "updated_at"),
        Index("idx_projects_deleted", "deleted_at"),
    )


class ChatSessionRow(Base):
    __tablename__ = "chat_sessions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(128), nullable=False)
    project_id: Mapped[str] = mapped_column(String(128), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    kind: Mapped[str] = mapped_column(String(32), nullable=False)
    sdk_session_id: Mapped[str | None] = mapped_column(String(128))
    sdk_project_key: Mapped[str | None] = mapped_column(String(256))
    snippet: Mapped[str | None] = mapped_column(String(500))
    summary: Mapped[str | None] = mapped_column(Text)
    task_type: Mapped[str | None] = mapped_column(String(32))
    symbols: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    markets: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    tags: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    current_strategy_version_id: Mapped[str | None] = mapped_column(String(40))
    current_backtest_run_id: Mapped[str | None] = mapped_column(String(40))
    data_scope_label: Mapped[str | None] = mapped_column(String(120))
    last_saved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    archived_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        Index("idx_chat_sessions_user_updated", "user_id", "updated_at"),
        Index("idx_chat_sessions_sdk", "sdk_session_id"),
        Index("idx_chat_sessions_kind", "kind"),
    )


class ChatSessionAssetLinkRow(Base):
    __tablename__ = "chat_session_asset_links"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    chat_session_id: Mapped[str] = mapped_column(String(64), nullable=False)
    asset_type: Mapped[str] = mapped_column(String(40), nullable=False)
    asset_id: Mapped[str] = mapped_column(String(64), nullable=False)
    relation_type: Mapped[str] = mapped_column(String(40), nullable=False)
    sdk_session_id: Mapped[str | None] = mapped_column(String(128))
    sdk_message_uuid: Mapped[str | None] = mapped_column(String(128))
    sdk_tool_use_id: Mapped[str | None] = mapped_column(String(128))
    display_snapshot: Mapped[object | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "chat_session_id",
            "asset_type",
            "asset_id",
            "relation_type",
            name="uq_chat_session_asset_link",
        ),
        Index("idx_chat_session_asset_links_session", "chat_session_id", "created_at"),
        Index("idx_chat_session_asset_links_sdk_message", "sdk_session_id", "sdk_message_uuid"),
    )


class CodeArtifactRow(Base):
    __tablename__ = "code_artifacts"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(128), nullable=False)
    project_id: Mapped[str] = mapped_column(String(128), nullable=False)
    chat_session_id: Mapped[str] = mapped_column(String(64), nullable=False)
    source_sdk_session_id: Mapped[str | None] = mapped_column(String(128))
    source_sdk_message_uuid: Mapped[str | None] = mapped_column(String(128))
    source_sdk_tool_use_id: Mapped[str | None] = mapped_column(String(128))
    artifact_type: Mapped[str] = mapped_column(String(40), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    entrypoint: Mapped[str | None] = mapped_column(String(256))
    root_path: Mapped[str] = mapped_column(String(512), nullable=False)
    main_file_id: Mapped[str | None] = mapped_column(String(64))
    checksum: Mapped[str] = mapped_column(String(128), nullable=False)
    metadata_json: Mapped[object] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="created")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        Index("idx_code_artifacts_chat_created", "chat_session_id", "created_at"),
        Index("idx_code_artifacts_sdk_tool_use", "source_sdk_tool_use_id"),
        Index("idx_code_artifacts_type", "artifact_type"),
        UniqueConstraint(
            "source_sdk_tool_use_id",
            "artifact_type",
            "checksum",
            "entrypoint",
            name="uq_code_artifacts_idempotent",
        ),
    )


class ArtifactFileRow(Base):
    __tablename__ = "artifact_files"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    artifact_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("code_artifacts.id"),
        nullable=False,
    )
    file_role: Mapped[str] = mapped_column(String(40), nullable=False)
    relative_path: Mapped[str] = mapped_column(String(512), nullable=False)
    storage_uri: Mapped[str] = mapped_column(String(1024), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(128), nullable=False)
    size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    checksum: Mapped[str] = mapped_column(String(128), nullable=False)
    is_entrypoint: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    render_metadata_json: Mapped[object] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        Index("idx_artifact_files_artifact", "artifact_id"),
        Index("idx_artifact_files_role", "file_role"),
        UniqueConstraint("artifact_id", "relative_path", name="uq_artifact_files_path"),
    )


class ArtifactVersionRow(Base):
    __tablename__ = "artifact_versions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    artifact_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("code_artifacts.id"),
        nullable=False,
    )
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    root_path: Mapped[str] = mapped_column(String(512), nullable=False)
    checksum: Mapped[str] = mapped_column(String(128), nullable=False)
    entrypoint: Mapped[str | None] = mapped_column(String(256))
    manifest_json: Mapped[object] = mapped_column(JSON, nullable=False, default=dict)
    created_by_sdk_tool_use_id: Mapped[str | None] = mapped_column(String(128))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        UniqueConstraint("artifact_id", "version", name="uq_artifact_versions_version"),
        UniqueConstraint(
            "artifact_id",
            "checksum",
            "entrypoint",
            name="uq_artifact_versions_checksum",
        ),
    )


class ArtifactLinkRow(Base):
    __tablename__ = "artifact_links"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    artifact_id: Mapped[str] = mapped_column(String(64), nullable=False)
    file_id: Mapped[str | None] = mapped_column(String(64))
    target_type: Mapped[str] = mapped_column(String(40), nullable=False)
    target_id: Mapped[str] = mapped_column(String(128), nullable=False)
    relation: Mapped[str] = mapped_column(String(40), nullable=False)
    metadata_json: Mapped[object] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        Index("idx_artifact_links_target", "target_type", "target_id"),
        Index("idx_artifact_links_artifact", "artifact_id"),
    )


class StrategyRow(Base):
    __tablename__ = "strategies"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(128), nullable=False)
    project_id: Mapped[str] = mapped_column(String(128), nullable=False)
    chat_session_id: Mapped[str] = mapped_column(String(64), nullable=False)
    source_sdk_message_uuid: Mapped[str | None] = mapped_column(String(128))
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    strategy_type: Mapped[str] = mapped_column(String(64), nullable=False)
    tags_json: Mapped[object] = mapped_column(JSON, nullable=False, default=list)
    current_version_id: Mapped[str | None] = mapped_column(String(64))
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    payload_json: Mapped[object] = mapped_column(JSON, nullable=False)

    __table_args__ = (
        Index("idx_strategies_user_project_updated", "user_id", "project_id", "updated_at"),
        Index("idx_strategies_chat_session", "chat_session_id"),
        Index("idx_strategies_type", "strategy_type"),
    )


class StrategyVersionRow(Base):
    __tablename__ = "strategy_versions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    strategy_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("strategies.id"),
        nullable=False,
    )
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    version_name: Mapped[str | None] = mapped_column(String(128))
    parent_version_id: Mapped[str | None] = mapped_column(String(64))
    code_artifact_id: Mapped[str] = mapped_column(String(128), nullable=False)
    entrypoint: Mapped[str] = mapped_column(String(256), nullable=False)
    params_schema_json: Mapped[object] = mapped_column(JSON, nullable=False)
    default_params_json: Mapped[object] = mapped_column(JSON, nullable=False)
    logic_summary: Mapped[str | None] = mapped_column(Text)
    change_summary: Mapped[str | None] = mapped_column(Text)
    source_sdk_session_id: Mapped[str | None] = mapped_column(String(128))
    source_sdk_message_uuid: Mapped[str | None] = mapped_column(String(128))
    source_sdk_tool_use_id: Mapped[str | None] = mapped_column(String(128))
    code_checksum: Mapped[str] = mapped_column(String(128), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    payload_json: Mapped[object] = mapped_column(JSON, nullable=False)

    __table_args__ = (
        UniqueConstraint("strategy_id", "version", name="uq_strategy_versions_strategy_version"),
        Index("idx_strategy_versions_strategy", "strategy_id", "version"),
        Index("idx_strategy_versions_parent", "parent_version_id"),
        Index("idx_strategy_versions_artifact", "code_artifact_id"),
        Index("idx_strategy_versions_status", "status"),
    )


class StrategyBacktestRow(Base):
    __tablename__ = "strategy_backtests"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(128), nullable=False)
    project_id: Mapped[str] = mapped_column(String(128), nullable=False)
    chat_session_id: Mapped[str] = mapped_column(String(64), nullable=False)
    strategy_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("strategies.id"),
        nullable=False,
    )
    strategy_version_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("strategy_versions.id"),
        nullable=False,
    )
    run_type: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    config_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    result_id: Mapped[str | None] = mapped_column(String(64))
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    payload_json: Mapped[object] = mapped_column(JSON, nullable=False)

    __table_args__ = (
        Index("idx_strategy_backtests_version_created", "strategy_version_id", "created_at"),
        Index("idx_strategy_backtests_status", "status"),
    )


class StrategyBacktestResultRow(Base):
    __tablename__ = "strategy_backtest_results"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    strategy_backtest_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("strategy_backtests.id"),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    payload_json: Mapped[object] = mapped_column(JSON, nullable=False)

    __table_args__ = (
        UniqueConstraint("strategy_backtest_id", name="uq_strategy_backtest_results_run"),
    )
