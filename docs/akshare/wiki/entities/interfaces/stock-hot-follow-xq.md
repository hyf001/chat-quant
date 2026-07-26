---
title: "stock_hot_follow_xq - 关注排行榜"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_hot_follow_xq

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 股票热度 > 股票热度-雪球 > 关注排行榜
- 描述: 雪球-沪深股市-热度排行榜-关注排行榜
- 目标地址: https://xueqiu.com/hq
- 限量: 单次返回指定 symbol 的排行数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 关注排行榜

接口: stock_hot_follow_xq

目标地址: https://xueqiu.com/hq

描述: 雪球-沪深股市-热度排行榜-关注排行榜

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

stock_hot_follow_xq_df = ak.stock_hot_follow_xq(symbol="最热门")
print(stock_hot_follow_xq_df)
```

数据示例

```
     股票代码  股票简称         关注      最新价
0     SH600519  贵州茅台  2763065.0  1663.36
1     SH601318  中国平安  2321952.0    38.97
2     SH600036  招商银行  2039407.0    28.29
3     SZ000651  格力电器  1768422.0    32.98
4     SZ002594   比亚迪  1494585.0   192.68
        ...   ...        ...      ...
5420  BJ836957  汉维科技      180.0     9.42
5421  BJ836942  恒立钻具      178.0    13.07
5422  BJ836419  万德股份      176.0    11.15
5423  BJ873690   N捷众       30.0    21.01
5424  SZ300307  慈星股份        NaN     6.20
[5425 rows x 4 columns]
```
