---
title: "stock_restricted_release_queue_em - 解禁批次"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_restricted_release_queue_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 限售解禁 > 解禁批次
- 描述: 东方财富网-数据中心-个股限售解禁-解禁批次
- 目标地址: https://data.eastmoney.com/dxf/q/600000.html
- 限量: 单次获取指定 symbol 的解禁批次数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 解禁批次

接口: stock_restricted_release_queue_em

目标地址: https://data.eastmoney.com/dxf/q/600000.html

描述: 东方财富网-数据中心-个股限售解禁-解禁批次

限量: 单次获取指定 symbol 的解禁批次数据

输入参数

| 名称     | 类型  | 描述              |
|--------|-----|-----------------|
| symbol | str | symbol="600000" |

输出参数

| 名称         | 类型      | 描述      |
|------------|---------|---------|
| 序号         | int64   | -       |
| 解禁时间       | object  | -       |
| 解禁股东数      | int64   | -       |
| 解禁数量       | float64 | 注意单位: 股 |
| 实际解禁数量     | float64 | 注意单位: 股 |
| 未解禁数量      | int64   | 注意单位: 股 |
| 实际解禁数量市值   | float64 | 注意单位: 元 |
| 占总市值比例     | float64 | -       |
| 占流通市值比例    | float64 | -       |
| 解禁前一交易日收盘价 | float64 | 注意单位: 元 |
| 限售股类型      | object  | -       |
| 解禁前20日涨跌幅  | float64 | 注意单位: % |
| 解禁后20日涨跌幅  | float64 | 注意单位: % |

接口示例

```python
import akshare as ak

stock_restricted_release_queue_em_df = ak.stock_restricted_release_queue_em(symbol="600000")
print(stock_restricted_release_queue_em_df)
```

数据示例

```
   序号   解禁时间  解禁股东数  ...   限售股类型  解禁前20日涨跌幅  解禁后20日涨跌幅
0   1  2020-09-04      2  ...  定向增发机构配售股份  -3.893637  -6.916996
1   2  2017-03-20     11  ...  定向增发机构配售股份  -2.644231  -5.555556
2   3  2015-10-14      1  ...  定向增发机构配售股份   6.042497  12.085160
3   4  2010-09-29     38  ...  定向增发机构配售股份 -10.334996  15.262321
[4 rows x 13 columns]
```
