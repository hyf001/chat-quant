---
title: "stock_hot_rank_detail_realtime_em - A股"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_hot_rank_detail_realtime_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 股票热度 > 个股人气榜-实时变动 > A股
- 描述: 东方财富网-个股人气榜-实时变动
- 目标地址: http://guba.eastmoney.com/rank/stock?code=000665
- 限量: 单次返回指定 symbol 的股票近期历史数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### A股

接口: stock_hot_rank_detail_realtime_em

目标地址: http://guba.eastmoney.com/rank/stock?code=000665

描述: 东方财富网-个股人气榜-实时变动

限量: 单次返回指定 symbol 的股票近期历史数据

输入参数

| 名称     | 类型  | 描述                |
|--------|-----|-------------------|
| symbol | str | symbol="SZ000665" |

输出参数

| 名称   | 类型      | 描述  |
|------|---------|-----|
| 时间   | object  | -   |
| 排名   | int64   | -   |

接口示例

```python
import akshare as ak

stock_hot_rank_detail_realtime_em_df = ak.stock_hot_rank_detail_realtime_em(symbol="SZ000665")
print(stock_hot_rank_detail_realtime_em_df)
```

数据示例

```
                  时间   排名
0   2022-02-26 00:00:00  170
1   2022-02-26 00:10:00  170
2   2022-02-26 00:20:00  170
3   2022-02-26 00:30:00  170
4   2022-02-26 00:40:00  171
..                  ...  ...
94  2022-02-26 15:40:00  225
95  2022-02-26 15:50:00  224
96  2022-02-26 16:00:00  222
97  2022-02-26 16:10:00  215
98  2022-02-26 16:20:00  211
```
