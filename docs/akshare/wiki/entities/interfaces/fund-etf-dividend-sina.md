---
title: "fund_etf_dividend_sina - 基金累计分红"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_etf_dividend_sina

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 分红送配 > 基金累计分红
- 描述: 新浪财经-基金-ETF 基金-累计分红
- 目标地址: https://finance.sina.com.cn/fund/quotes/510050/bc.shtml
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 基金累计分红

接口: fund_etf_dividend_sina

目标地址: https://finance.sina.com.cn/fund/quotes/510050/bc.shtml

描述: 新浪财经-基金-ETF 基金-累计分红

限量: 单次返回所有历史数据

输入参数

| 名称     | 类型  | 描述                |
|--------|-----|-------------------|
| symbol | str | symbol="sh510050" |

输出参数

| 名称   | 类型      | 描述    |
|------|---------|-------|
| 日期   | object  | 除权除息日 |
| 累计分红 | float64 | -     |

接口示例

```python
import akshare as ak

fund_etf_dividend_sina_df = ak.fund_etf_dividend_sina(symbol="sh510050")
print(fund_etf_dividend_sina_df)
```

数据示例

```
           日期   累计分红
0  2006-05-19  0.024
1  2006-11-16  0.061
2  2008-11-19  0.121
3  2010-11-16  0.147
4  2012-05-16  0.158
5  2012-11-13  0.195
6  2013-11-15  0.248
7  2014-11-17  0.291
8  2016-11-29  0.344
9  2017-11-28  0.398
10 2018-12-03  0.447
11 2019-12-02  0.494
12 2020-11-30  0.545
13 2021-11-29  0.586
14 2022-12-01  0.623
15 2023-11-27  0.662
16 2024-12-02  0.717
```
