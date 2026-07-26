---
title: "stock_hot_rank_detail_em - A股"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_hot_rank_detail_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 股票热度 > 历史趋势及粉丝特征 > A股
- 描述: 东方财富网-股票热度-历史趋势及粉丝特征
- 目标地址: http://guba.eastmoney.com/rank/stock?code=000665
- 限量: 单次返回指定 symbol 的股票近期历史数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### A股

接口: stock_hot_rank_detail_em

目标地址: http://guba.eastmoney.com/rank/stock?code=000665

描述: 东方财富网-股票热度-历史趋势及粉丝特征

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
| 证券代码 | object  | -   |
| 新晋粉丝 | float64 | -   |
| 铁杆粉丝 | float64 | -   |

接口示例

```python
import akshare as ak

stock_hot_rank_detail_em_df = ak.stock_hot_rank_detail_em(symbol="SZ000665")
print(stock_hot_rank_detail_em_df)
```

数据示例

```
         时间    排名   证券代码   新晋粉丝 铁杆粉丝
0    2024-07-24  4973  SZ871245  0.4259  0.5741
1    2024-07-25  2231  SZ871245  0.5476  0.4524
2    2024-07-26  2870  SZ871245  0.6578  0.3422
3    2024-07-27  4862  SZ871245  0.6669  0.3331
4    2024-07-28  4452  SZ871245  0.6725  0.3275
..          ...   ...       ...     ...     ...
361  2025-07-20  5052  SZ871245  0.5067  0.4933
362  2025-07-21   459  SZ871245  0.8479  0.1521
363  2025-07-22   548  SZ871245  0.9044  0.0956
364  2025-07-23  1610  SZ871245  0.9134  0.0866
365  2025-07-24  3646  SZ871245  0.9175  0.0825
[366 rows x 5 columns]
```
