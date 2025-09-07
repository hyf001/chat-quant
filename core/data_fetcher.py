from util import sql_executor
import logging
import pandas as pd
import akshare as ak
from datetime import datetime,timedelta
import pymysql
from core.data_fetch.data_fetcher_1 import create_query_service

class DataFetcher:
    def __init__(self):
        self.logger = logging.getLogger("data_fetcher")
        try:
            # 初始化统一查询服务
            self.query_service = create_query_service()
            self.logger.info("统一查询服务初始化成功")
        except Exception as e:
            self.logger.warning(f"统一查询服务初始化失败: {e}")
            self.query_service = None


    def sync_historical_data(self,stock : str,start_date,end_date): 
        """
        同步股票数据到数据库
        """
        self.logger.info(f"开始同步数据，股票{stock},开始时间{start_date},结束时间{end_date}")
        df_data : pd.DataFrame = self._fetch_historical_data(stock,start_date=start_date,end_date=end_date)
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
        stock_code : str = str(stock).strip().lower()
        print(stock_code)
        df = ak.stock_zh_a_tick_tx_js(symbol=stock_code)
        print(df)
        return df

    # ==================== 统一查询接口 ====================
    
    def query_api(self, api_name: str, **kwargs) -> pd.DataFrame:
        """
        统一API查询接口
        
        Args:
            api_name: API名称（基于schemas/akshare目录下的元数据）
            **kwargs: 查询参数
            
        Returns:
            pandas.DataFrame: 查询结果
            
        Example:
            # 查询股票历史数据
            result = data_fetcher.query_api(
                'stock_zh_a_hist',
                symbol='000001',
                start_date='20240901',
                end_date='20240910',
                period='daily',
                adjust='qfq'
            )
        """
        if not self.query_service:
            raise RuntimeError("统一查询服务未初始化")
        
        try:
            self.logger.info(f"调用API: {api_name}, 参数: {kwargs}")
            result = self.query_service.query_direct(api_name, **kwargs)
            self.logger.info(f"API调用完成，返回 {len(result)} 行数据")
            return result
        except Exception as e:
            self.logger.error(f"API调用失败: {e}")
            raise
    
    def get_stock_history_unified(self, symbol: str, start_date: str = None, 
                                end_date: str = None, period: str = 'daily', 
                                adjust: str = 'qfq') -> pd.DataFrame:
        """
        获取股票历史数据（使用统一接口）
        
        Args:
            symbol: 股票代码
            start_date: 开始日期 YYYYMMDD
            end_date: 结束日期 YYYYMMDD
            period: 周期 daily/weekly/monthly
            adjust: 复权方式 qfq/hfq/''
            
        Returns:
            pandas.DataFrame: 股票历史数据
        """
        if not self.query_service:
            raise RuntimeError("统一查询服务未初始化")
        
        return self.query_service.get_stock_history(
            symbol=symbol,
            start_date=start_date,
            end_date=end_date,
            period=period,
            adjust=adjust
        )
    
    def list_available_apis(self) -> dict:
        """
        列出可用的API接口
        
        Returns:
            dict: {api_name: display_name} 字典
        """
        if not self.query_service:
            return {}
        
        return self.query_service.list_available_apis()
    
    def describe_api(self, api_name: str) -> str:
        """
        获取API详细描述
        
        Args:
            api_name: API名称
            
        Returns:
            str: API的详细描述信息
        """
        if not self.query_service:
            return "统一查询服务未初始化"
        
        return self.query_service.describe_api(api_name)
    
    def create_query_builder(self):
        """
        创建查询构建器
        
        Returns:
            QueryBuilder: 查询构建器实例
            
        Example:
            result = data_fetcher.create_query_builder() \
                .api('stock_zh_a_hist') \
                .param('symbol', '000001') \
                .param('start_date', '20240901') \
                .execute()
        """
        if not self.query_service:
            raise RuntimeError("统一查询服务未初始化")
        
        return self.query_service.create_query()