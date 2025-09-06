from util import sql_executor
import logging
import pandas as pd
import akshare as ak
from datetime import datetime,timedelta
import pymysql

class DataFetcher:
    def __init__(self):
        self.logger = logging.getLogger("data_fetcher")
        pass


    def sync_historical_data(self,stock,start_date,end_date): 
        """
        同步股票数据到数据库
        """
        self.logger.info(f"开始同步数据，股票{stock},开始时间{start_date},结束时间{end_date}")
        df_data : pd.DataFram = self._fetch_historical_data(stock,start_date=start_date,end_date=end_date)
        if df_data.empty:
            return
        df_to_save = df_data.copy()
        df_to_save['日期'] = pd.to_datetime(df_to_save['日期']).dt.strftime('%Y%m%d')
        #删除旧的数据
        sql_executor.execute_sql(f"delete from stock_data_day where stock_code = %s and data_date between %s and %s",
                                 df_to_save['股票代码'][0],df_to_save['日期'].min(),df_to_save['日期'].max())
        
        data_list : list[tuple] = []
        for _, row in df_to_save.iterrows():
            data_list.append((row['日期'],row['股票代码'],
                        row['开盘'],row['收盘'],
                        row['最高'],row['最低'],
                        row['成交量'],row['成交额'],
                        row['振幅'],row['涨跌幅'],
                        row['涨跌额'],row['换手率']))
        sql_executor.execute_batch("""INSERT INTO stock_data_day 
                                    (data_date,stock_code, open, close, high, low, volume,
                                    turnover,amplitude,change_rate,change_amount,turnover_rate)
                        VALUES ( %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s)""",
                        data_list)
        self.logger.info(f"同步数据结束，共{len(data_list)}条")


    """股票市场总貌"""
    """个股信息查询"""  
    """行情报价"""
    """历史行情数据"""    
    def _fetch_historical_data(self,stock,start_date,end_date) -> pd.DataFrame:
        if start_date is None or end_date is None :
            raise Exception('缺少开始或结束时间,时间格式必须是%Y-%m-%d')
        #处理股票代码
        stock_code : str = str(stock).strip().upper()
        if stock_code.endswith('.SZ') or stock_code.endswith('.SH'):
            stock_code = stock_code.replace('.SZ','').replace('.SH','')
        df = ak.stock_zh_a_hist(symbol=stock_code,period='daily',
                                start_date=start_date,end_date=end_date,adjust='qfq')
        return df
    
    """历史分比数据"""
    def _fetch_historical_tick(self,stock) -> pd.DataFrame:
        stock_code : str = str(stock).strip().lower
        print(stock_code)
        df = ak.stock_zh_a_tick_tx_js(symbol=stock_code)
        print(df)
        return df