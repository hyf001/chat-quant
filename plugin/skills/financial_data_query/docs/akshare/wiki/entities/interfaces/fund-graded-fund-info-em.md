---
title: "fund_graded_fund_info_em - 分级基金-历史数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_graded_fund_info_em

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金净值 > 分级基金-历史数据
- 描述: 东方财富网站-天天基金网-基金数据-分级基金-历史数据
- 目标地址: http://fundf10.eastmoney.com/jjjz_004186.html
- 限量: 单次返回当前时刻所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 分级基金-历史数据

接口: fund_graded_fund_info_em

目标地址: http://fundf10.eastmoney.com/jjjz_004186.html

描述: 东方财富网站-天天基金网-基金数据-分级基金-历史数据

限量: 单次返回当前时刻所有历史数据

输入参数

| 名称     | 类型  | 描述                                                                    |
|--------|-----|-----------------------------------------------------------------------|
| symbol | str | symbol="150232"; 需要基金代码, 可以通过调用 **ak.fund_graded_fund_daily_em()** 获取 |

输出参数

| 名称   | 类型    | 描述                                                                       |
|------|-------|--------------------------------------------------------------------------|
| 净值日期 | str   | -                                                                        |
| 单位净值 | float | -                                                                        |
| 累计净值 | float | -                                                                        |
| 日增长率 | float | 注意单位: %; 日增长率为空原因如下: 1. 非交易日净值不参与日增长率计算(灰色数据行). 2. 上一交易日净值未披露, 日增长率无法计算. |
| 申购状态 | str   | -                                                                        |
| 赎回状态 | str   | -                                                                        |

接口示例

```python
import akshare as ak

fund_graded_fund_info_em_df = ak.fund_graded_fund_info_em(symbol="150232")
print(fund_graded_fund_info_em_df)
```

数据示例

```
      净值日期     单位净值 累计净值 日增长率 申购状态 赎回状态
0     2015-05-14  1.0000  1.0000   NaN  封闭期  封闭期
1     2015-05-15  0.9997  0.9997 -0.03  封闭期  封闭期
2     2015-05-18  0.9993  0.9993 -0.04  封闭期  封闭期
3     2015-05-19  0.9991  0.9991 -0.02  封闭期  封闭期
4     2015-05-20  0.9988  0.9988 -0.03  封闭期  封闭期
...          ...     ...     ...   ...  ...  ...
1338  2020-11-03  0.9749     NaN  1.72  封闭期  封闭期
1339  2020-11-04  0.9830     NaN  0.83  封闭期  封闭期
1340  2020-11-05  1.0235     NaN  4.12  封闭期  封闭期
1341  2020-11-06  1.0453     NaN  2.13  封闭期  封闭期
1342  2020-11-09  1.1120     NaN  6.38  封闭期  封闭期
[1343 rows x 6 columns]
```
