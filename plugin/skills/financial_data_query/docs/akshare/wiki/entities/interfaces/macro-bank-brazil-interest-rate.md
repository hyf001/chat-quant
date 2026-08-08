---
title: "macro_bank_brazil_interest_rate - 巴西利率决议报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, interest-rate, parameters, returns, example]
sources: [raw/data-dictionary/interest_rate/interest_rate.md]
confidence: high
---
# macro_bank_brazil_interest_rate

- 分类: [[interest-rate-interest-rate|AKShare 利率数据]]
- 主题路径: AKShare 利率数据 > 主要央行利率 > 巴西利率决议报告
- 描述: 巴西利率决议报告, 数据区间从20080201-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_brazil_interest_rate_decision
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/interest_rate/interest_rate.html

## 相关

- [[interest-rate-interest-rate|AKShare 利率数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 巴西利率决议报告

接口: macro_bank_brazil_interest_rate

目标地址: https://datacenter.jin10.com/reportType/dc_brazil_interest_rate_decision

描述: 巴西利率决议报告, 数据区间从20080201-至今

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

macro_bank_brazil_interest_rate_df = ak.macro_bank_brazil_interest_rate()
print(macro_bank_brazil_interest_rate_df)
```

数据示例

```
           商品          日期     今值    预测值     前值
0    巴西央行决议报告  2008-02-01  11.25    NaN    NaN
1    巴西央行决议报告  2008-04-01  11.25    NaN  11.25
2    巴西央行决议报告  2008-05-01  11.75    NaN  11.25
3    巴西央行决议报告  2008-07-01  12.25    NaN  11.75
4    巴西央行决议报告  2008-08-01  13.00    NaN  12.25
..        ...         ...    ...    ...    ...
145  巴西央行决议报告  2024-06-20  10.50  10.50  10.50
146  巴西央行决议报告  2024-08-01  10.50  10.50  10.50
147  巴西央行决议报告  2024-09-19  10.75  10.75  10.50
148  巴西央行决议报告  2024-11-07    NaN  11.25  10.75
149  巴西央行决议报告  2024-12-12    NaN    NaN    NaN
[150 rows x 5 columns]
```
