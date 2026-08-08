---
title: "macro_bank_euro_interest_rate - 欧洲央行决议报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, interest-rate, parameters, returns, example]
sources: [raw/data-dictionary/interest_rate/interest_rate.md]
confidence: high
---
# macro_bank_euro_interest_rate

- 分类: [[interest-rate-interest-rate|AKShare 利率数据]]
- 主题路径: AKShare 利率数据 > 主要央行利率 > 欧洲央行决议报告
- 描述: 欧洲央行决议报告, 数据区间从 19990101-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_interest_rate_decision
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/interest_rate/interest_rate.html

## 相关

- [[interest-rate-interest-rate|AKShare 利率数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 欧洲央行决议报告

接口: macro_bank_euro_interest_rate

目标地址: https://datacenter.jin10.com/reportType/dc_interest_rate_decision

描述: 欧洲央行决议报告, 数据区间从 19990101-至今

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

macro_bank_euro_interest_rate_df = ak.macro_bank_euro_interest_rate()
print(macro_bank_euro_interest_rate_df)
```

数据示例

```
           商品          日期    今值   预测值    前值
0    欧洲央行决议报告  1999-01-01  3.00   NaN   NaN
1    欧洲央行决议报告  1999-02-01  3.00   NaN  3.00
2    欧洲央行决议报告  1999-03-01  3.00   NaN  3.00
3    欧洲央行决议报告  1999-04-01  3.00   NaN  3.00
4    欧洲央行决议报告  1999-05-01  2.50   NaN  3.00
..        ...         ...   ...   ...   ...
268  欧洲央行决议报告  2024-06-06  4.25  4.25  4.50
269  欧洲央行决议报告  2024-07-18  4.25  4.25  4.25
270  欧洲央行决议报告  2024-09-12  3.65  3.65  4.25
271  欧洲央行决议报告  2024-10-17  3.40  3.40  3.65
272  欧洲央行决议报告  2024-12-12   NaN   NaN   NaN
[273 rows x 5 columns]
```
