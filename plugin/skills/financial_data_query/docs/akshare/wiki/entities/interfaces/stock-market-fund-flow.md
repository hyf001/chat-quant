---
title: "stock_market_fund_flow - 大盘资金流"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_market_fund_flow

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 资金流向 > 东方财富 > 大盘资金流
- 描述: 东方财富网-数据中心-资金流向-大盘
- 目标地址: https://data.eastmoney.com/zjlx/dpzjlx.html
- 限量: 单次获取大盘资金流向历史数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 大盘资金流

接口: stock_market_fund_flow

目标地址: https://data.eastmoney.com/zjlx/dpzjlx.html

描述: 东方财富网-数据中心-资金流向-大盘

限量: 单次获取大盘资金流向历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称         | 类型      | 描述      |
|------------|---------|---------|
| 日期         | object  | -       |
| 上证-收盘价     | float64 | -       |
| 上证-涨跌幅     | float64 | 注意单位: % |
| 深证-收盘价     | float64 | -       |
| 深证-涨跌幅     | float64 | 注意单位: % |
| 主力净流入-净额   | float64 | -       |
| 主力净流入-净占比  | float64 | 注意单位: % |
| 超大单净流入-净额  | float64 | -       |
| 超大单净流入-净占比 | float64 | 注意单位: % |
| 大单净流入-净额   | float64 | -       |
| 大单净流入-净占比  | float64 | 注意单位: % |
| 中单净流入-净额   | float64 | -       |
| 中单净流入-净占比  | float64 | 注意单位: % |
| 小单净流入-净额   | float64 | -       |
| 小单净流入-净占比  | float64 | 注意单位: % |

接口示例

```python
import akshare as ak

stock_market_fund_flow_df = ak.stock_market_fund_flow()
print(stock_market_fund_flow_df)
```

数据示例

```
       日期      上证-收盘价 上证-涨跌幅  ...  中单净流入-净占比  小单净流入-净额  小单净流入-净占比
0    2024-02-23  3004.88    0.55  ...      -0.17  5.147947e+09       0.56
1    2024-02-26  2977.02   -0.93  ...       0.08  1.855043e+10       1.88
2    2024-02-27  3015.48    1.29  ...      -1.05 -3.641864e+09      -0.37
3    2024-02-28  2957.85   -1.91  ...       0.12  7.204130e+10       5.31
4    2024-02-29  3015.17    1.94  ...      -1.01 -9.629499e+09      -0.91
..          ...      ...     ...  ...        ...           ...        ...
116  2024-08-13  2867.95    0.34  ...      -0.39  9.309733e+09       1.95
117  2024-08-14  2850.65   -0.60  ...       0.02  8.340414e+09       1.75
118  2024-08-15  2877.36    0.94  ...      -0.97  7.407305e+09       1.25
119  2024-08-16  2879.43    0.07  ...       0.07  1.201517e+10       2.03
120  2024-08-19  2893.67    0.49  ...      -0.25  1.239419e+10       2.17
[121 rows x 15 columns]
```
