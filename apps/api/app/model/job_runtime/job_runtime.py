from __future__ import annotations

from datetime import datetime

from sqlalchemy import JSON, DateTime, Enum, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base

from .enums import InstanceStatus, TriggerType


def _enum_values(enum_cls: type) -> list[str]:
    return [item.value for item in enum_cls]


class JobSchedulerRow(Base):
    __tablename__ = "job_schedulers"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    job_type: Mapped[str] = mapped_column(String(64), nullable=False)
    job_id: Mapped[str] = mapped_column(String(128), nullable=False)
    cron: Mapped[str] = mapped_column(String(120), nullable=False)
    payload_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    last_run_at: Mapped[datetime | None] = mapped_column(DateTime)
    next_run_at: Mapped[datetime | None] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    __table_args__ = (
        UniqueConstraint("job_type", "job_id", name="uq_job_schedulers_job"),
        Index("idx_job_schedulers_job_type", "job_type"),
    )


class JobInstanceRow(Base):
    __tablename__ = "job_instances"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    job_type: Mapped[str] = mapped_column(String(64), nullable=False)
    job_id: Mapped[str] = mapped_column(String(128), nullable=False)
    trigger_type: Mapped[TriggerType] = mapped_column(
        Enum(TriggerType, values_callable=_enum_values, native_enum=False),
        nullable=False,
    )
    trigger_key: Mapped[str] = mapped_column(String(256), nullable=False)
    trigger_payload_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[InstanceStatus] = mapped_column(
        Enum(InstanceStatus, values_callable=_enum_values, native_enum=False),
        nullable=False,
    )
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    scheduled_for: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    started_at: Mapped[datetime | None] = mapped_column(DateTime)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime)
    result_status: Mapped[str | None] = mapped_column(String(64))
    summary: Mapped[str] = mapped_column(Text, nullable=False, default="")
    error_message: Mapped[str] = mapped_column(Text, nullable=False, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "job_type",
            "job_id",
            "trigger_key",
            name="uq_job_instances_trigger",
        ),
        Index("idx_job_instances_due", "status", "scheduled_for", "priority"),
        Index("idx_job_instances_job", "job_type", "job_id", "created_at"),
    )
