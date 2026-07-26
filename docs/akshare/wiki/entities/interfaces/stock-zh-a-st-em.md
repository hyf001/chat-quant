---
title: "stock_zh_a_st_em - 风险警示板"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_zh_a_st_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 风险警示板
- 描述: 东方财富网-行情中心-沪深个股-风险警示板
- 目标地址: https://quote.eastmoney.com/center/gridlist.html#st_board
- 限量: 单次返回当前交易日风险警示板的所有股票的行情数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

### 风险警示板

接口: stock_zh_a_st_em

目标地址: https://quote.eastmoney.com/center/gridlist.html#st_board

描述: 东方财富网-行情中心-沪深个股-风险警示板

限量: 单次返回当前交易日风险警示板的所有股票的行情数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称     | 类型      | 描述      |
|--------|---------|---------|
| 序号     | int64   | -       |
| 代码     | object  | -       |
| 名称     | object  | -       |
| 最新价    | float64 | -       |
| 涨跌幅    | float64 | 注意单位: % |
| 涨跌额    | float64 | -       |
| 成交量    | float64 | -       |
| 成交额    | float64 | -       |
| 振幅     | float64 | 注意单位: % |
| 最高     | float64 | -       |
| 最低     | float64 | -       |
| 今开     | float64 | -       |
| 昨收     | float64 | -       |
| 量比     | float64 | -       |
| 换手率    | float64 | 注意单位: % |
| 市盈率-动态 | float64 | -       |
| 市净率    | float64 | -       |

接口示例

```python
import akshare as ak

stock_zh_a_st_em_df = ak.stock_zh_a_st_em()
print(stock_zh_a_st_em_df)
```

数据示例

```
      序号      代码     名称    最新价    涨跌幅  ...     昨收    量比    换手率   市盈率-动态    市净率
0      1  300313  *ST天山   7.61  10.45  ...   6.89  7.84  11.96   -90.65  33.49
1      2  300167  ST迪威迅   3.19   7.41  ...   2.97  3.86   9.31    -5.82  54.39
2      3  002569   ST步森   6.90   5.02  ...   6.57  0.88   0.93   -27.27   7.05
3      4  000996  *ST中期   5.24   5.01  ...   4.99  0.81   4.47  6823.87   3.73
4      5  600589  *ST榕泰   5.48   4.98  ...   5.22  1.71   4.07   -24.53  -5.13
..   ...     ...    ...    ...    ...  ...    ...   ...    ...      ...    ...
113  114  000615  *ST美谷   4.10  -4.87  ...   4.31  1.25   5.02   -37.97 -15.44
114  115  000697  *ST炼石   4.82  -4.93  ...   5.07  2.60   1.62    -9.97  -5.81
115  116  000889   ST中嘉   2.12  -4.93  ...   2.23  0.40   0.91   -68.39   8.04
116  117  000752  *ST西发   9.01  -4.96  ...   9.48  0.19   1.26   -64.79 -48.62
117  118  600766  *ST园城  12.34  -5.00  ...  12.99  1.56   1.05  1372.29  47.59
[118 rows x 17 columns]
```
