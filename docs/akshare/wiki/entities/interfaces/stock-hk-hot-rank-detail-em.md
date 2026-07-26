---
title: "stock_hk_hot_rank_detail_em - 港股"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_hk_hot_rank_detail_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 股票热度 > 历史趋势及粉丝特征 > 港股
- 描述: 东方财富网-股票热度-历史趋势
- 目标地址: https://guba.eastmoney.com/rank/stock?code=HK_00700
- 限量: 单次返回指定 symbol 的股票近期历史数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 港股

接口: stock_hk_hot_rank_detail_em

目标地址: https://guba.eastmoney.com/rank/stock?code=HK_00700

描述: 东方财富网-股票热度-历史趋势

限量: 单次返回指定 symbol 的股票近期历史数据

输入参数

| 名称     | 类型  | 描述             |
|--------|-----|----------------|
| symbol | str | symbol="00700" |

输出参数

| 名称   | 类型      | 描述  |
|------|---------|-----|
| 时间   | object  | -   |
| 排名   | int64   | -   |
| 证券代码 | object  | -   |

接口示例

```python
import akshare as ak

stock_hk_hot_rank_detail_em_df = ak.stock_hk_hot_rank_detail_em(symbol="00700")
print(stock_hk_hot_rank_detail_em_df)
```

数据示例

```
      时间    排名   证券代码
0    2022-11-26   1  00700
1    2022-11-27   2  00700
2    2022-11-28   1  00700
3    2022-11-29   1  00700
4    2022-11-30   1  00700
..          ...  ..    ...
115  2023-03-21   1  00700
116  2023-03-22   1  00700
117  2023-03-23   1  00700
118  2023-03-24   1  00700
119  2023-03-25   1  00700
```
