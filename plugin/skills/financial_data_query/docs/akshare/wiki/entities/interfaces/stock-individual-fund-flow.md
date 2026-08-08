---
title: "stock_individual_fund_flow - 个股资金流"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_individual_fund_flow

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 资金流向 > 东方财富 > 个股资金流
- 描述: 东方财富网-数据中心-个股资金流向
- 目标地址: https://data.eastmoney.com/zjlx/detail.html
- 限量: 单次获取指定市场和股票的近 100 个交易日的资金流数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 个股资金流

接口: stock_individual_fund_flow

目标地址: https://data.eastmoney.com/zjlx/detail.html

描述: 东方财富网-数据中心-个股资金流向

限量: 单次获取指定市场和股票的近 100 个交易日的资金流数据

输入参数

| 名称     | 类型  | 描述                                                 |
|--------|-----|----------------------------------------------------|
| stock  | str | stock="000425"; 股票代码                               |
| market | str | market="sh"; 上海证券交易所: sh, 深证证券交易所: sz, 北京证券交易所: bj |

输出参数

| 名称         | 类型      | 描述      |
|------------|---------|---------|
| 日期         | object  | -       |
| 收盘价        | float64 | -       |
| 涨跌幅        | float64 | 注意单位: % |
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

stock_individual_fund_flow_df = ak.stock_individual_fund_flow(stock="600094", market="sh")
print(stock_individual_fund_flow_df)
```

数据示例

```
    日期   收盘价   涨跌幅  ...  中单净流入-净占比    小单净流入-净额  小单净流入-净占比
0    2023-03-31  3.13 -0.32  ...       4.02    240002.0       0.95
1    2023-04-03  3.18  1.60  ...      -0.93    910076.0       2.50
2    2023-04-04  3.13 -1.57  ...      10.87    929360.0       2.25
3    2023-04-06  3.11 -0.64  ...      -4.87   5618110.0      17.43
4    2023-04-07  3.15  1.29  ...      -7.44   -839635.0      -3.00
..          ...   ...   ...  ...        ...         ...        ...
96   2023-08-22  3.50 -0.57  ...       2.99  10665906.0      10.36
97   2023-08-23  3.46 -1.14  ...       1.45   6542085.0       8.41
98   2023-08-24  3.45 -0.29  ...       5.15  -4355064.0      -5.41
99   2023-08-25  3.43 -0.58  ...      -1.51 -18759517.0     -22.13
100  2023-08-28  3.51  2.33  ...      14.49  10409307.0       5.47
[101 rows x 13 columns]
```
