import backtrader as bt
import logging
import pandas as pd
import json
from datetime import datetime
from typing import Type
from base_strategy import BaseStrategy

class StrategyRunner:
    def __init__(self, strategy_class: Type[BaseStrategy], live_mode=False, cash=100000, commission=0.001, **strategy_params):
        self.cerebro = bt.Cerebro()
        self.strategy_class = strategy_class
        self.cerebro.addstrategy(strategy_class, live_mode=live_mode, runner=self, **strategy_params)
        self.cerebro.broker.setcash(cash)
        self.cerebro.broker.setcommission(commission=commission)
        self.live_mode = live_mode
        self.cash = cash
        self.commission = commission
        self.strategy_params = strategy_params
        self.trades = []

        if not live_mode:
            self.cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
            self.cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
            self.cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')
        else:
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(message)s')

    def add_data(self, data: pd.DataFrame):
        bt_data = bt.feeds.PandasData(dataname=data)
        self.cerebro.adddata(bt_data)

    def fetch_data(self, symbols: list, start_date: str, end_date: str, **kwargs):
        """从 akshare 获取多个股票数据"""
        import akshare as ak
        for symbol in symbols:
            df = ak.stock_zh_a_hist(symbol=symbol, start_date=start_date, end_date=end_date, adjust="qfq", **kwargs)
            df = df.rename(columns={'日期': 'date', '开盘': 'open', '最高': 'high',
                                    '最低': 'low', '收盘': 'close', '成交量': 'volume'})
            df.set_index('date', inplace=True)
            df.index = pd.to_datetime(df.index)
            self.add_data(df)

    def run(self, output_file='backtest_results.json'):
        if self.live_mode:
            print('Starting Live Mode (Log Simulation)...')
            self.cerebro.run()
            print('Live Mode Completed')
        else:
            print(f'Starting Portfolio Value: {self.cerebro.broker.getvalue():.2f}')
            results = self.cerebro.run()
            print(f'Final Portfolio Value: {self.cerebro.broker.getvalue():.2f}')

            strat = results[0]
            print(f"Sharpe Ratio: {strat.analyzers.sharpe.get_analysis().get('sharperatio', 'N/A')}")
            print(f"Max Drawdown: {strat.analyzers.drawdown.get_analysis()['max']['drawdown']:.2f}%")

            self.__save_results(output_file)
            return results

    def __save_results(self, output_file='backtest_results.json'):
        if self.live_mode:
            return

        data = self.cerebro.datas[0]
        klines = []
        for i in range(-len(data), 0):
            klines.append({
                'date': data.datetime.date(i).isoformat(),
                'open': data.open[i],
                'high': data.high[i],
                'low': data.low[i],
                'close': data.close[i],
                'volume': data.volume[i] if hasattr(data, 'volume') else 0
            })

        results = {
            'config': {
                'strategy': self.strategy_class.__name__,
                'cash': self.cash,
                'commission': self.commission,
                'params': self.strategy_params
            },
            'klines': klines,
            'trades': self.trades,
            'final_value': self.cerebro.broker.getvalue()
        }

        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f'Results saved to {output_file}')
