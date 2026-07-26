---
title: "macro_bank_australia_interest_rate - 澳洲联储决议报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, interest-rate, parameters, returns, example]
sources: [raw/data-dictionary/interest_rate/interest_rate.md]
confidence: high
---
# macro_bank_australia_interest_rate

- 分类: [[interest-rate-interest-rate|AKShare 利率数据]]
- 主题路径: AKShare 利率数据 > 主要央行利率 > 澳洲联储决议报告
- 描述: 澳洲联储决议报告, 数据区间从 19800201-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_australia_interest_rate_decision
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/interest_rate/interest_rate.html

## 相关

- [[interest-rate-interest-rate|AKShare 利率数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 澳洲联储决议报告

接口: macro_bank_australia_interest_rate

目标地址: https://datacenter.jin10.com/reportType/dc_australia_interest_rate_decision

描述: 澳洲联储决议报告, 数据区间从 19800201-至今

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称  | 类型      | 描述      |
|-----|---------|---------|
| 商品  | object  | -       |
| 日期  | object  | -       |
| 今值  | float64 | 注意单位: % |
| 预测值 | float64 | 注意单位: % |
| 前值  | float64 | 注意单位: % |

接口示例

```python
import akshare as ak

macro_bank_australia_interest_rate_df = ak.macro_bank_australia_interest_rate()
print(macro_bank_australia_interest_rate_df)
```

数据示例

```
           商品          日期     今值   预测值    前值
0    澳洲联储决议报告  1980-02-01   7.92   NaN   NaN
1    澳洲联储决议报告  1980-03-01   8.20   NaN  7.92
2    澳洲联储决议报告  1980-04-01   9.25   NaN  8.20
3    澳洲联储决议报告  1980-05-01   8.98   NaN  9.25
4    澳洲联储决议报告  1980-06-01  10.74   NaN  8.98
..        ...         ...    ...   ...   ...
517  澳洲联储决议报告  2024-06-18   4.35  4.35  4.35
518  澳洲联储决议报告  2024-08-06   4.35  4.35  4.35
519  澳洲联储决议报告  2024-09-24   4.35  4.35  4.35
520  澳洲联储决议报告  2024-11-05   4.35  4.35  4.35
521  澳洲联储决议报告  2024-12-10    NaN   NaN   NaN
[522 rows x 5 columns]
```
