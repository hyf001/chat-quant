---
title: "fund_report_stock_cninfo - 基金重仓股"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_report_stock_cninfo

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金报告 > 基金重仓股
- 描述: 巨潮资讯-数据中心-专题统计-基金报表-基金重仓股
- 目标地址: https://webapi.cninfo.com.cn/#/thematicStatistics
- 限量: 返回指定 date 的所有数据; date 从 2017 年开始
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 基金重仓股

接口: fund_report_stock_cninfo

目标地址: https://webapi.cninfo.com.cn/#/thematicStatistics

描述: 巨潮资讯-数据中心-专题统计-基金报表-基金重仓股

限量: 返回指定 date 的所有数据; date 从 2017 年开始

输入参数

| 名称   | 类型  | 描述                                                                                       |
|------|-----|------------------------------------------------------------------------------------------|
| date | str | date="20210630"; choice of {"XXXX0331", "XXXX0630", "XXXX0930", "XXXX1231"}, 其中 XXXX 为年份 |

输出参数

| 名称     | 类型     | 描述  |
|--------|--------|-----|
| 序号     | int64  | -   |
| 股票代码   | object | -   |
| 股票简称   | object | -   |
| 报告期    | object | -   |
| 基金覆盖家数 | int64  | -   |
| 持股总数   | object | -   |
| 持股总市值  | object | -   |

接口示例

```python
import akshare as ak

fund_report_stock_cninfo_df = ak.fund_report_stock_cninfo(date="20210630")
print(fund_report_stock_cninfo_df)
```

数据示例

```
       序号  股票代码  股票简称   报告期  基金覆盖家数   持股总数  持股总市值
0        1  605011  杭州热电  2021-06-30    3722  1928625   1712.62
1        2  603171  税友股份  2021-06-30    3653  2289995   4396.79
2        3  001208  华菱线缆  2021-06-30    3593  6218772   4807.11
3        4  605287  德才股份  2021-06-30    3461  1200847   3789.87
4        5  601528  瑞丰银行  2021-06-30    3324  7284126  11341.38
...    ...     ...   ...         ...     ...      ...       ...
3951  3952  836239  长虹能源  2021-06-30       1   273070   1791.34
3952  3953  836675  秉扬科技  2021-06-30       1   477163    660.87
3953  3954  836826  盖世食品  2021-06-30       1  1731830   1087.59
3954  3955  837344  三元基因  2021-06-30       1   274142    610.79
3955  3956  839167  同享科技  2021-06-30       1   315074    667.96
```
