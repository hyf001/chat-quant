---
title: "macro_usa_house_starts - 美国新屋开工总数年化报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_usa_house_starts

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 美国宏观 > 产业指标 > 房地产 > 美国新屋开工总数年化报告
- 描述: 美国新屋开工总数年化报告, 数据区间从 19700101-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_usa_house_starts
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 美国新屋开工总数年化报告

接口: macro_usa_house_starts

目标地址: https://datacenter.jin10.com/reportType/dc_usa_house_starts

描述: 美国新屋开工总数年化报告, 数据区间从 19700101-至今

限量: 单次返回所有历史数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称  | 类型      | 描述       |
|-----|---------|----------|
| 商品  | object  | -        |
| 日期  | object  | -        |
| 今值  | float64 | 注意单位: 万户 |
| 预测值 | float64 | 注意单位: 万户 |
| 前值  | float64 | 注意单位: 万户 |

接口示例

```python
import akshare as ak

macro_usa_house_starts_df = ak.macro_usa_house_starts()
print(macro_usa_house_starts_df)
```

数据示例

```
               商品          日期     今值    预测值     前值
0    美国新屋开工总数年化报告  1970-01-01  133.0    NaN    NaN
1    美国新屋开工总数年化报告  1970-02-01  109.0    NaN  133.0
2    美国新屋开工总数年化报告  1970-03-01  131.0    NaN  109.0
3    美国新屋开工总数年化报告  1970-04-01  132.0    NaN  131.0
4    美国新屋开工总数年化报告  1970-05-01  126.0    NaN  132.0
..            ...         ...    ...    ...    ...
645  美国新屋开工总数年化报告  2023-12-19  156.0  136.0  135.9
646  美国新屋开工总数年化报告  2024-01-18  146.0  142.6  152.5
647  美国新屋开工总数年化报告  2024-02-16  133.1  145.0  156.2
648  美国新屋开工总数年化报告  2024-03-19  152.1  143.0  137.4
649  美国新屋开工总数年化报告  2024-04-16    NaN    NaN  152.1
[650 rows x 5 columns]
```
