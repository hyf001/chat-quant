# get_iwencai

- ID: 399
- 分类: i问财接口
- 来源: https://quant.10jqka.com.cn/view/dataplatform/detail/399
- 简介: 自然语言选股接口服务，选股结果与问财backtest等同。仅支持在股票策略初始化阶段调用。

## 使用说明

<p align="center">
<img src="https://s.thsi.cn/cd/iwc-web-result-red-rabbit-project/unifiedwap/static/img/wencai_logo_index.png" align="middle" width="200">
</p>

- ?️ 介绍
  [backtest](http://backtest.10jqka.com.cn/)是同花顺i问财推出的策略回测服务，可以基于自然语言快速选出每天符合条件的股票池
- ?调用方法：
  `get_iwencai(sentence, set_attr, version)`
- ?参数说明：
  
  | 参数      | 格式 | 说明                                                                                                                                                         |
| --------- | ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| sentence  | str  | 自然语句，语句规范可参考[backtest](http://backtest.10jqka.com.cn/)                                                                                           |
| set\_attr | str  | 如果该参数不输入,则返回的股票列表默认保存在context.iwencai_securities中如果该参数输入'stocks_list'(自定义),则返回的股票列表保存在context.stocks_list中 |
| version   | str  | 'stable':稳定版'online':为正式版备注：如果您希望跟问财官网保持一致，请使用'online'                                                                           |
  
  
- ?作用：
  
  - get_iwencai函数是智能选股函数，可以通过输入自然语言，执行选股并获取股票列表(仅可在股票API策略框架的[初始化函数]()中调用)
- ❗注意事项：
  
  - 该函数是智能选股函数,属于初始化函数，必须在init函数下设置,否则无效
  - 该函数设置在init函数下时，系统会保存该语句，并使得该函数能每天执行选股，将结果保存至context对象中
  - 该函数的set_attr参数不输入, 则会将返回的股票列表默认保存在context.iwencai_securities中
  - get_iwencai的选股结果不会直接输出,返回值为空
  - 该函数有调用次数限制，每15分钟内限制调用5000次
- ?示例一：
  
  ```python
  def init(context):
      # 输入选股条件
      get_iwencai('净利润增长大于20%,股价位于20日均线上方')
  
  def handle_bar(context, bar_dict):
      # 打印输回测出前一日收盘后的选股结果
      log.info(context.iwencai_securities)
  ```
- ?示例二：
  
  ```python
  # 研究环境中使用get_iwencai
  get_iwencai = get_iwencai = get_open_api('public').get_iwencai
  stk_pool 
  ```
