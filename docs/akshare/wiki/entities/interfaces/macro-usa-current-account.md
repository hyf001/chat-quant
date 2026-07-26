---
title: "macro_usa_current_account - 美国经常帐报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_usa_current_account

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 美国宏观 > 贸易状况 > 美国经常帐报告
- 描述: 美国经常帐报告, 数据区间从 20080317-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_usa_current_account
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 美国经常帐报告

接口: macro_usa_current_account

目标地址: https://datacenter.jin10.com/reportType/dc_usa_current_account

描述: 美国经常帐报告, 数据区间从 20080317-至今

限量: 单次返回所有历史数据

输入参数

| 名称 | 类型   | 描述 |
|----|------|----|
| -  | -  - |

输出参数

| 名称  | 类型      | 描述        |
|-----|---------|-----------|
| 商品  | object  | -         |
| 日期  | object  | -         |
| 今值  | float64 | 注意单位: 亿美元 |
| 预测值 | float64 | 注意单位: 亿美元 |
| 前值  | float64 | 注意单位: 亿美元 |

接口示例

```python
import akshare as ak

macro_usa_current_account_df = ak.macro_usa_current_account()
print(macro_usa_current_account_df)
```

数据示例

```
         商品          日期    今值     预测值    前值
0   美国经常账报告  2008-03-17 -1730 -1840.0 -1790
1   美国经常账报告  2008-06-17 -1760     NaN -1730
2   美国经常账报告  2008-09-17 -1830 -1800.0 -1760
3   美国经常账报告  2008-12-17 -1740 -1800.0 -1830
4   美国经常账报告  2009-03-18 -1330 -1370.0 -1740
..      ...         ...   ...     ...   ...
60  美国经常账报告  2023-03-23 -2068 -2132.0 -2190
61  美国经常账报告  2023-06-22 -2193 -2169.0 -2162
62  美国经常账报告  2023-09-21 -2121 -2210.0 -2145
63  美国经常账报告  2023-12-20 -2003 -1970.0 -2168
64  美国经常账报告  2024-03-21 -1948 -2090.0 -1964
[65 rows x 5 columns]
```
