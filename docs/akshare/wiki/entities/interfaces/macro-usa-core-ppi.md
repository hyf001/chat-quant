---
title: "macro_usa_core_ppi - 美国核心生产者物价指数(PPI)报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_usa_core_ppi

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 美国宏观 > 产业指标 > 制造业 > 美国核心生产者物价指数(PPI)报告
- 描述: 美国核心生产者物价指数(PPI)报告, 数据区间从 20080318-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_usa_core_ppi
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 美国核心生产者物价指数(PPI)报告

接口: macro_usa_core_ppi

目标地址: https://datacenter.jin10.com/reportType/dc_usa_core_ppi

描述: 美国核心生产者物价指数(PPI)报告, 数据区间从 20080318-至今

限量: 单次返回所有历史数据

输入参数

| 名称 | 类型   | 描述 |
|----|------|----|
| -  | -  - |

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

macro_usa_core_ppi_df = ak.macro_usa_core_ppi()
print(macro_usa_core_ppi_df)
```

数据示例

```
              商品          日期   今值  预测值   前值
0    美国核心生产者物价指数  2008-03-18  0.5  0.2  0.4
1    美国核心生产者物价指数  2008-04-15  0.2  0.2  0.5
2    美国核心生产者物价指数  2008-05-20  0.4  0.2  0.2
3    美国核心生产者物价指数  2008-06-17  0.2  0.2  0.4
4    美国核心生产者物价指数  2008-08-19  0.7  0.2  0.2
..           ...         ...  ...  ...  ...
188  美国核心生产者物价指数  2023-12-13  0.0  0.2  0.0
189  美国核心生产者物价指数  2024-01-12  0.0  0.2  0.0
190  美国核心生产者物价指数  2024-02-16  0.5  0.1 -0.1
191  美国核心生产者物价指数  2024-03-14  0.3  0.2  0.5
192  美国核心生产者物价指数  2024-04-11  NaN  0.2  0.3
[193 rows x 5 columns]
```
