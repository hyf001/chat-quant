---
title: "stock_hot_up_em - 飙升榜-A股"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_hot_up_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 股票热度 > 股票热度-东财 > 飙升榜-A股
- 描述: 东方财富-个股人气榜-飙升榜
- 目标地址: http://guba.eastmoney.com/rank/
- 限量: 单次返回当前交易日前 100 个股票的飙升榜排名数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 飙升榜-A股

接口: stock_hot_up_em

目标地址: http://guba.eastmoney.com/rank/

描述: 东方财富-个股人气榜-飙升榜

限量: 单次返回当前交易日前 100 个股票的飙升榜排名数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称      | 类型      | 描述      |
|---------|---------|---------|
| 排名较昨日变动 | int64   | -       |
| 当前排名    | int64   | -       |
| 代码      | object  | -       |
| 股票名称    | object  | -       |
| 最新价     | float64 | -       |
| 涨跌额     | float64 | -       |
| 涨跌幅     | float64 | 注意单位: % |

接口示例

```python
import akshare as ak

stock_hot_up_em_df = ak.stock_hot_up_em()
print(stock_hot_up_em_df)
```

数据示例

```
    排名较昨日变动  当前排名    代码  股票名称   最新价  涨跌额    涨跌幅
0      4491   484  SH688226  威腾电气  18.89  2.349916  12.44
1      4240   454  SZ301079  邵阳液压  19.42  1.648758   8.49
2      4029   645  SH688698  伟创电气  31.45  2.858805   9.09
3      4023   366  SZ002523  天桥起重   2.87  0.180810   6.30
4      4019   568  SZ300402  宝色股份  20.50  1.377600   6.72
..      ...   ...       ...   ...    ...       ...    ...
95     2261   504  SZ000795   英洛华   6.31  0.217064   3.44
96     2253  2816  SZ430425  乐创技术  13.78  0.826800   6.00
97     2234  1515  SZ300861  美畅股份  41.60  2.025920   4.87
98     2230   367  SH688003  天准科技  46.06  4.900784  10.64
99     2230  2825  SZ835985  海泰新能   6.56  0.217136   3.31
[100 rows x 7 columns]
```
