---
title: "stock_hot_rank_em - 人气榜-A股"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_hot_rank_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 股票热度 > 股票热度-东财 > 人气榜-A股
- 描述: 东方财富网站-股票热度
- 目标地址: http://guba.eastmoney.com/rank/
- 限量: 单次返回当前交易日前 100 个股票的人气排名数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 人气榜-A股

接口: stock_hot_rank_em

目标地址: http://guba.eastmoney.com/rank/

描述: 东方财富网站-股票热度

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
| 涨跌额  | float64 | -       |
| 涨跌幅  | float64 | 注意单位: % |

接口示例

```python
import akshare as ak

stock_hot_rank_em_df = ak.stock_hot_rank_em()
print(stock_hot_rank_em_df)
```

数据示例

```
    当前排名   代码  股票名称    最新价       涨跌额    涨跌幅
0      1  SZ002261  拓维信息  18.83  0.090384   0.48
1      2  SH603000   人民网  34.35  2.881965   8.39
2      3  SH601127   赛力斯  33.72  3.378744  10.02
3      4  SZ002229  鸿博股份  35.09  0.021054   0.06
4      5  SZ000936  华西股份  10.41  1.045164  10.04
..   ...       ...   ...    ...       ...    ...
95    96  SZ002585  双星新材   9.69  0.968031   9.99
96    97  SZ002670  国盛金控   8.46  0.520290   6.15
97    98  SZ300116   保力新   1.53  0.191250  12.50
98    99  SH603533  掌阅科技  33.14 -3.231150  -9.75
99   100  SZ301368  丰立智能  58.32  3.563352   6.11
[100 rows x 6 columns]
```
