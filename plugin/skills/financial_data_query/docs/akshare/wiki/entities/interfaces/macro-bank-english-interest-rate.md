---
title: "macro_bank_english_interest_rate - 英国央行决议报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, interest-rate, parameters, returns, example]
sources: [raw/data-dictionary/interest_rate/interest_rate.md]
confidence: high
---
# macro_bank_english_interest_rate

- 分类: [[interest-rate-interest-rate|AKShare 利率数据]]
- 主题路径: AKShare 利率数据 > 主要央行利率 > 英国央行决议报告
- 描述: 英国央行决议报告, 数据区间从 19700101-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_english_interest_rate_decision
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/interest_rate/interest_rate.html

## 相关

- [[interest-rate-interest-rate|AKShare 利率数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 英国央行决议报告

接口: macro_bank_english_interest_rate

目标地址: https://datacenter.jin10.com/reportType/dc_english_interest_rate_decision

描述: 英国央行决议报告, 数据区间从 19700101-至今

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

macro_bank_english_interest_rate_df = ak.macro_bank_english_interest_rate()
print(macro_bank_english_interest_rate_df)
```

数据示例

```
           商品          日期    今值   预测值    前值
0    英国央行决议报告  1970-01-01  8.00   NaN   NaN
1    英国央行决议报告  1970-02-01  8.00   NaN  8.00
2    英国央行决议报告  1970-03-01  8.00   NaN  8.00
3    英国央行决议报告  1970-04-01  7.50   NaN  8.00
4    英国央行决议报告  1970-05-01  7.00   NaN  7.50
..        ...         ...   ...   ...   ...
627  英国央行决议报告  2024-06-20  5.25  5.25  5.25
628  英国央行决议报告  2024-08-01  5.00  5.00  5.25
629  英国央行决议报告  2024-09-19  5.00  5.00  5.00
630  英国央行决议报告  2024-11-07   NaN  4.75  5.00
631  英国央行决议报告  2024-12-19   NaN   NaN   NaN
[632 rows x 5 columns]
```
