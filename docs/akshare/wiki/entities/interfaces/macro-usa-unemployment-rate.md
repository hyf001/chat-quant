---
title: "macro_usa_unemployment_rate - 美国失业率报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_usa_unemployment_rate

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 美国宏观 > 劳动力市场 > 失业率 > 美国失业率报告
- 描述: 美国失业率报告, 数据区间从 19700101-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_usa_unemployment_rate
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 美国失业率报告

接口: macro_usa_unemployment_rate

目标地址: https://datacenter.jin10.com/reportType/dc_usa_unemployment_rate

描述: 美国失业率报告, 数据区间从 19700101-至今

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

macro_usa_unemployment_rate_df = ak.macro_usa_unemployment_rate()
print(macro_usa_unemployment_rate_df)
```

数据示例

```
        商品          日期   今值  预测值   前值
0    美国失业率  1970-01-01  3.5  NaN  3.5
1    美国失业率  1970-02-01  3.9  NaN  3.5
2    美国失业率  1970-03-01  4.2  NaN  3.9
3    美国失业率  1970-04-01  4.4  NaN  4.2
4    美国失业率  1970-05-01  4.6  NaN  4.4
..     ...         ...  ...  ...  ...
647  美国失业率  2023-12-08  3.7  3.9  3.9
648  美国失业率  2024-01-05  3.7  3.8  3.7
649  美国失业率  2024-02-02  3.7  3.8  3.7
650  美国失业率  2024-03-08  3.9  3.7  3.7
651  美国失业率  2024-04-05  NaN  3.9  3.9
[652 rows x 5 columns]
```
