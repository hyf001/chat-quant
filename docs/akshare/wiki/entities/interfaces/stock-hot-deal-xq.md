---
title: "stock_hot_deal_xq - 交易排行榜"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_hot_deal_xq

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 股票热度 > 股票热度-雪球 > 交易排行榜
- 描述: 雪球-沪深股市-热度排行榜-交易排行榜
- 目标地址: https://xueqiu.com/hq
- 限量: 单次返回指定 symbol 的排行数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 交易排行榜

接口: stock_hot_deal_xq

目标地址: https://xueqiu.com/hq

描述: 雪球-沪深股市-热度排行榜-交易排行榜

限量: 单次返回指定 symbol 的排行数据

输入参数

| 名称     | 类型  | 描述                                      |
|--------|-----|-----------------------------------------|
| symbol | str | symbol="最热门"; choice of {"本周新增", "最热门"} |

输出参数

| 名称   | 类型      | 描述      |
|------|---------|---------|
| 股票代码 | object  | -       |
| 股票简称 | object  | -       |
| 关注   | float64 | -       |
| 最新价  | float64 | 注意单位: 元 |

接口示例

```python
import akshare as ak

stock_hot_deal_xq_df = ak.stock_hot_deal_xq(symbol="最热门")
print(stock_hot_deal_xq_df)
```

数据示例

```
     股票代码  股票简称   关注      最新价
0     SH601318  中国平安  304    38.97
1     SZ002229  鸿博股份  258    24.69
2     SH600519  贵州茅台  257  1663.36
3     SZ002594   比亚迪  257   192.68
4     SH600880  博瑞传播  231     4.90
        ...   ...  ...      ...
5420  SZ300932  三友联众    0    15.95
5421  SZ300956  英力股份    0    18.21
5422  SH688618  三旺通信    0    52.82
5423  BJ836149  旭杰科技    0     7.97
5424  SH688655   迅捷兴    0    14.64
[5425 rows x 4 columns]
```
