---
title: "stock_zh_a_hist_pre_min_em - 盘前数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_zh_a_hist_pre_min_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 盘前数据
- 描述: 东方财富-股票行情-盘前数据
- 目标地址: https://quote.eastmoney.com/concept/sh603777.html
- 限量: 单次返回指定 symbol 的最近一个交易日的股票分钟数据, 包含盘前分钟数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 盘前数据

接口: stock_zh_a_hist_pre_min_em

目标地址: https://quote.eastmoney.com/concept/sh603777.html

描述: 东方财富-股票行情-盘前数据

限量: 单次返回指定 symbol 的最近一个交易日的股票分钟数据, 包含盘前分钟数据

输入参数

| 名称         | 类型  | 描述                                  |
|------------|-----|-------------------------------------|
| symbol     | str | symbol="000001"; 股票代码               |
| start_time | str | start_time="09:00:00"; 时间; 默认返回所有数据 |
| end_time   | str | end_time="15:40:00"; 时间; 默认返回所有数据   |

输出参数

| 名称  | 类型      | 描述      |
|-----|---------|---------|
| 时间  | object  | -       |
| 开盘  | float64 | -       |
| 收盘  | float64 | -       |
| 最高  | float64 | -       |
| 最低  | float64 | -       |
| 成交量 | float64 | 注意单位: 手 |
| 成交额 | float64 | -       |
| 最新价 | float64 | -       |

接口示例

```python
import akshare as ak

stock_zh_a_hist_pre_min_em_df = ak.stock_zh_a_hist_pre_min_em(symbol="000001", start_time="09:00:00", end_time="15:40:00")
print(stock_zh_a_hist_pre_min_em_df)
```

数据示例

```
          时间             开盘  收盘   最高  最低    成交量    成交额  最新价
0    2023-12-11 09:15:00  9.30  9.30  9.30  9.30     0        0.0  9.300
1    2023-12-11 09:16:00  9.25  9.28  9.28  9.25     0        0.0  9.300
2    2023-12-11 09:17:00  9.28  9.28  9.28  9.28     0        0.0  9.300
3    2023-12-11 09:18:00  9.28  9.28  9.28  9.28     0        0.0  9.300
4    2023-12-11 09:19:00  9.28  9.27  9.28  9.27     0        0.0  9.300
..                   ...   ...   ...   ...   ...   ...        ...    ...
251  2023-12-11 14:56:00  9.35  9.35  9.35  9.34  7793  7283721.0  9.214
252  2023-12-11 14:57:00  9.34  9.36  9.36  9.34  5169  4833563.0  9.215
253  2023-12-11 14:58:00  9.36  9.36  9.36  9.36    22    20592.0  9.215
254  2023-12-11 14:59:00  9.36  9.36  9.36  9.36     0        0.0  9.215
255  2023-12-11 15:00:00  9.35  9.35  9.35  9.35  7138  6674030.0  9.216
[256 rows x 8 columns]
```
