---
title: "stock_board_concept_spot_em - 东方财富-概念板块-实时行情"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_board_concept_spot_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 概念板块 > 东方财富-概念板块-实时行情
- 描述: 东方财富网-行情中心-沪深京板块-概念板块-实时行情
- 目标地址: https://quote.eastmoney.com/bk/90.BK0818.html
- 限量: 单次返回指定概念板块的实时行情数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 东方财富-概念板块-实时行情

接口: stock_board_concept_spot_em

目标地址: https://quote.eastmoney.com/bk/90.BK0818.html

描述: 东方财富网-行情中心-沪深京板块-概念板块-实时行情

限量: 单次返回指定概念板块的实时行情数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称    | 类型      | 描述 |
|-------|---------|----|
| item  | object  | -  |
| value | float64 | -  |

接口示例

```python
import akshare as ak

stock_board_concept_spot_em_df = ak.stock_board_concept_spot_em(symbol="可燃冰")
print(stock_board_concept_spot_em_df)
```

数据示例

```
  item         value
0   最新  1.138760e+03
1   最高  1.149370e+03
2   最低  1.119960e+03
3   开盘  1.119960e+03
4  成交量  4.543638e+06
5  成交额  2.916916e+09
6  换手率  1.190000e+00
7  涨跌额  2.487000e+01
8  涨跌幅  2.230000e+00
9   振幅  2.640000e+00
```
