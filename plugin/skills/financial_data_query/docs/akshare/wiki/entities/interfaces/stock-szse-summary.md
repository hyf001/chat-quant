---
title: "stock_szse_summary - 证券类别统计"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_szse_summary

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: AKShare 股票数据 > A股 > 股票市场总貌 > 深圳证券交易所 > 证券类别统计
- 描述: 深圳证券交易所-市场总貌-证券类别统计
- 目标地址: http://www.szse.cn/market/overview/index.html
- 限量: 单次返回指定 date 的市场总貌数据-证券类别统计(当前交易日的数据需要交易所收盘后统计)
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 证券类别统计

接口: stock_szse_summary

目标地址: http://www.szse.cn/market/overview/index.html

描述: 深圳证券交易所-市场总貌-证券类别统计

限量: 单次返回指定 date 的市场总貌数据-证券类别统计(当前交易日的数据需要交易所收盘后统计)

输入参数

| 名称   | 类型  | 描述                                  |
|------|-----|-------------------------------------|
| date | str | date="20200619"; 当前交易日的数据需要交易所收盘后统计 |

输出参数

| 名称   | 类型      | 描述      |
|------|---------|---------|
| 证券类别 | object  | -       |
| 数量   | int64   | 注意单位: 只 |
| 成交金额 | float64 | 注意单位: 元 |
| 总市值  | float64 | -       |
| 流通市值 | float64 | -       |

接口示例

```python
import akshare as ak

stock_szse_summary_df = ak.stock_szse_summary(date="20200619")
print(stock_szse_summary_df)
```

数据示例

```
     证券类别    数量          成交金额           总市值          流通市值
0      股票  2284  4.647749e+11  2.706514e+13  2.104546e+13
1    主板A股   460  9.775950e+10  7.864787e+12  6.943990e+12
2    主板B股    46  8.626816e+07  4.759658e+10  4.706385e+10
3     中小板   960  2.013526e+11  1.130741e+13  8.669555e+12
4   创业板A股   818  1.655765e+11  7.845345e+12  5.384854e+12
5      基金   551  1.362524e+10  2.417277e+11  2.417277e+11
6     ETF   100  1.165436e+10  1.628294e+11  1.628294e+11
7     LOF   250  7.335768e+08  4.043156e+10  4.043156e+10
8   封闭式基金     1  5.527571e+05  7.622440e+08  7.622440e+08
9    分级基金   200  1.236746e+09  3.770451e+10  3.770451e+10
10     债券  7174  1.371389e+11           NaN           NaN
11   债券现券  6599  2.911357e+10  3.683881e+13  1.823072e+12
12   债券回购    13  1.054592e+11           NaN           NaN
13    ABS   562  2.566134e+09  4.849642e+11  4.849642e+11
14     期权   108  2.441560e+08           NaN           NaN
```
