"""
Database models for financial strategies and backtest results.
"""

from sqlalchemy import String, DateTime, Text, JSON, Float, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.db.base import Base


class Strategy(Base):
    """Strategy definition model."""

    __tablename__ = "strategies"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    project_id: Mapped[str] = mapped_column(String(64), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)

    # Strategy details
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    strategy_type: Mapped[str] = mapped_column(String(64), nullable=False)  # sma, rsi, macd, bollinger, custom

    # Strategy parameters
    parameters: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

    # Strategy code (for custom strategies)
    code: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Status
    status: Mapped[str] = mapped_column(String(32), default="draft", nullable=False)  # draft, active, archived

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    backtest_results = relationship("BacktestResult", back_populates="strategy", cascade="all, delete-orphan")


class BacktestResult(Base):
    """Backtest result model."""

    __tablename__ = "backtest_results"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    strategy_id: Mapped[str] = mapped_column(String(64), ForeignKey("strategies.id", ondelete="CASCADE"), nullable=False, index=True)

    # Backtest configuration
    symbol: Mapped[str] = mapped_column(String(32), nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    initial_cash: Mapped[float] = mapped_column(Float, nullable=False)
    commission: Mapped[float] = mapped_column(Float, nullable=False)

    # Performance metrics
    final_value: Mapped[float] = mapped_column(Float, nullable=False)
    total_return: Mapped[float] = mapped_column(Float, nullable=False)
    return_pct: Mapped[float] = mapped_column(Float, nullable=False)
    sharpe_ratio: Mapped[float | None] = mapped_column(Float, nullable=True)
    max_drawdown: Mapped[float | None] = mapped_column(Float, nullable=True)
    max_drawdown_period: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Trading metrics
    total_trades: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    won_trades: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    lost_trades: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    win_rate: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    avg_win: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    avg_loss: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    # Additional metrics
    avg_return: Mapped[float | None] = mapped_column(Float, nullable=True)
    annual_return: Mapped[float | None] = mapped_column(Float, nullable=True)
    sqn: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Full results JSON
    detailed_results: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    # Status
    status: Mapped[str] = mapped_column(String(32), default="completed", nullable=False)  # running, completed, failed
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Relationships
    strategy = relationship("Strategy", back_populates="backtest_results")
