---
title: "macro_usa_exist_home_sales - 美国成屋销售总数年化报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_usa_exist_home_sales

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 美国宏观 > 产业指标 > 房地产 > 美国成屋销售总数年化报告
- 描述: 美国成屋销售总数年化报告, 数据区间从 19700101-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_usa_exist_home_sales
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 美国成屋销售总数年化报告

接口: macro_usa_exist_home_sales

目标地址: https://datacenter.jin10.com/reportType/dc_usa_exist_home_sales

描述: 美国成屋销售总数年化报告, 数据区间从 19700101-至今

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

macro_usa_exist_home_sales_df = ak.macro_usa_exist_home_sales()
print(macro_usa_exist_home_sales_df)
```

数据示例

```
               商品          日期     今值    预测值     前值
0    美国成屋销售总数年化报告  1970-01-01  160.0    NaN    NaN
1    美国成屋销售总数年化报告  1970-02-01  153.0    NaN  160.0
2    美国成屋销售总数年化报告  1970-03-01  146.0    NaN  153.0
3    美国成屋销售总数年化报告  1970-04-01  137.0    NaN  146.0
4    美国成屋销售总数年化报告  1970-05-01  151.0    NaN  137.0
..            ...         ...    ...    ...    ...
647  美国成屋销售总数年化报告  2023-12-20  382.0  378.0  379.0
648  美国成屋销售总数年化报告  2024-01-19  378.0  382.0  382.0
649  美国成屋销售总数年化报告  2024-02-22  400.0  396.0  388.0
650  美国成屋销售总数年化报告  2024-03-21  438.0  395.0  400.0
651  美国成屋销售总数年化报告  2024-04-18    NaN    NaN  438.0
[652 rows x 5 columns]
```
