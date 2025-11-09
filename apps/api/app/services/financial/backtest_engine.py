"""
Backtesting engine using backtrader framework.
"""

from typing import Dict, Any, Optional, List
import backtrader as bt
from datetime import datetime
import pandas as pd
import json


class BacktestEngine:
    """Engine for running backtests with various configurations."""

    def __init__(
        self,
        initial_cash: float = 10000.0,
        commission: float = 0.001,
        slippage: Optional[float] = None
    ):
        self.initial_cash = initial_cash
        self.commission = commission
        self.slippage = slippage
        self.cerebro = None
        self.results = None

    def setup_cerebro(self):
        """Initialize cerebro with configurations."""
        self.cerebro = bt.Cerebro()

        # Set initial cash
        self.cerebro.broker.setcash(self.initial_cash)

        # Set commission
        self.cerebro.broker.setcommission(commission=self.commission)

        # Add analyzers
        self.cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
        self.cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
        self.cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')
        self.cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')
        self.cerebro.addanalyzer(bt.analyzers.SQN, _name='sqn')

        # Add observers
        self.cerebro.addobserver(bt.observers.Broker)
        self.cerebro.addobserver(bt.observers.Trades)
        self.cerebro.addobserver(bt.observers.BuySell)

    def add_data(
        self,
        data: pd.DataFrame,
        name: str = 'data',
        fromdate: Optional[datetime] = None,
        todate: Optional[datetime] = None
    ):
        """Add data feed to cerebro."""
        if self.cerebro is None:
            self.setup_cerebro()

        # Convert pandas dataframe to backtrader data feed
        data_feed = bt.feeds.PandasData(
            dataname=data,
            fromdate=fromdate,
            todate=todate,
            datetime=None,  # Use index as datetime
            open='open',
            high='high',
            low='low',
            close='close',
            volume='volume',
            openinterest=-1
        )

        self.cerebro.adddata(data_feed, name=name)

    def add_strategy(
        self,
        strategy_class: type,
        **params
    ):
        """Add strategy to cerebro."""
        if self.cerebro is None:
            self.setup_cerebro()

        self.cerebro.addstrategy(strategy_class, **params)

    def run(self) -> Dict[str, Any]:
        """Run the backtest and return results."""
        if self.cerebro is None:
            raise ValueError("Cerebro not initialized. Call setup_cerebro() first.")

        print(f'Starting Portfolio Value: {self.cerebro.broker.getvalue():.2f}')

        # Run backtest
        strategies = self.cerebro.run()
        strategy = strategies[0]

        print(f'Final Portfolio Value: {self.cerebro.broker.getvalue():.2f}')

        # Extract analyzer results
        results = self._extract_results(strategy)

        self.results = results
        return results

    def _extract_results(self, strategy) -> Dict[str, Any]:
        """Extract results from analyzers."""
        results = {
            'initial_value': self.initial_cash,
            'final_value': self.cerebro.broker.getvalue(),
            'total_return': self.cerebro.broker.getvalue() - self.initial_cash,
            'return_pct': ((self.cerebro.broker.getvalue() - self.initial_cash) / self.initial_cash) * 100,
        }

        # Sharpe Ratio
        sharpe_analysis = strategy.analyzers.sharpe.get_analysis()
        results['sharpe_ratio'] = sharpe_analysis.get('sharperatio', None)

        # Drawdown
        drawdown_analysis = strategy.analyzers.drawdown.get_analysis()
        results['max_drawdown'] = drawdown_analysis.get('max', {}).get('drawdown', 0)
        results['max_drawdown_period'] = drawdown_analysis.get('max', {}).get('len', 0)

        # Returns
        returns_analysis = strategy.analyzers.returns.get_analysis()
        results['avg_return'] = returns_analysis.get('ravg', 0)
        results['annual_return'] = returns_analysis.get('rnorm', 0)

        # Trades
        trades_analysis = strategy.analyzers.trades.get_analysis()
        results['total_trades'] = trades_analysis.get('total', {}).get('total', 0)
        results['won_trades'] = trades_analysis.get('won', {}).get('total', 0)
        results['lost_trades'] = trades_analysis.get('lost', {}).get('total', 0)

        if results['total_trades'] > 0:
            results['win_rate'] = (results['won_trades'] / results['total_trades']) * 100
        else:
            results['win_rate'] = 0

        # Average PnL
        if results['won_trades'] > 0:
            results['avg_win'] = trades_analysis.get('won', {}).get('pnl', {}).get('average', 0)
        else:
            results['avg_win'] = 0

        if results['lost_trades'] > 0:
            results['avg_loss'] = trades_analysis.get('lost', {}).get('pnl', {}).get('average', 0)
        else:
            results['avg_loss'] = 0

        # SQN (System Quality Number)
        sqn_analysis = strategy.analyzers.sqn.get_analysis()
        results['sqn'] = sqn_analysis.get('sqn', 0)

        return results

    def reset(self):
        """Reset the engine for a new backtest."""
        self.cerebro = None
        self.results = None


class OptimizationEngine:
    """Engine for optimizing strategy parameters."""

    def __init__(
        self,
        initial_cash: float = 10000.0,
        commission: float = 0.001
    ):
        self.initial_cash = initial_cash
        self.commission = commission

    def optimize(
        self,
        data: pd.DataFrame,
        strategy_class: type,
        param_ranges: Dict[str, tuple],
        optimization_metric: str = 'sharpe_ratio'
    ) -> Dict[str, Any]:
        """
        Optimize strategy parameters.

        Args:
            data: Historical data
            strategy_class: Strategy class to optimize
            param_ranges: Dictionary of parameter names and their ranges (min, max, step)
            optimization_metric: Metric to optimize ('sharpe_ratio', 'return_pct', etc.)

        Returns:
            Dictionary with best parameters and results
        """
        cerebro = bt.Cerebro(optreturn=True)

        # Set initial cash and commission
        cerebro.broker.setcash(self.initial_cash)
        cerebro.broker.setcommission(commission=self.commission)

        # Add data
        data_feed = bt.feeds.PandasData(
            dataname=data,
            datetime=None,
            open='open',
            high='high',
            low='low',
            close='close',
            volume='volume',
            openinterest=-1
        )
        cerebro.adddata(data_feed)

        # Add analyzers
        cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
        cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')
        cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')

        # Optimize strategy
        opt_runs = cerebro.optstrategy(strategy_class, **param_ranges)

        # Run optimization
        print("Running optimization...")
        results = cerebro.run()

        # Find best result
        best_result = None
        best_metric_value = float('-inf')

        for run in results:
            for strategy in run:
                # Get metric value
                if optimization_metric == 'sharpe_ratio':
                    metric_value = strategy.analyzers.sharpe.get_analysis().get('sharperatio', 0) or 0
                elif optimization_metric == 'return_pct':
                    final_value = cerebro.broker.getvalue()
                    metric_value = ((final_value - self.initial_cash) / self.initial_cash) * 100
                else:
                    metric_value = 0

                if metric_value > best_metric_value:
                    best_metric_value = metric_value
                    best_result = {
                        'params': strategy.params.__dict__,
                        'metric_value': metric_value,
                        'final_value': cerebro.broker.getvalue()
                    }

        return best_result or {}
