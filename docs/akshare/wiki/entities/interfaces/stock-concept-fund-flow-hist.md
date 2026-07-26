---
title: "stock_concept_fund_flow_hist - 概念历史资金流"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_concept_fund_flow_hist

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 资金流向 > 东方财富 > 概念历史资金流
- 描述: 东方财富网-数据中心-资金流向-概念资金流-概念历史资金流
- 目标地址: https://data.eastmoney.com/bkzj/BK0574.html
- 限量: 单次获取指定 symbol 的近期概念历史资金流数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 概念历史资金流

接口: stock_concept_fund_flow_hist

目标地址: https://data.eastmoney.com/bkzj/BK0574.html

描述: 东方财富网-数据中心-资金流向-概念资金流-概念历史资金流

限量: 单次获取指定 symbol 的近期概念历史资金流数据

输入参数

| 名称     | 类型  | 描述            |
|--------|-----|---------------|
| symbol | str | symbol="数据要素" |

输出参数

| 名称         | 类型      | 描述      |
|------------|---------|---------|
| 日期         | object  | 注意单位: % |
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

stock_concept_fund_flow_hist_df = ak.stock_concept_fund_flow_hist(symbol="数据要素")
print(stock_concept_fund_flow_hist_df)
```

数据示例

```
      日期      主力净流入-净额  主力净流入-净占比  ... 中单净流入-净占比 小单净流入-净额  小单净流入-净占比
0    2024-08-20 -6.313736e+08      -4.65  ...      -1.32  8.085588e+08       5.96
1    2024-08-21 -3.658787e+08      -2.77  ...      -0.68  4.585833e+08       3.47
2    2024-08-22 -8.680331e+08      -6.05  ...      -1.09  1.004540e+09       7.00
3    2024-08-23 -1.840573e+08      -1.41  ...      -2.69  5.319882e+08       4.07
4    2024-08-26 -1.560898e+08      -1.42  ...      -2.13  3.791972e+08       3.44
..          ...           ...        ...  ...        ...           ...        ...
116  2025-02-18 -1.405755e+10      -8.92  ...       1.16  1.216662e+10       7.72
117  2025-02-19 -9.526664e+08      -0.73  ...      -0.99  2.248251e+09       1.71
118  2025-02-20 -5.894632e+09      -4.55  ...       0.36  5.343512e+09       4.12
119  2025-02-21  2.832990e+09       1.60  ...      -1.23 -5.548521e+08      -0.31
120  2025-02-24 -1.108665e+10      -7.88  ...       1.80  8.521074e+09       6.06
[121 rows x 11 columns]
```
