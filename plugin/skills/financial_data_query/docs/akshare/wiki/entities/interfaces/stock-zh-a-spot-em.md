---
title: "stock_zh_a_spot_em - 沪深京 A 股"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_zh_a_spot_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: AKShare 股票数据 > A股 > 实时行情数据 > 实时行情数据-东财 > 沪深京 A 股
- 描述: 东方财富网-沪深京 A 股-实时行情数据
- 目标地址: https://quote.eastmoney.com/center/gridlist.html#hs_a_board
- 限量: 单次返回所有沪深京 A 股上市公司的实时行情数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 沪深京 A 股

接口: stock_zh_a_spot_em

目标地址: https://quote.eastmoney.com/center/gridlist.html#hs_a_board

描述: 东方财富网-沪深京 A 股-实时行情数据

限量: 单次返回所有沪深京 A 股上市公司的实时行情数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称      | 类型      | 描述      |
|---------|---------|---------|
| 序号      | int64   | -       |
| 代码      | object  | -       |
| 名称      | object  | -       |
| 最新价     | float64 | -       |
| 涨跌幅     | float64 | 注意单位: % |
| 涨跌额     | float64 | -       |
| 成交量     | float64 | 注意单位: 手 |
| 成交额     | float64 | 注意单位: 元 |
| 振幅      | float64 | 注意单位: % |
| 最高      | float64 | -       |
| 最低      | float64 | -       |
| 今开      | float64 | -       |
| 昨收      | float64 | -       |
| 量比      | float64 | -       |
| 换手率     | float64 | 注意单位: % |
| 市盈率-动态  | float64 | -       |
| 市净率     | float64 | -       |
| 总市值     | float64 | 注意单位: 元 |
| 流通市值    | float64 | 注意单位: 元 |
| 涨速      | float64 | -       |
| 5分钟涨跌   | float64 | 注意单位: % |
| 60日涨跌幅  | float64 | 注意单位: % |
| 年初至今涨跌幅 | float64 | 注意单位: % |

接口示例

```python
import akshare as ak

stock_zh_a_spot_em_df = ak.stock_zh_a_spot_em()
print(stock_zh_a_spot_em_df)
```

数据示例

```
        序号 代码    名称    最新价  ...   涨速 5分钟涨跌  60日涨跌幅  年初至今涨跌幅
0        1  836149  旭杰科技   7.31  ...  0.00   0.00   28.47    -9.53
1        2  300767  震安科技   9.28  ...  0.00   0.00   -9.55   -46.61
2        3  300125  ST聆达   4.67  ...  0.00   0.00  177.98   -62.97
3        4  301027  华蓝集团   8.93  ...  0.00   0.00   17.81   -28.56
4        5  300584  海辰药业  23.26  ...  0.00   0.00   42.44     0.13
...    ...     ...   ...    ...  ...   ...    ...     ...      ...
5630  5631  300531   优博讯  12.45  ... -0.16  -0.24   25.50   -18.52
5631  5632  301302  华如科技  13.47  ...  0.07  -0.07  -28.88   -46.36
5632  5633  300496  中科创达  32.30  ... -0.09  -0.12  -44.60   -59.53
5633  5634  300050  世纪鼎利   5.04  ... -0.20   0.60   72.01     6.55
5634  5635  832175  东方碳素   6.48  ...  0.00   0.00  -21.64   -47.57
[5635 rows x 23 columns]
```
