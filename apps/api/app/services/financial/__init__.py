"""
Financial services module for strategy creation and backtesting.
Uses backtrader framework for backtesting.
"""

from .strategies import BaseStrategy, StrategyFactory
from .backtest_engine import BacktestEngine
from .data_manager import DataManager

__all__ = [
    'BaseStrategy',
    'StrategyFactory',
    'BacktestEngine',
    'DataManager',
]
