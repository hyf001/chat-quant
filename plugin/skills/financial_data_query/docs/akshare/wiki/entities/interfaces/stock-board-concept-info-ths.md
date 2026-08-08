---
title: "stock_board_concept_info_ths - 同花顺-概念板块简介"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_board_concept_info_ths

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 概念板块 > 同花顺-概念板块简介
- 描述: 同花顺-板块-概念板块-板块简介
- 目标地址: http://q.10jqka.com.cn/gn/detail/code/301558/
- 限量: 单次返回所有数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 同花顺-概念板块简介

接口: stock_board_concept_info_ths

目标地址: http://q.10jqka.com.cn/gn/detail/code/301558/

描述: 同花顺-板块-概念板块-板块简介

限量: 单次返回所有数据

输入参数

| 名称     | 类型  | 描述                                                                                |
|--------|-----|-----------------------------------------------------------------------------------|
| symbol | str | symbol: str = "阿里巴巴概念"; 可以通过调用 **ak.stock_board_concept_name_ths()** 查看同花顺的所有概念名称 |

输出参数

| 名称 | 类型      | 描述 |
|----|---------|----|
| 项目 | object  | -  |
| 值  | float64 | -  |

接口示例

```python
import akshare as ak

stock_board_concept_info_ths_df = ak.stock_board_concept_info_ths(symbol="阿里巴巴概念")
print(stock_board_concept_info_ths_df)
```

数据示例

```
         项目         值
0        今开   1825.71
1        昨收   1844.18
2        最低   1752.74
3        最高   1827.99
4   成交量(万手)  12324.70
5      板块涨幅    -4.96%
6      涨幅排名   317/396
7      涨跌家数    25/222
8  资金净流入(亿)   -251.00
9    成交额(亿)   2167.43
```
