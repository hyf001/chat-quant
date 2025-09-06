
import logging
from core.data_fetcher import DataFetcher




def setUpLogger() -> logging.Logger:
  # 创建logger
  logger = logging.getLogger(__name__)
  logger.setLevel(logging.INFO)
  
  # 防止重复添加handler
  if logger.handlers:
    logger.handlers.clear()


  # 创建log目录（如果不存在）
  import os
  os.makedirs('log', exist_ok=True)
  
  # 创建文件handler - 修改路径到log/app.log
  file_handler = logging.FileHandler('log/app.log', mode='w')
  file_handler.setLevel(logging.INFO)

  # 创建formatter - 添加时间
  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

  # 将formatter添加到handler
  file_handler.setFormatter(formatter)

  # 将handler添加到logger
  logger.addHandler(file_handler)
  return logger

if __name__ == '__main__':
     logger = setUpLogger()
     logger.info("app start")
     #data_fetcher = DataFetcher()
     #data_fetcher.fetch_historical_data('300033','20250830','20250904')
     #data_fetcher._fetch_historical_tick('sz301259')
     #data_fetcher.sync_historical_data('300033','20250801','20250905')
     