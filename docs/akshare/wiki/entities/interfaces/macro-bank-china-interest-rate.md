---
title: "macro_bank_china_interest_rate - 中国央行决议报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, interest-rate, parameters, returns, example]
sources: [raw/data-dictionary/interest_rate/interest_rate.md]
confidence: high
---
# macro_bank_china_interest_rate

- 分类: [[interest-rate-interest-rate|AKShare 利率数据]]
- 主题路径: AKShare 利率数据 > 主要央行利率 > 中国央行决议报告
- 描述: 中国央行决议报告, 数据区间从 19910105-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_china_interest_rate_decision
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/interest_rate/interest_rate.html

## 相关

- [[interest-rate-interest-rate|AKShare 利率数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 中国央行决议报告

接口: macro_bank_china_interest_rate

目标地址: https://datacenter.jin10.com/reportType/dc_china_interest_rate_decision

描述: 中国央行决议报告, 数据区间从 19910105-至今

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

macro_bank_china_interest_rate_df = ak.macro_bank_china_interest_rate()
print(macro_bank_china_interest_rate_df)
```

数据示例

```
           商品          日期    今值  预测值    前值
0    中国央行决议报告  1991-05-01  8.64  NaN   NaN
1    中国央行决议报告  1991-06-01  8.64  NaN  8.64
2    中国央行决议报告  1991-07-01  8.64  NaN  8.64
3    中国央行决议报告  1991-08-01  8.64  NaN  8.64
4    中国央行决议报告  1991-09-01  8.64  NaN  8.64
..        ...         ...   ...  ...   ...
213  中国央行决议报告  2015-08-25  4.60  NaN  4.85
214  中国央行决议报告  2015-10-23  4.35  NaN  4.60
215  中国央行决议报告  2019-09-20  4.20  NaN  4.25
216  中国央行决议报告  2019-10-21  4.20  NaN  4.20
217  中国央行决议报告  2019-11-20  4.15  4.2  4.20
[218 rows x 5 columns]
```
