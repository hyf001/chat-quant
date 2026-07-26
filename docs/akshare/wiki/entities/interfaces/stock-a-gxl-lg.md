---
title: "stock_a_gxl_lg - A 股股息率"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_a_gxl_lg

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > A 股股息率
- 描述: 乐咕乐股-股息率-A 股股息率
- 目标地址: https://legulegu.com/stockdata/guxilv
- 限量: 单次获取指定 symbol 的所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### A 股股息率

接口: stock_a_gxl_lg

目标地址: https://legulegu.com/stockdata/guxilv

描述: 乐咕乐股-股息率-A 股股息率

限量: 单次获取指定 symbol 的所有历史数据

输入参数

| 名称     | 类型  | 描述                                                      |
|--------|-----|---------------------------------------------------------|
| symbol | str | symbol="上证A股"; choice of {"上证A股", "深证A股", "创业板", "科创板"} |

输出参数

| 名称  | 类型      | 描述  |
|-----|---------|-----|
| 日期  | object  | -   |
| 股息率 | float64 | -   |

接口示例

```python
import akshare as ak

stock_a_gxl_lg_df = ak.stock_a_gxl_lg(symbol="上证A股")
print(stock_a_gxl_lg_df)
```

数据示例

```
           日期   股息率
0     2005-01-04  2.03
1     2005-01-05  2.05
2     2005-01-06  2.07
3     2005-01-07  2.06
4     2005-01-10  2.05
          ...   ...
4685  2024-04-18  3.44
4686  2024-04-19  3.44
4687  2024-04-22  3.48
4688  2024-04-23  3.52
4689  2024-04-24  3.50
[4690 rows x 2 columns]
```
