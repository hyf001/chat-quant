from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import JSON, Date, DateTime, Index, Integer, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class TrainingSessionRow(Base):
    """训练会话；symbol / 日期按普通列存，脱敏只在 API 出口做。"""

    __tablename__ = "training_sessions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    project_id: Mapped[str] = mapped_column(String(128), nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    period: Mapped[str] = mapped_column(String(8), nullable=False)
    symbol: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str | None] = mapped_column(String(128))
    slice_start: Mapped[date] = mapped_column(Date, nullable=False)
    slice_end: Mapped[date] = mapped_column(Date, nullable=False)
    warmup_bars: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False)
    initial_cash: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    config_json: Mapped[object] = mapped_column(JSON, nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    __table_args__ = (
        Index("idx_training_sessions_project", "project_id", "created_at"),
        Index("idx_training_sessions_status", "status"),
    )


class TrainingEventRow(Base):
    """人工信号历史：每行 = 一次点击 = 一根推进（顺序看 seq，不看时间）。"""

    __tablename__ = "training_events"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    session_id: Mapped[str] = mapped_column(String(64), nullable=False)
    seq: Mapped[int] = mapped_column(Integer, nullable=False)
    event_type: Mapped[str] = mapped_column(String(32), nullable=False)
    payload_json: Mapped[object | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    __table_args__ = (
        UniqueConstraint("session_id", "seq", name="uq_training_events_session_seq"),
        Index("idx_training_events_session", "session_id", "seq"),
    )
