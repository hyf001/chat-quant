"""
Pydantic schemas for financial API.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


# Strategy schemas
class StrategyBase(BaseModel):
    name: str = Field(..., description="Strategy name")
    description: Optional[str] = Field(None, description="Strategy description")
    strategy_type: str = Field(..., description="Strategy type (sma, rsi, macd, bollinger, custom)")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Strategy parameters")
    code: Optional[str] = Field(None, description="Custom strategy code")


class StrategyCreate(StrategyBase):
    project_id: str = Field(..., description="Project ID")


class StrategyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    code: Optional[str] = None
    status: Optional[str] = None


class StrategyResponse(StrategyBase):
    id: str
    project_id: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Backtest schemas
class BacktestConfig(BaseModel):
    strategy_id: str = Field(..., description="Strategy ID")
    symbol: str = Field(..., description="Trading symbol")
    start_date: datetime = Field(..., description="Backtest start date")
    end_date: datetime = Field(..., description="Backtest end date")
    initial_cash: float = Field(10000.0, description="Initial cash")
    commission: float = Field(0.001, description="Commission rate")
    data_source: str = Field("csv", description="Data source (csv, json, yahoo)")
    data_path: Optional[str] = Field(None, description="Path to data file")


class BacktestResultResponse(BaseModel):
    id: str
    strategy_id: str
    symbol: str
    start_date: datetime
    end_date: datetime
    initial_cash: float
    commission: float

    # Performance metrics
    final_value: float
    total_return: float
    return_pct: float
    sharpe_ratio: Optional[float]
    max_drawdown: Optional[float]
    max_drawdown_period: Optional[int]

    # Trading metrics
    total_trades: int
    won_trades: int
    lost_trades: int
    win_rate: float
    avg_win: float
    avg_loss: float

    # Additional metrics
    avg_return: Optional[float]
    annual_return: Optional[float]
    sqn: Optional[float]

    detailed_results: Optional[Dict[str, Any]]
    status: str
    error_message: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True


# List responses
class StrategyListResponse(BaseModel):
    strategies: List[StrategyResponse]
    total: int


class BacktestListResponse(BaseModel):
    results: List[BacktestResultResponse]
    total: int


# Optimization schemas
class OptimizationConfig(BaseModel):
    strategy_id: str = Field(..., description="Strategy ID")
    symbol: str = Field(..., description="Trading symbol")
    start_date: datetime = Field(..., description="Optimization start date")
    end_date: datetime = Field(..., description="Optimization end date")
    param_ranges: Dict[str, tuple] = Field(..., description="Parameter ranges for optimization")
    optimization_metric: str = Field("sharpe_ratio", description="Metric to optimize")
    initial_cash: float = Field(10000.0, description="Initial cash")
    commission: float = Field(0.001, description="Commission rate")
    data_source: str = Field("csv", description="Data source")
    data_path: Optional[str] = Field(None, description="Path to data file")


class OptimizationResultResponse(BaseModel):
    best_params: Dict[str, Any]
    metric_value: float
    final_value: float


# Data generation schemas
class DataGenerationConfig(BaseModel):
    start_date: datetime
    end_date: datetime
    initial_price: float = 100.0
    volatility: float = 0.02


# Available strategies list
class AvailableStrategy(BaseModel):
    name: str
    display_name: str
    description: str
    default_params: Dict[str, Any]


class AvailableStrategiesResponse(BaseModel):
    strategies: List[AvailableStrategy]
