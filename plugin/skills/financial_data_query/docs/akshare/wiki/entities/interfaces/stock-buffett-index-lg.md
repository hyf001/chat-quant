---
title: "stock_buffett_index_lg - 巴菲特指标"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_buffett_index_lg

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 巴菲特指标
- 描述: 乐估乐股-底部研究-巴菲特指标
- 目标地址: https://legulegu.com/stockdata/marketcap-gdp
- 限量: 单次获取所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 巴菲特指标

接口: stock_buffett_index_lg

目标地址: https://legulegu.com/stockdata/marketcap-gdp

描述: 乐估乐股-底部研究-巴菲特指标

限量: 单次获取所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称     | 类型      | 描述                             |
|--------|---------|--------------------------------|
| 日期     | object  | 交易日                            |
| 收盘价    | float64 | -                              |
| 总市值    | float64 | A股收盘价*已发行股票总股本（A股+B股+H股）       |
| GDP    | float64 | 上年度国内生产总值（例如：2019年，则取2018年GDP） |

接口示例

```python
import akshare as ak

stock_buffett_index_lg_df = ak.stock_buffett_index_lg()
print(stock_buffett_index_lg_df)
```

数据示例

```
         日期      收盘价         总市值        GDP
0     2005-04-08  1003.45    38470.47   161840.16
1     2005-04-11   995.42    39184.81   161840.16
2     2005-04-12   978.70    38955.09   161840.16
3     2005-04-13  1000.90    38287.33   161840.16
4     2005-04-14   986.98    39166.32   161840.16
...          ...      ...         ...         ...
5125  2026-05-20  4850.70  1343475.14  1401879.00
5126  2026-05-21  4783.10  1314824.23  1401879.00
5127  2026-05-22  4845.10  1336559.01  1401879.00
5128  2026-05-25  4921.60  1349958.28  1401879.00
5129  2026-05-26  4947.85  1345774.20  1401879.00
[5130 rows x 4 columns]
```
