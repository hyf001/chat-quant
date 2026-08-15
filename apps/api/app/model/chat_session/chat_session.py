from __future__ import annotations

from datetime import datetime

from sqlalchemy import JSON, DateTime, Index, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class ChatSessionRow(Base):
    __tablename__ = "chat_sessions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
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
    last_saved_at: Mapped[datetime | None] = mapped_column(DateTime)
    archived_at: Mapped[datetime | None] = mapped_column(DateTime)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    __table_args__ = (
        Index("idx_chat_sessions_project_updated", "project_id", "updated_at"),
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
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

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
