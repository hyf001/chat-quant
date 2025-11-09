import backtrader as bt
import talib
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from base_strategy import BaseStrategy

class MACrossStrategy(BaseStrategy):
    params = (
        ('ma_short', 10),
        ('ma_mid', 30),
        ('ma_long', 60),
    )

    def __init__(self):
        super().__init__()
        self.ma10 = None
        self.ma30 = None
        self.ma60 = None

    def next(self):
        close = self.datas[0].close

        # 使用 TA-Lib 计算移动平均线
        if len(close) >= self.p.ma_long:
            close_array = close.get(size=self.p.ma_long)
            self.ma10 = talib.SMA(close_array, timeperiod=self.p.ma_short)[-1]
            self.ma30 = talib.SMA(close_array, timeperiod=self.p.ma_mid)[-1]
            self.ma60 = talib.SMA(close_array, timeperiod=self.p.ma_long)[-1]

        # 交易逻辑
        if self.ma10 and self.ma30 and self.ma60:
            close_price = close[0]
            if not self.position:
                if close_price < self.ma10 and close_price < self.ma30 and close_price < self.ma60:
                    self.buy_signal()
            else:
                if close_price > self.ma10 and close_price > self.ma30 and close_price > self.ma60:
                    self.sell_signal()
