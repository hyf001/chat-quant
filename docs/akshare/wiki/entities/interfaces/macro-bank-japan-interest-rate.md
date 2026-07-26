---
title: "macro_bank_japan_interest_rate - 日本利率决议报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, interest-rate, parameters, returns, example]
sources: [raw/data-dictionary/interest_rate/interest_rate.md]
confidence: high
---
# macro_bank_japan_interest_rate

- 分类: [[interest-rate-interest-rate|AKShare 利率数据]]
- 主题路径: AKShare 利率数据 > 主要央行利率 > 日本利率决议报告
- 描述: 日本利率决议报告, 数据区间从 20080214-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_japan_interest_rate_decision
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/interest_rate/interest_rate.html

## 相关

- [[interest-rate-interest-rate|AKShare 利率数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 日本利率决议报告

接口: macro_bank_japan_interest_rate

目标地址: https://datacenter.jin10.com/reportType/dc_japan_interest_rate_decision

描述: 日本利率决议报告, 数据区间从 20080214-至今

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

macro_bank_japan_interest_rate_df = ak.macro_bank_japan_interest_rate()
print(macro_bank_japan_interest_rate_df)
```

数据示例

```
           商品          日期    今值   预测值    前值
0    日本央行决议报告  2008-02-14  0.50  0.50  0.50
1    日本央行决议报告  2008-03-07  0.50  0.50  0.50
2    日本央行决议报告  2008-04-09  0.50  0.50  0.50
3    日本央行决议报告  2008-04-30  0.50  0.50  0.50
4    日本央行决议报告  2008-06-13  0.50  0.50  0.50
..        ...         ...   ...   ...   ...
190  日本央行决议报告  2024-06-14  0.10  0.10  0.10
191  日本央行决议报告  2024-07-31  0.25  0.10  0.10
192  日本央行决议报告  2024-09-20  0.25  0.25  0.25
193  日本央行决议报告  2024-10-31  0.25  0.25  0.25
194  日本央行决议报告  2024-12-19   NaN   NaN  0.25
[195 rows x 5 columns]
```
