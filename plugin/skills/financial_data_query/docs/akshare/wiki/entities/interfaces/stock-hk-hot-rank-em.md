---
title: "stock_hk_hot_rank_em - 人气榜-港股"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_hk_hot_rank_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 股票热度 > 股票热度-东财 > 人气榜-港股
- 描述: 东方财富-个股人气榜-人气榜-港股市场
- 目标地址: https://guba.eastmoney.com/rank/
- 限量: 单次返回当前交易日前 100 个股票的人气排名数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 人气榜-港股

接口: stock_hk_hot_rank_em

目标地址: https://guba.eastmoney.com/rank/

描述: 东方财富-个股人气榜-人气榜-港股市场

限量: 单次返回当前交易日前 100 个股票的人气排名数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称   | 类型      | 描述      |
|------|---------|---------|
| 当前排名 | int64   | -       |
| 代码   | object  | -       |
| 股票名称 | object  | -       |
| 最新价  | float64 | -       |
| 涨跌幅  | float64 | 注意单位: % |

接口示例

```python
import akshare as ak

stock_hk_hot_rank_em_df = ak.stock_hk_hot_rank_em()
print(stock_hk_hot_rank_em_df)
```

数据示例

```
    当前排名     代码    股票名称      最新价   涨跌幅
0      1  00700    腾讯控股  376.800  0.32
1      2  01810  小米集团-W   12.440  1.80
2      3  02158    医渡科技    8.350  3.73
3      4  03690    美团-W  140.200 -0.64
4      5  09955    智云健康    7.880  4.51
..   ...    ...     ...      ...   ...
95    96  01951    锦欣生殖    5.380 -1.28
96    97  01898    中煤能源    5.910 -8.51
97    98  02768  佳源国际控股    0.179 -2.19
98    99  00388   香港交易所  342.000  0.00
99   100  01816   中广核电力    1.900 -1.55
```
