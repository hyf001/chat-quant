# 高量定义：当天的成交量 > 前三天任意一天，不管红绿
# 箱体：顶部高量最高价，底部是高量最低价
# 从高亮开始知道最后，股价必须在箱体内
# 最近3交易日至少有一天股价突破箱体，且上涨的时候是放量，下跌时是缩量

import pandas as pd
from datetime import date,timedelta
from pathlib import Path
import sys
from types import SimpleNamespace

api_root = Path(__file__).resolve().parent / "apps" / "api"
if str(api_root) not in sys.path:
    sys.path.insert(0, str(api_root))

from app.service.dataset.python_api import query_dataset
from app.service.stock_pool.python_api import add_pool_stocks

chatq = SimpleNamespace(
    query_dataset=query_dataset,
    add_pool_stocks=add_pool_stocks,
)
start_offset = -30
recent_days = date.today() + timedelta(days=start_offset)
sql = f"""select symbol,open,high,low,close,volume,trade_date 
from a_stock_daily_price_pre_adjusted where trade_date >= '{recent_days.strftime("%Y%m%d")}' order by symbol,trade_date
"""

df_all = chatq.query_dataset(sql)
print(df_all['trade_date'].max())
stock_df_dict = {symbol:group for symbol,group in df_all.groupby('symbol')} #股票为key，value是这个股票的行情

def high_volumn(stock_df:pd.DataFrame,offset):
    """
    是否高量,如果是就返回高量的顶部和底部
    """
    df_len = len(stock_df)
    if offset + df_len < 3:
        return None
    volume_pre = stock_df.iloc[offset-3:offset]['volume']
    volume_current = stock_df.iloc[offset]['volume']
    if volume_current > volume_pre.max():
        return stock_df.iloc[offset]['high'],stock_df.iloc[offset]['low'],stock_df.iloc[offset]['trade_date']
        


def is_in_box(df:pd.DataFrame):
    """
    是否在箱体内部
    """
    if df is None or df.empty:
        return False
    top = df.iloc[0]['high']
    bottom = df.iloc[0]['low']
    mask = df['open'].between(bottom, top) & df['close'].between(bottom, top)
    return mask.all()

def is_break(df:pd.DataFrame,high,low):
    """
    股价是否有突破
    """
    mask = df['close'] > high
    return mask.any()
    

stock_high_volumn_in_box:dict[str,list]={} 

for stock in stock_df_dict:
    stock_df = stock_df_dict[stock]
    for offset in range (-10,-30,-1):
        high_low_date =  high_volumn(stock_df,offset)
        if  high_low_date is None:
            continue
        stock_df_after_offset = stock_df.iloc[offset:-5] # 日期大于offset之后到-5的行情
        stock_df_after_5 = stock_df.iloc[-5:] # -5之后到行情
        if is_in_box(stock_df_after_offset) and is_break(stock_df_after_5,high_low_date[0],high_low_date[1]):
            stock_high_volumn_in_box.setdefault(stock,[]).append(high_low_date[2])

stock_notes = {
    stock: f"高量日期：{', '.join(dates)}"
    for stock, dates in stock_high_volumn_in_box.items()
}
chatq.add_pool_stocks('高量选股', [s for s in stock_high_volumn_in_box], note=stock_notes)
stock_high_volumn_in_box
