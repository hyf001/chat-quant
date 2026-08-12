# query_iwencai

- ID: 398
- 分类: i问财接口
- 来源: https://quant.10jqka.com.cn/view/dataplatform/detail/398
- 简介: 问财接口服务，结果与问财网页版相同

## 使用说明

<p align="center">
<img src="https://s.thsi.cn/cd/iwc-web-result-red-rabbit-project/unifiedwap/static/img/wencai_logo_index.png" align="middle" width="200">
</p>

- ?️ 介绍
  [i问财](http://www.iwencai.com/unifiedwap/home/index)同花顺旗下的AI投顾平台，是财经领域落地最为成功的自然语言、语音问答系统。
- ?调用方法：
  `query_iwencai(query,domain='股票',timeout=6,df=True)`
- ?参数说明：
  
  | 参数    | 格式 | 说明                                                                                  |
| ------- | ---- | ------------------------------------------------------------------------------------- |
| query   | str  | 自然语句，语句规范可参考[i问财官方网站](http://www.iwencai.com/unifiedwap/home/index) |
| domain  | str  | 可选'股票'、'基金'、'指数'、'新三板'、'港股'、'美股'                                  |
| timeout | int  | 超时时间                                                                              |
| df      | bool | 格式化dataframe                                                                       |
  
  
- ?作用：
  
  - query_iwencai函数是智能选股函数，可以通过输入自然语言，执行选股并获取股票列表
- ❗注意事项：
  
  - 该函数可获得和网页版问财相同的结果
  - 该函数支持问财专业版的问句
  - 该函数有调用次数限制，每15分钟内限制调用5000次
- ?示例：
  
  ```python
  query_iwencai("近10日的区间主力资金流向>5000万元，市值>1000亿，日成交额>30亿")
  ```
