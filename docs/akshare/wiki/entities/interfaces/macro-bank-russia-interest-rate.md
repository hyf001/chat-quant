---
title: "macro_bank_russia_interest_rate - 俄罗斯利率决议报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, interest-rate, parameters, returns, example]
sources: [raw/data-dictionary/interest_rate/interest_rate.md]
confidence: high
---
# macro_bank_russia_interest_rate

- 分类: [[interest-rate-interest-rate|AKShare 利率数据]]
- 主题路径: AKShare 利率数据 > 主要央行利率 > 俄罗斯利率决议报告
- 描述: 俄罗斯利率决议报告, 数据区间从 20030601-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_russia_interest_rate_decision
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/interest_rate/interest_rate.html

## 相关

- [[interest-rate-interest-rate|AKShare 利率数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 俄罗斯利率决议报告

接口: macro_bank_russia_interest_rate

目标地址: https://datacenter.jin10.com/reportType/dc_russia_interest_rate_decision

描述: 俄罗斯利率决议报告, 数据区间从 20030601-至今

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

macro_bank_russia_interest_rate_df = ak.macro_bank_russia_interest_rate()
print(macro_bank_russia_interest_rate_df)
```

数据示例

```
            商品          日期    今值   预测值    前值
0    俄罗斯央行决议报告  2003-06-01   6.5   NaN   NaN
1    俄罗斯央行决议报告  2003-07-01   6.5   NaN   6.5
2    俄罗斯央行决议报告  2003-08-01   6.5   NaN   6.5
3    俄罗斯央行决议报告  2003-09-01   6.5   NaN   6.5
4    俄罗斯央行决议报告  2003-10-01   6.5   NaN   6.5
..         ...         ...   ...   ...   ...
214  俄罗斯央行决议报告  2024-04-26  16.0  16.0  16.0
215  俄罗斯央行决议报告  2024-06-07  16.0  16.0  16.0
216  俄罗斯央行决议报告  2024-07-26  18.0  18.0  16.0
217  俄罗斯央行决议报告  2024-09-13  19.0  18.0  18.0
218  俄罗斯央行决议报告  2024-10-25  21.0  20.0  19.0
[219 rows x 5 columns]
```
