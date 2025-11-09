"""
Strategy implementations using backtrader framework.
"""

from typing import Dict, Any, Type, Optional
import backtrader as bt
from datetime import datetime


class BaseStrategy(bt.Strategy):
    """Base strategy class with common functionality."""

    params = (
        ('printlog', False),
        ('stake', 100),
    )

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.bar_executed = None

    def log(self, txt, dt=None):
        """Logging function for strategy."""
        if self.params.printlog:
            dt = dt or self.datas[0].datetime.date(0)
            print(f'{dt.isoformat()} {txt}')

    def notify_order(self, order):
        """Notify when an order is executed."""
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    f'BUY EXECUTED, Price: {order.executed.price:.2f}, '
                    f'Cost: {order.executed.value:.2f}, '
                    f'Comm: {order.executed.comm:.2f}'
                )
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
                self.log(
                    f'SELL EXECUTED, Price: {order.executed.price:.2f}, '
                    f'Cost: {order.executed.value:.2f}, '
                    f'Comm: {order.executed.comm:.2f}'
                )

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        """Notify when a trade is closed."""
        if not trade.isclosed:
            return

        self.log(f'OPERATION PROFIT, GROSS {trade.pnl:.2f}, NET {trade.pnlcomm:.2f}')


class SMAStrategy(BaseStrategy):
    """Simple Moving Average Crossover Strategy."""

    params = (
        ('fast_period', 10),
        ('slow_period', 30),
        ('printlog', False),
        ('stake', 100),
    )

    def __init__(self):
        super().__init__()

        # Create moving averages
        self.sma_fast = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.fast_period
        )
        self.sma_slow = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.slow_period
        )

        # Create crossover signal
        self.crossover = bt.indicators.CrossOver(self.sma_fast, self.sma_slow)

    def next(self):
        """Execute strategy logic on each bar."""
        if self.order:
            return

        # Check if we are in the market
        if not self.position:
            # Not in market, check if fast SMA crosses above slow SMA
            if self.crossover > 0:
                self.log(f'BUY CREATE, {self.dataclose[0]:.2f}')
                self.order = self.buy(size=self.params.stake)
        else:
            # In market, check if fast SMA crosses below slow SMA
            if self.crossover < 0:
                self.log(f'SELL CREATE, {self.dataclose[0]:.2f}')
                self.order = self.sell(size=self.params.stake)


class MACDStrategy(BaseStrategy):
    """MACD-based strategy."""

    params = (
        ('fast_ema', 12),
        ('slow_ema', 26),
        ('signal', 9),
        ('printlog', False),
        ('stake', 100),
    )

    def __init__(self):
        super().__init__()

        # Create MACD indicator
        self.macd = bt.indicators.MACD(
            self.datas[0],
            period_me1=self.params.fast_ema,
            period_me2=self.params.slow_ema,
            period_signal=self.params.signal
        )

        # Crossover between MACD and signal line
        self.crossover = bt.indicators.CrossOver(self.macd.macd, self.macd.signal)

    def next(self):
        """Execute strategy logic on each bar."""
        if self.order:
            return

        # Check if we are in the market
        if not self.position:
            # Buy when MACD crosses above signal line
            if self.crossover > 0:
                self.log(f'BUY CREATE, {self.dataclose[0]:.2f}')
                self.order = self.buy(size=self.params.stake)
        else:
            # Sell when MACD crosses below signal line
            if self.crossover < 0:
                self.log(f'SELL CREATE, {self.dataclose[0]:.2f}')
                self.order = self.sell(size=self.params.stake)


class BollingerBandsStrategy(BaseStrategy):
    """Bollinger Bands mean reversion strategy."""

    params = (
        ('period', 20),
        ('devfactor', 2.0),
        ('printlog', False),
        ('stake', 100),
    )

    def __init__(self):
        super().__init__()

        # Create Bollinger Bands indicator
        self.bbands = bt.indicators.BollingerBands(
            self.datas[0],
            period=self.params.period,
            devfactor=self.params.devfactor
        )

    def next(self):
        """Execute strategy logic on each bar."""
        if self.order:
            return

        # Check if we are in the market
        if not self.position:
            # Buy when price touches lower band
            if self.dataclose[0] < self.bbands.lines.bot[0]:
                self.log(f'BUY CREATE, {self.dataclose[0]:.2f}')
                self.order = self.buy(size=self.params.stake)
        else:
            # Sell when price touches upper band
            if self.dataclose[0] > self.bbands.lines.top[0]:
                self.log(f'SELL CREATE, {self.dataclose[0]:.2f}')
                self.order = self.sell(size=self.params.stake)