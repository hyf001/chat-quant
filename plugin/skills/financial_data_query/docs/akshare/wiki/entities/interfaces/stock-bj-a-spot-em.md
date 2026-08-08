---
title: "stock_bj_a_spot_em - 京 A 股"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_bj_a_spot_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: AKShare 股票数据 > A股 > 实时行情数据 > 实时行情数据-东财 > 京 A 股
- 描述: 东方财富网-京 A 股-实时行情数据
- 目标地址: http://quote.eastmoney.com/center/gridlist.html#bj_a_board
- 限量: 单次返回所有京 A 股上市公司的实时行情数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 京 A 股

接口: stock_bj_a_spot_em

目标地址: http://quote.eastmoney.com/center/gridlist.html#bj_a_board

描述: 东方财富网-京 A 股-实时行情数据

限量: 单次返回所有京 A 股上市公司的实时行情数据

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

stock_bj_a_spot_em_df = ak.stock_bj_a_spot_em()
print(stock_bj_a_spot_em_df)
```

数据示例

```
      序号  代码   名称      最新价 涨跌幅  ...    流通市值  涨速 5分钟涨跌 60日涨跌幅 年初至今涨跌幅
0      1  836149  旭杰科技   7.31  29.84  ...   349965819  0.00   0.00   28.47    -9.53
1      2  871263  莱赛激光   9.95   8.86  ...   271814568 -0.40   1.84   -8.63   -50.74
2      3  833873  中设咨询   3.32   4.73  ...   362479267  0.00  -0.90   13.70   -23.33
3      4  833230  欧康医药   9.61   4.46  ...   321772274  0.31   0.21    6.31   -31.60
4      5  836892  广咨国际   7.68   4.35  ...  1025658954 -0.13   0.92  -11.52   -30.94
..   ...     ...   ...    ...    ...  ...         ...   ...    ...     ...      ...
249  250  833575  康乐卫士  14.93  -8.69  ...  2789441772 -0.86  -0.99  -27.63   -44.99
250  251  430476  海能技术   6.10  -9.09  ...   392764330 -0.16   0.16  -25.52   -59.03
251  252  832149   利尔达   4.28  -9.51  ...   490226248 -0.47  -0.93   25.15   -41.61
252  253  872374  云里物里  11.30  -9.89  ...   330132913  0.71   0.09   29.74   -27.47
253  254  832175  东方碳素   6.48 -20.20  ...   391996578  0.00   0.00  -21.64   -47.57
[254 rows x 23 columns]
```
