#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Backtest Execution Script
Based on backtrader framework for quantitative trading strategy backtesting

Usage:
    python run_backtest.py --strategy strategy_file.py --cash 100000 --commission 0.001
"""

import argparse
import sys
import os
import importlib.util
import json
from datetime import datetime
from typing import Type, Dict, Any, Optional
from pathlib import Path
import backtrader as bt
import pandas as pd


class TradeDetailAnalyzer(bt.Analyzer):
    """交易详情分析器 - 记录每笔交易的详细信息"""

    def __init__(self):
        super().__init__()
        self.trades = []

    def notify_trade(self, trade):
        """当交易发生时被调用"""
        if trade.isclosed:
            # 交易已关闭，记录详细信息
            trade_info = {
                'entry_date': bt.num2date(trade.dtopen).isoformat() if trade.dtopen else None,
                'exit_date': bt.num2date(trade.dtclose).isoformat() if trade.dtclose else None,
                'entry_price': float(trade.price),
                'exit_price': float(trade.price + (trade.pnl / trade.size)) if trade.size != 0 else 0.0,
                'size': float(trade.size),
                'value': float(trade.value),
                'pnl_gross': float(trade.pnl),
                'pnl_net': float(trade.pnlcomm),
                'commission': float(trade.commission),
                'duration_bars': int(trade.barlen) if trade.barlen else 0,
                'direction': 'LONG' if trade.size > 0 else 'SHORT'
            }
            self.trades.append(trade_info)

    def get_analysis(self):
        """返回分析结果"""
        return {
            'trades': self.trades,
            'total_count': len(self.trades)
        }


class DailyRecordAnalyzer(bt.Analyzer):
    """每日记录分析器 - 记录每日行情和账户状态，以及所有订单"""

    def __init__(self):
        super().__init__()
        self.daily_records = []
        self.order_records = []
        self.kline_data = []

    def notify_order(self, order):
        """订单状态通知"""
        if order.status in [order.Completed]:
            # 记录所有成交的订单
            order_info = {
                'date': bt.num2date(order.executed.dt).isoformat() if order.executed.dt else None,
                'type': 'BUY' if order.isbuy() else 'SELL',
                'price': float(order.executed.price),
                'size': float(order.executed.size),
                'value': float(order.executed.value),
                'commission': float(order.executed.comm),
                'cost': float(order.executed.value + order.executed.comm)
            }
            self.order_records.append(order_info)

    def next(self):
        """每个交易日调用"""
        dt = self.datas[0].datetime.date(0)

        # 记录K线数据
        kline_info = {
            'date': dt.isoformat(),
            'open': float(self.datas[0].open[0]),
            'high': float(self.datas[0].high[0]),
            'low': float(self.datas[0].low[0]),
            'close': float(self.datas[0].close[0]),
            'volume': float(self.datas[0].volume[0])
        }
        self.kline_data.append(kline_info)

        # 记录账户状态
        daily_info = {
            'date': dt.isoformat(),
            'close': float(self.datas[0].close[0]),
            'value': float(self.strategy.broker.getvalue()),
            'cash': float(self.strategy.broker.getcash()),
            'position_value': float(self.strategy.broker.getvalue() - self.strategy.broker.getcash()),
            'position_size': float(self.strategy.position.size) if self.strategy.position else 0.0
        }
        self.daily_records.append(daily_info)

    def get_analysis(self):
        """返回分析结果"""
        return {
            'kline_data': self.kline_data,
            'daily_records': self.daily_records,
            'order_records': self.order_records
        }


class BacktestRunner:
    """Backtest Runner"""

    def __init__(
        self,
        strategy_class: Type[bt.Strategy],
        cash: float = 100000.0,
        commission: float = 0.0005,
        slippage: float = 0.0,
        strategy_params: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize Backtest Runner

        Args:
            strategy_class: backtrader Strategy class
            cash: Initial capital, default 100000
            commission: Commission rate, default 0.001 (0.1%)
            slippage: Slippage, default 0
            strategy_params: Strategy parameters dict
        """
        self.strategy_class = strategy_class
        self.cash = cash
        self.commission = commission
        self.slippage = slippage
        self.strategy_params = strategy_params or {}
        self.cerebro = None
        self.results = None

    def setup_cerebro(self):
        """Setup cerebro engine"""
        self.cerebro = bt.Cerebro()

        # Add strategy
        self.cerebro.addstrategy(self.strategy_class, **self.strategy_params)

        # Set initial capital
        self.cerebro.broker.setcash(self.cash)

        # Set commission
        self.cerebro.broker.setcommission(commission=self.commission)

        # Set slippage (if needed)
        if self.slippage > 0:
            self.cerebro.broker.set_slippage_perc(self.slippage)

        # Add analyzers
        self.cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe', riskfreerate=0.03)
        self.cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
        self.cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')
        self.cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')
        self.cerebro.addanalyzer(bt.analyzers.TimeReturn, _name='timereturn')
        self.cerebro.addanalyzer(TradeDetailAnalyzer, _name='trade_details')
        self.cerebro.addanalyzer(DailyRecordAnalyzer, _name='daily_records')

        # Add observers
        self.cerebro.addobserver(bt.observers.Value)
        self.cerebro.addobserver(bt.observers.DrawDown)
        self.cerebro.addobserver(bt.observers.Trades)

    

    def run(self) -> Dict[str, Any]:
        """
        Execute backtest

        Returns:
            Backtest results dict
        """
        if self.cerebro is None:
            raise RuntimeError("Please call setup_cerebro() first to initialize engine")

        # Record initial capital
        start_value = self.cerebro.broker.getvalue()
        print(f'\n{"="*60}')
        print(f'{"Backtest Started":^60}')
        print(f'{"="*60}')
        print(f'Initial Capital: {start_value:,.2f}')

        # Run backtest
        self.results = self.cerebro.run()

        # Check if we have results
        if not self.results or len(self.results) == 0:
            raise RuntimeError("Backtest returned no results. Please check if data was loaded properly.")

        # Get final capital
        end_value = self.cerebro.broker.getvalue()

        # Extract analysis results
        strategy_result = self.results[0]

        # Calculate basic metrics
        total_return = end_value - start_value
        total_return_pct = (end_value / start_value - 1) * 100

        # Get analyzer results
        sharpe_ratio = self._get_sharpe_ratio(strategy_result)
        max_drawdown = self._get_max_drawdown(strategy_result)
        returns_analysis = self._get_returns_analysis(strategy_result)
        trade_analysis = self._get_trade_analysis(strategy_result)
        trade_details = self._get_trade_details(strategy_result)
        daily_data = self._get_daily_records(strategy_result)

        # Assemble results
        results = {
            'start_value': start_value,
            'end_value': end_value,
            'total_return': total_return,
            'total_return_pct': total_return_pct,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'returns': returns_analysis,
            'trades': trade_analysis,
            'trade_details': trade_details,
            'kline_data': daily_data.get('kline_data', []),
            'daily_records': daily_data.get('daily_records', []),
            'order_records': daily_data.get('order_records', [])
        }

        # Print results
        self._print_results(results)

        # Save results to JSON
        self._save_results_to_json(results)

        return results

    def _get_sharpe_ratio(self, strategy_result) -> Optional[float]:
        """Get Sharpe Ratio"""
        try:
            sharpe = strategy_result.analyzers.sharpe.get_analysis()
            return sharpe.get('sharperatio', None)
        except:
            return None

    def _get_max_drawdown(self, strategy_result) -> Dict[str, Any]:
        """Get Maximum Drawdown"""
        try:
            drawdown = strategy_result.analyzers.drawdown.get_analysis()
            return {
                'max': drawdown.get('max', {}).get('drawdown', 0),
                'len': drawdown.get('max', {}).get('len', 0),
                'money': drawdown.get('max', {}).get('moneydown', 0)
            }
        except:
            return {'max': 0, 'len': 0, 'money': 0}

    def _get_returns_analysis(self, strategy_result) -> Dict[str, Any]:
        """Get Returns Analysis"""
        try:
            returns = strategy_result.analyzers.returns.get_analysis()
            return {
                'rtot': returns.get('rtot', 0),
                'ravg': returns.get('ravg', 0),
                'rnorm': returns.get('rnorm', 0),
                'rnorm100': returns.get('rnorm100', 0)
            }
        except:
            return {'rtot': 0, 'ravg': 0, 'rnorm': 0, 'rnorm100': 0}

    def _get_trade_analysis(self, strategy_result) -> Dict[str, Any]:
        """Get Trade Analysis"""
        try:
            trades = strategy_result.analyzers.trades.get_analysis()
            total_trades = trades.get('total', {}).get('total', 0)
            won_trades = trades.get('won', {}).get('total', 0)
            lost_trades = trades.get('lost', {}).get('total', 0)

            win_rate = (won_trades / total_trades * 100) if total_trades > 0 else 0

            return {
                'total': total_trades,
                'won': won_trades,
                'lost': lost_trades,
                'win_rate': win_rate,
                'pnl': {
                    'gross': trades.get('pnl', {}).get('gross', {}).get('total', 0),
                    'net': trades.get('pnl', {}).get('net', {}).get('total', 0),
                    'average': trades.get('pnl', {}).get('net', {}).get('average', 0)
                }
            }
        except:
            return {
                'total': 0,
                'won': 0,
                'lost': 0,
                'win_rate': 0,
                'pnl': {'gross': 0, 'net': 0, 'average': 0}
            }

    def _get_trade_details(self, strategy_result) -> Dict[str, Any]:
        """Get Trade Details"""
        try:
            trade_details = strategy_result.analyzers.trade_details.get_analysis()
            return {
                'trades': trade_details.get('trades', []),
                'total_count': trade_details.get('total_count', 0)
            }
        except:
            return {'trades': [], 'total_count': 0}

    def _get_daily_records(self, strategy_result) -> Dict[str, Any]:
        """Get Daily Records (K-line, account status, orders)"""
        try:
            daily_data = strategy_result.analyzers.daily_records.get_analysis()
            return {
                'kline_data': daily_data.get('kline_data', []),
                'daily_records': daily_data.get('daily_records', []),
                'order_records': daily_data.get('order_records', [])
            }
        except:
            return {
                'kline_data': [],
                'daily_records': [],
                'order_records': []
            }

    def _print_results(self, results: Dict[str, Any]):
        """Print backtest results"""
        print(f'\n{"="*60}')
        print(f'{"Backtest Results":^60}')
        print(f'{"="*60}')

        # Capital Info
        print(f'\n[Capital Info]')
        print(f'  Initial Capital: {results["start_value"]:,.2f}')
        print(f'  Final Capital: {results["end_value"]:,.2f}')
        print(f'  Total Return: {results["total_return"]:,.2f}')
        print(f'  Total Return %: {results["total_return_pct"]:.2f}%')

        # Risk Metrics
        print(f'\n[Risk Metrics]')
        if results['sharpe_ratio'] is not None:
            print(f'  Sharpe Ratio: {results["sharpe_ratio"]:.4f}')
        else:
            print(f'  Sharpe Ratio: N/A')

        drawdown = results['max_drawdown']
        print(f'  Max Drawdown: {drawdown["max"]:.2f}%')
        print(f'  Max Drawdown Period: {drawdown["len"]} days')
        print(f'  Max Drawdown Amount: {drawdown["money"]:,.2f}')

        # Trade Statistics
        print(f'\n[Trade Statistics]')
        trades = results['trades']
        print(f'  Total Trades: {trades["total"]}')
        print(f'  Winning Trades: {trades["won"]}')
        print(f'  Losing Trades: {trades["lost"]}')
        print(f'  Win Rate: {trades["win_rate"]:.2f}%')
        print(f'  Total PnL (Net): {trades["pnl"]["net"]:,.2f}')
        print(f'  Average PnL: {trades["pnl"]["average"]:,.2f}')

        # Order Records (买卖点)
        order_records = results.get('order_records', [])
        if len(order_records) > 0:
            print(f'\n[Order Records - 买卖点]')
            print(f'  Total Orders: {len(order_records)}')
            for i, order in enumerate(order_records[:10], 1):  # Show first 10 orders
                print(f'\n  Order #{i}:')
                print(f'    Date: {order["date"]}')
                print(f'    Type: {order["type"]}')
                print(f'    Price: ¥{order["price"]:.2f}')
                print(f'    Size: {order["size"]:.0f}')
                print(f'    Cost: ¥{order["cost"]:.2f} (including commission: ¥{order["commission"]:.2f})')
            if len(order_records) > 10:
                print(f'\n  ... and {len(order_records) - 10} more orders')

        # Trade Details (已平仓交易)
        trade_details = results.get('trade_details', {})
        if trade_details.get('total_count', 0) > 0:
            print(f'\n[Closed Trades]')
            print(f'  Total Closed Trades: {trade_details["total_count"]}')
            for i, trade in enumerate(trade_details['trades'][:10], 1):  # Show first 10 trades
                print(f'\n  Trade #{i}:')
                print(f'    Entry: {trade["entry_date"]} @ ¥{trade["entry_price"]:.2f}')
                print(f'    Exit:  {trade["exit_date"]} @ ¥{trade["exit_price"]:.2f}')
                print(f'    Size: {trade["size"]:.0f} | Direction: {trade["direction"]}')
                print(f'    PnL: ¥{trade["pnl_net"]:.2f} (Net) | Duration: {trade["duration_bars"]} bars')
            if trade_details["total_count"] > 10:
                print(f'\n  ... and {trade_details["total_count"] - 10} more trades')

        # Data Summary
        kline_data = results.get('kline_data', [])
        daily_records = results.get('daily_records', [])
        if len(kline_data) > 0:
            print(f'\n[Data Summary]')
            print(f'  K-line Data Points: {len(kline_data)}')
            print(f'  Daily Records: {len(daily_records)}')
            print(f'  Date Range: {kline_data[0]["date"]} to {kline_data[-1]["date"]}')

        print(f'\n{"="*60}\n')

    def _convert_to_serializable(self, obj: Any) -> Any:
        """Convert object to JSON serializable format"""
        if isinstance(obj, dict):
            return {k: self._convert_to_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [self._convert_to_serializable(item) for item in obj]
        elif isinstance(obj, (int, float, str, bool, type(None))):
            return obj
        elif hasattr(obj, 'item'):  # numpy types
            return obj.item()
        else:
            return float(obj) if obj is not None else None

    def _save_results_to_json(self, results: Dict[str, Any]):
        """Save backtest results to JSON file"""
        try:
            # Get the script directory
            script_dir = Path(__file__).parent
            # Navigate to ../../../data_file/final/
            output_dir = script_dir / '..' / '..' / '..' / 'data_file' / 'final'
            output_dir = output_dir.resolve()

            # Create directory if it doesn't exist
            output_dir.mkdir(parents=True, exist_ok=True)

            # Generate filename with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'backtest_results_{timestamp}.json'
            output_path = output_dir / filename

            # Convert results to JSON-serializable format
            serializable_results = self._convert_to_serializable(results)

            # Write to JSON file with pretty formatting
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(serializable_results, f, indent=2, ensure_ascii=False)

            print(f'[Results Saved]')
            print(f'  JSON file saved to: {output_path}')

        except Exception as e:
            print(f'\n[Warning] Failed to save results to JSON: {e}', file=sys.stderr)


def load_strategy_from_file(strategy_file: str):
    """
    Load strategy class and module from file

    Args:
        strategy_file: Strategy file path

    Returns:
        Tuple of (strategy_class, module)
    """
    if not os.path.exists(strategy_file):
        raise FileNotFoundError(f"Strategy file does not exist: {strategy_file}")

    # Dynamic import module
    spec = importlib.util.spec_from_file_location("strategy_module", strategy_file)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load strategy file: {strategy_file}")

    module = importlib.util.module_from_spec(spec)
    sys.modules["strategy_module"] = module
    spec.loader.exec_module(module)

    # Find strategy class
    strategy_class = None
    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        if (isinstance(attr, type) and
            issubclass(attr, bt.Strategy) and
            attr is not bt.Strategy):
            strategy_class = attr
            break

    if strategy_class is None:
        raise ValueError(f"No valid strategy class found in file {strategy_file}")

    return strategy_class, module


def find_data_loader(module) -> Optional[callable]:
    """
    Find data loading function in module

    Args:
        module: The loaded strategy module

    Returns:
        Data loading function or None
    """
    # Common data loading function names
    common_names = [
        'get_data', 'load_data', 'get_stock_data',
        'fetch_data', 'prepare_data', 'get_hundsun_data'
    ]

    for func_name in common_names:
        if hasattr(module, func_name):
            func = getattr(module, func_name)
            if callable(func):
                return func

    # Search for any function that contains 'data' in its name
    for attr_name in dir(module):
        if 'data' in attr_name.lower() and not attr_name.startswith('_'):
            attr = getattr(module, attr_name)
            if callable(attr) and attr_name not in ['bt', 'pd', 'ak']:
                return attr

    return None


def parse_strategy_params(param_strings: list) -> Dict[str, Any]:
    """
    Parse strategy parameters

    Args:
        param_strings: Parameter string list, format is "key=value"

    Returns:
        Parameter dict
    """
    params = {}
    if not param_strings:
        return params

    for param_str in param_strings:
        if '=' not in param_str:
            print(f"Warning: Ignoring invalid parameter format: {param_str}")
            continue

        key, value = param_str.split('=', 1)
        key = key.strip()
        value = value.strip()

        # Try to convert to numeric type
        try:
            # Try to convert to integer
            if '.' not in value:
                params[key] = int(value)
            else:
                params[key] = float(value)
        except ValueError:
            # If not numeric, keep as string
            # Handle boolean values
            if value.lower() in ('true', 'false'):
                params[key] = value.lower() == 'true'
            else:
                params[key] = value

    return params


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Execute quantitative trading strategy backtest based on backtrader',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example usage:
  # Basic usage
  python run_backtest.py --strategy my_strategy.py --cash 100000

  # With strategy parameters
  python run_backtest.py --strategy my_strategy.py --cash 100000 --params period=20 stop_loss=0.05

  # Set commission and slippage
  python run_backtest.py --strategy my_strategy.py --cash 100000 --commission 0.001 --slippage 0.0005

  # Show chart
  python run_backtest.py --strategy my_strategy.py --cash 100000 --plot
        """
    )

    parser.add_argument(
        '--strategy', '-s',
        required=True,
        help='Strategy file path (Python file containing backtrader Strategy class)'
    )

    parser.add_argument(
        '--cash', '-c',
        type=float,
        default=100000.0,
        help='Initial capital (default: 100000)'
    )

    parser.add_argument(
        '--commission',
        type=float,
        default=0.0005,
        help='Commission rate (default: 0.0005)'
    )

    parser.add_argument(
        '--slippage',
        type=float,
        default=0.0,
        help='Slippage (default: 0)'
    )

    parser.add_argument(
        '--params', '-p',
        nargs='+',
        help='Strategy parameters, format is key=value, multiple parameters separated by space'
    )

    args = parser.parse_args()

    try:
        # Load strategy and module
        strategy_class, module = load_strategy_from_file(args.strategy)
        print(f"Successfully loaded strategy: {strategy_class.__name__}")

        # Parse strategy parameters
        strategy_params = parse_strategy_params(args.params)
        if strategy_params:
            print(f"Strategy parameters: {strategy_params}")

        # Create backtest runner
        runner = BacktestRunner(
            strategy_class=strategy_class,
            cash=args.cash,
            commission=args.commission,
            slippage=args.slippage,
            strategy_params=strategy_params
        )

        # Setup cerebro
        runner.setup_cerebro()

        # Try to find and load data from the strategy module
        data_loader = find_data_loader(module)
        if data_loader:
            print(f"\nFound data loading function: {data_loader.__name__}")
            print("Loading data...")
            try:
                df = data_loader()
                data = bt.feeds.PandasData(dataname=df)
                runner.cerebro.adddata(data)
                print(f"Successfully loaded {len(df)} data points")
            except Exception as e:
                print(f"Warning: Failed to load data using {data_loader.__name__}: {e}")
                print("Proceeding with empty data...")
        else:
            print("\nWarning: No data loading function found in strategy file")
            print("Strategy will run without data. Make sure to add data manually if needed.\n")

        # Run backtest
        results = runner.run()

        return 0

    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
