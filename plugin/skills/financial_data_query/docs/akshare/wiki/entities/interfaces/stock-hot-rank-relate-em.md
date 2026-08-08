---
title: "stock_hot_rank_relate_em - 相关股票"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_hot_rank_relate_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 股票热度 > 相关股票
- 描述: 东方财富-个股人气榜-相关股票
- 目标地址: http://guba.eastmoney.com/rank/stock?code=000665
- 限量: 单次返回指定 symbol 的股票近期历史数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 相关股票

接口: stock_hot_rank_relate_em

目标地址: http://guba.eastmoney.com/rank/stock?code=000665

描述: 东方财富-个股人气榜-相关股票

限量: 单次返回指定 symbol 的股票近期历史数据

输入参数

| 名称     | 类型  | 描述                |
|--------|-----|-------------------|
| symbol | str | symbol="SZ000665" |

输出参数

| 名称     | 类型      | 描述  |
|--------|---------|-----|
| 时间     | object  | -   |
| 股票代码   | object  | -   |
| 相关股票代码 | object  | -   |
| 涨跌幅    | float64 | -   |

接口示例

```python
import akshare as ak

stock_hot_rank_relate_em_df = ak.stock_hot_rank_relate_em(symbol="SZ000665")
print(stock_hot_rank_relate_em_df)
```

数据示例

```
              时间       股票代码   相关股票代码 涨跌幅
0  2024-09-30 20:00:00  SZ000665  SZ300059  6.18
1  2024-09-30 20:00:00  SZ000665  SZ000158  4.46
2  2024-09-30 20:00:00  SZ000665  SH600519  2.71
3  2024-09-30 20:00:00  SZ000665  SH601162  2.29
4  2024-09-30 20:00:00  SZ000665  SZ000595  2.01
5  2024-09-30 20:00:00  SZ000665  SZ002717  1.72
6  2024-09-30 20:00:00  SZ000665  SZ300085  1.72
7  2024-09-30 20:00:00  SZ000665  SZ301551  1.59
8  2024-09-30 20:00:00  SZ000665  SZ000002  1.54
9  2024-09-30 20:00:00  SZ000665  SZ000980  1.50
```
