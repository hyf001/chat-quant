---
title: "stock_sh_a_spot_em - 沪 A 股"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_sh_a_spot_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: AKShare 股票数据 > A股 > 实时行情数据 > 实时行情数据-东财 > 沪 A 股
- 描述: 东方财富网-沪 A 股-实时行情数据
- 目标地址: http://quote.eastmoney.com/center/gridlist.html#sh_a_board
- 限量: 单次返回所有沪 A 股上市公司的实时行情数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 沪 A 股

接口: stock_sh_a_spot_em

目标地址: http://quote.eastmoney.com/center/gridlist.html#sh_a_board

描述: 东方财富网-沪 A 股-实时行情数据

限量: 单次返回所有沪 A 股上市公司的实时行情数据

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

stock_sh_a_spot_em_df = ak.stock_sh_a_spot_em()
print(stock_sh_a_spot_em_df)
```

数据示例

```
      序号    代码    名称   最新价  ...  涨速  5分钟涨跌 60日涨跌幅 年初至今涨跌幅
0        1  688670   金迪克  12.80  ... -0.16   0.00  -19.14   -55.02
1        2  688656   浩欧博  22.40  ... -0.62  -0.40   -4.92   -34.81
2        3  603183   建研院   3.71  ...  0.00   0.00   10.09   -19.87
3        4  603909  建发合诚   7.98  ...  0.13   0.25  -16.09   -29.26
4        5  603700  宁水集团   9.97  ...  0.00   0.00    0.30   -28.63
...    ...     ...   ...    ...  ...   ...    ...     ...      ...
2380  2381  601512  中新集团   6.70  ...  0.00  -0.30  -18.69    -9.95
2381  2382  600187  国中水务   3.02  ...  0.00   0.00   41.12    14.39
2382  2383  603499  翔港科技  12.32  ...  0.00   0.00  -30.24    14.82
2383  2384  605178  时空科技  13.48  ...  0.00  -0.74    9.06   -51.39
2384  2385  688175  高凌信息  11.49  ...  0.00   0.00  -30.15   -42.00
[2385 rows x 23 columns]
```
