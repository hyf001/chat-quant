import backtrader as bt
import logging

class BaseStrategy(bt.Strategy):
    params = (
        ('live_mode', False),
        ('runner', None),
    )

    _name = "base"

    def __init__(self):
        self.order = None
        self.logger = logging.getLogger(self.__class__.__name__)

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        self.logger.info(f'{dt.isoformat()} {txt}')

    def notify_order(self, order: bt.OrderBase) -> None:
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            trade_info = {
                'date': self.datas[0].datetime.date(0).isoformat(),
                'type': 'buy' if order.isbuy() else 'sell',
                'price': order.executed.price,
                'size': order.executed.size,
                'value': order.executed.value,
                'commission': order.executed.comm
            }

            if self.p.runner:
                self.p.runner.trades.append(trade_info)

            if order.isbuy():
                self.log(f'BUY EXECUTED, Price: {order.executed.price:.2f}, Cost: {order.executed.value:.2f}, Comm: {order.executed.comm:.2f}')
            elif order.issell():
                self.log(f'SELL EXECUTED, Price: {order.executed.price:.2f}, Cost: {order.executed.value:.2f}, Comm: {order.executed.comm:.2f}')
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log(f'TRADE PROFIT, Gross: {trade.pnl:.2f}, Net: {trade.pnlcomm:.2f}')

    def buy_signal(self, data=None, size=None, **kwargs):
        """统一的买入接口"""
        if self.order:
            return

        if self.p.live_mode:
            self.log(f'[LIVE] BUY SIGNAL - Size: {size or "default"}')
        else:
            self.order = self.buy(data=data, size=size, **kwargs)

    def sell_signal(self, data=None, size=None, **kwargs):
        """统一的卖出接口"""
        if self.order:
            return

        if self.p.live_mode:
            self.log(f'[LIVE] SELL SIGNAL - Size: {size or "default"}')
        else:
            self.order = self.sell(data=data, size=size, **kwargs)

    def next(self):
        """子类需要实现具体策略逻辑"""
        raise NotImplementedError("Subclass must implement next()")
