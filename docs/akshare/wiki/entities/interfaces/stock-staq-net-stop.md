---
title: "stock_staq_net_stop - 两网及退市"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_staq_net_stop

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 两网及退市
- 描述: 东方财富网-行情中心-沪深个股-两网及退市
- 目标地址: https://quote.eastmoney.com/center/gridlist.html#staq_net_board
- 限量: 单次获取所有两网及退市的股票数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 两网及退市

接口: stock_staq_net_stop

目标地址: https://quote.eastmoney.com/center/gridlist.html#staq_net_board

描述: 东方财富网-行情中心-沪深个股-两网及退市

限量: 单次获取所有两网及退市的股票数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称  | 类型     | 描述  |
|-----|--------|-----|
| 序号  | int64  | -   |
| 代码  | object | -   |
| 名称  | object | -   |

接口示例

```python
import akshare as ak

stock_staq_net_stop_df = ak.stock_staq_net_stop()
print(stock_staq_net_stop_df)
```

数据示例

```
      序号   代码      名称
0      1  400199    阳光城5
1      2  400170     运盛5
2      3  400039  华  圣 5
3      4  400119     西创5
4      5  400045     猴王5
..   ...     ...     ...
199  200  400149     金泰5
200  201  400155     海医5
201  202  400142     宝德5
202  203  400163     计通5
203  204  400046     博嘉5
[204 rows x 3 columns]
```
