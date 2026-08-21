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

from app.db.session import Base


class StrategyRow(Base):
    __tablename__ = "strategies"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    project_id: Mapped[str] = mapped_column(String(128), nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    tags_json: Mapped[object] = mapped_column(JSON, nullable=False, default=list)
    current_version_id: Mapped[str | None] = mapped_column(String(64))
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    __table_args__ = (Index("idx_strategies_project_updated", "project_id", "updated_at"),)


class StrategyVersionRow(Base):
    __tablename__ = "strategy_versions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    strategy_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("strategies.id"),
        nullable=False,
    )
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    source_code: Mapped[str] = mapped_column(Text, nullable=False)
    strategy_mode: Mapped[str] = mapped_column(String(32), nullable=False)
    custom_params_json: Mapped[object] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    __table_args__ = (
        UniqueConstraint("strategy_id", "version", name="uq_strategy_versions_strategy_version"),
        Index("idx_strategy_versions_strategy", "strategy_id", "version"),
    )


class StrategyBacktestRow(Base):
    __tablename__ = "strategy_backtests"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    project_id: Mapped[str] = mapped_column(String(128), nullable=False)
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
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    result_id: Mapped[str | None] = mapped_column(String(64))
    started_at: Mapped[datetime | None] = mapped_column(DateTime)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    payload_json: Mapped[object] = mapped_column(JSON, nullable=False)

    __table_args__ = (
        Index("idx_strategy_backtests_version_created", "strategy_version_id", "created_at"),
        Index("idx_strategy_backtests_status", "status"),
    )


class StrategyDeploymentRow(Base):
    __tablename__ = "strategy_deployments"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    project_id: Mapped[str] = mapped_column(String(128), nullable=False)
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
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    mode: Mapped[str] = mapped_column(String(32), nullable=False)
    symbols_json: Mapped[object] = mapped_column(JSON, nullable=False, default=list)
    lookback_bars: Mapped[int] = mapped_column(Integer, nullable=False, default=250)
    params_json: Mapped[object] = mapped_column(JSON, nullable=False, default=dict)
    broker_id: Mapped[str | None] = mapped_column(String(128))
    requires_manual_confirm: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    risk_config_json: Mapped[object] = mapped_column(JSON, nullable=False, default=dict)
    state_json: Mapped[object] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    __table_args__ = (
        Index("idx_strategy_deployments_project_updated", "project_id", "updated_at"),
        Index("idx_strategy_deployments_strategy", "strategy_id", "strategy_version_id"),
        Index("idx_strategy_deployments_mode", "mode"),
    )


class StrategySignalRow(Base):
    __tablename__ = "strategy_signals"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    deployment_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("strategy_deployments.id"),
        nullable=False,
    )
    job_instance_id: Mapped[str | None] = mapped_column(
        String(64),
        ForeignKey("job_instances.id"),
    )
    strategy_version_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("strategy_versions.id"),
        nullable=False,
    )
    signal_datetime: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    action_json: Mapped[dict[str, object]] = mapped_column(JSON, nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    reason: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    __table_args__ = (
        Index("idx_strategy_signals_deployment_datetime", "deployment_id", "signal_datetime"),
        Index("idx_strategy_signals_job_instance", "job_instance_id"),
        Index("idx_strategy_signals_status", "status"),
    )
