---
title: "macro_usa_core_pce_price - 美国核心PCE物价指数年率报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_usa_core_pce_price

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 美国宏观 > 劳动力市场 > 消费者收入与支出 > 美国核心PCE物价指数年率报告
- 描述: 美国核心 PCE 物价指数年率报告, 数据区间从 19700101-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_usa_core_pce_price
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 美国核心PCE物价指数年率报告

接口: macro_usa_core_pce_price

目标地址: https://datacenter.jin10.com/reportType/dc_usa_core_pce_price

描述: 美国核心 PCE 物价指数年率报告, 数据区间从 19700101-至今

限量: 单次返回所有历史数据

说明: 当前接口使用 Jin10 历史数据接口; 经 2026-07 校验, 该上游链路未继续提供最新数据, 返回结果可能仅更新至 2025 年附近, 不代表 AKShare 本地缓存异常

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

macro_usa_core_pce_price_df = ak.macro_usa_core_pce_price()
print(macro_usa_core_pce_price_df)
```

数据示例

```
                商品          日期   今值  预测值   前值
0    美国核心PCE物价指数年率  1970-01-01  4.8  NaN  NaN
1    美国核心PCE物价指数年率  1970-02-01  4.7  NaN  4.8
2    美国核心PCE物价指数年率  1970-03-01  4.8  NaN  4.7
3    美国核心PCE物价指数年率  1970-04-01  4.7  NaN  4.8
4    美国核心PCE物价指数年率  1970-05-01  4.7  NaN  4.7
..             ...         ...  ...  ...  ...
649  美国核心PCE物价指数年率  2023-11-30  3.5  3.5  3.7
650  美国核心PCE物价指数年率  2023-12-22  3.2  3.3  3.4
651  美国核心PCE物价指数年率  2024-01-26  2.9  3.0  3.2
652  美国核心PCE物价指数年率  2024-02-29  2.8  2.8  2.9
653  美国核心PCE物价指数年率  2024-03-29  2.8  2.8  2.9
[654 rows x 5 columns]
```
