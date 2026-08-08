---
title: "macro_bank_india_interest_rate - 印度利率决议报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, interest-rate, parameters, returns, example]
sources: [raw/data-dictionary/interest_rate/interest_rate.md]
confidence: high
---
# macro_bank_india_interest_rate

- 分类: [[interest-rate-interest-rate|AKShare 利率数据]]
- 主题路径: AKShare 利率数据 > 主要央行利率 > 印度利率决议报告
- 描述: 印度利率决议报告, 数据区间从 20000801-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_india_interest_rate_decision
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/interest_rate/interest_rate.html

## 相关

- [[interest-rate-interest-rate|AKShare 利率数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 印度利率决议报告

接口: macro_bank_india_interest_rate

目标地址: https://datacenter.jin10.com/reportType/dc_india_interest_rate_decision

描述: 印度利率决议报告, 数据区间从 20000801-至今

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

macro_bank_india_interest_rate_df = ak.macro_bank_india_interest_rate()
print(macro_bank_india_interest_rate_df)
```

数据示例

```
           商品          日期     今值  预测值     前值
0    印度央行决议报告  2000-08-01   7.38  NaN    NaN
1    印度央行决议报告  2000-09-01  13.35  NaN   7.38
2    印度央行决议报告  2000-10-01  10.52  NaN  13.35
3    印度央行决议报告  2000-11-01   8.61  NaN  10.52
4    印度央行决议报告  2000-12-01   8.00  NaN   8.61
..        ...         ...    ...  ...    ...
222  印度央行决议报告  2024-02-08   6.50  6.5   6.50
223  印度央行决议报告  2024-04-05   6.50  6.5   6.50
224  印度央行决议报告  2024-06-07   6.50  6.5   6.50
225  印度央行决议报告  2024-08-08   6.50  6.5   6.50
226  印度央行决议报告  2024-10-09   6.50  6.5   6.50
[227 rows x 5 columns]
```
