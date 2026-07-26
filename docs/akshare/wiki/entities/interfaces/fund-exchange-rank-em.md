---
title: "fund_exchange_rank_em - 场内交易基金排行榜"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_exchange_rank_em

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金排行 > 场内交易基金排行榜
- 描述: 东方财富网-数据中心-场内交易基金排行榜
- 目标地址: https://fund.eastmoney.com/data/fbsfundranking.html
- 限量: 单次返回当前时刻所有数据, 每个交易日 17 点后更新
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 场内交易基金排行榜

接口: fund_exchange_rank_em

目标地址: https://fund.eastmoney.com/data/fbsfundranking.html

描述: 东方财富网-数据中心-场内交易基金排行榜

限量: 单次返回当前时刻所有数据, 每个交易日 17 点后更新

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称   | 类型      | 描述      |
|------|---------|---------|
| 序号   | int64   | -       |
| 基金代码 | object  | -       |
| 基金简称 | object  | -       |
| 类型   | object  | -       |
| 日期   | object  | -       |
| 单位净值 | float64 | -       |
| 累计净值 | float64 | -       |
| 近1周  | float64 | 注意单位: % |
| 近1月  | float64 | 注意单位: % |
| 近3月  | float64 | 注意单位: % |
| 近6月  | float64 | 注意单位: % |
| 近1年  | float64 | 注意单位: % |
| 近2年  | float64 | 注意单位: % |
| 近3年  | float64 | 注意单位: % |
| 今年来  | float64 | 注意单位: % |
| 成立来  | float64 | 注意单位: % |
| 成立日期 | object  | -       |

接口示例

```python
import akshare as ak

fund_exchange_rank_em_df = ak.fund_exchange_rank_em()
print(fund_exchange_rank_em_df)
```

数据示例

```
      序号    基金代码                基金简称  ...    今年来     成立来        成立日期
0      1  513300  华夏纳斯达克100ETF(QDII)  ...   8.31   62.36  2020-10-22
1      2  159632  华安纳斯达克100ETF(QDII)  ...   6.52   46.67  2022-07-21
2      3  513100        国泰纳斯达克100ETF  ...   7.14  545.00  2013-04-25
3      4  159941        广发纳斯达克100ETF  ...   7.07  288.28  2015-06-10
4      5  513520        华夏野村日经225ETF  ...  11.69   42.39  2019-06-12
..   ...     ...                 ...  ...    ...     ...         ...
875  876  159573       华夏创业板中盘200ETF  ... -15.70  -15.30  2023-12-15
876  877  159577      汇添富MSCI美国50ETF  ...    NaN    0.13  2024-02-05
877  878  159549     天弘中证红利低波动100ETF  ...   3.48    2.38  2023-11-23
878  879  159562    华夏中证沪深港黄金产业股票ETF  ...    NaN    3.62  2024-01-11
879  880  560300        汇添富中证电信主题ETF  ...   4.35    2.64  2023-12-05
[880 rows x 17 columns]
```
