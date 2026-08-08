---
title: "macro_china_lpr - LPR品种数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_lpr

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 国民经济运行状况 > 经济状况 > LPR品种数据
- 描述: 中国 LPR 品种数据, 数据区间从 19910421-至今
- 目标地址: https://data.eastmoney.com/cjsj/globalRateLPR.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

###### LPR品种数据

接口: macro_china_lpr

目标地址: https://data.eastmoney.com/cjsj/globalRateLPR.html

描述: 中国 LPR 品种数据, 数据区间从 19910421-至今

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称         | 类型      | 描述                  |
|------------|---------|---------------------|
| TRADE_DATE | object  | 日期                  |
| LPR1Y      | float64 | LPR_1Y利率(%)         |
| LPR5Y      | float64 | LPR_5Y利率(%)         |
| RATE_1     | float64 | 短期贷款利率:6个月至1年(含)(%) |
| RATE_2     | float64 | 中长期贷款利率:5年以上(%)     |

接口示例

```python
import akshare as ak

macro_china_lpr_df = ak.macro_china_lpr()
print(macro_china_lpr_df)
```

数据示例

```
      TRADE_DATE  LPR1Y  LPR5Y  RATE_1  RATE_2
0     1991-04-21    NaN    NaN    8.64    9.72
1     1993-05-15    NaN    NaN    9.36   12.24
2     1993-07-11    NaN    NaN   10.98   14.04
3     1995-01-01    NaN    NaN   10.98   14.76
4     1995-07-01    NaN    NaN   12.06   15.30
          ...    ...    ...     ...     ...
1533  2023-03-20   3.65    4.3    4.35    4.90
1534  2023-04-20   3.65    4.3    4.35    4.90
1535  2023-05-22   3.65    4.3    4.35    4.90
1536  2023-06-20   3.55    4.2    4.35    4.90
1537  2023-07-20   3.55    4.2    4.35    4.90
[1538 rows x 5 columns]
```
