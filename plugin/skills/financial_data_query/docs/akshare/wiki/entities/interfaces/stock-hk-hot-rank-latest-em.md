---
title: "stock_hk_hot_rank_latest_em - 港股"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_hk_hot_rank_latest_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 股票热度 > 个股人气榜-最新排名 > 港股
- 描述: 东方财富-个股人气榜-最新排名
- 目标地址: https://guba.eastmoney.com/rank/stock?code=HK_00700
- 限量: 单次返回指定 symbol 的股票近期历史数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 港股

接口: stock_hk_hot_rank_latest_em

目标地址: https://guba.eastmoney.com/rank/stock?code=HK_00700

描述: 东方财富-个股人气榜-最新排名

限量: 单次返回指定 symbol 的股票近期历史数据

输入参数

| 名称     | 类型  | 描述             |
|--------|-----|----------------|
| symbol | str | symbol="00700" |

输出参数

| 名称    | 类型     | 描述  |
|-------|--------|-----|
| item  | object | -   |
| value | object | -   |

接口示例

```python
import akshare as ak

stock_hk_hot_rank_latest_em_df = ak.stock_hk_hot_rank_latest_em(symbol="00700")
print(stock_hk_hot_rank_latest_em_df)
```

数据示例

```
                 item                value
0          marketType               000003
1      marketAllCount                 2613
2            calcTime  2023-03-25 23:30:00
3           innerCode              00700_2
4     srcSecurityCode             HK|00700
5                rank                    1
6          rankChange                    0
7       hisRankChange                    0
8  hisRankChange_rank                 1253
9                flag                    0
```
