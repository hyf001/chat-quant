---
title: "macro_usa_new_home_sales - 美国新屋销售总数年化报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_usa_new_home_sales

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 美国宏观 > 产业指标 > 房地产 > 美国新屋销售总数年化报告
- 描述: 美国新屋销售总数年化报告, 数据区间从 19700101-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_usa_new_home_sales
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 美国新屋销售总数年化报告

接口: macro_usa_new_home_sales

目标地址: https://datacenter.jin10.com/reportType/dc_usa_new_home_sales

描述: 美国新屋销售总数年化报告, 数据区间从 19700101-至今

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

macro_usa_new_home_sales_df = ak.macro_usa_new_home_sales()
print(macro_usa_new_home_sales_df)
```

数据示例

```
               商品          日期    今值   预测值    前值
0    美国新屋销售总数年化报告  1970-01-01  45.2   NaN   NaN
1    美国新屋销售总数年化报告  1970-02-01  46.1   NaN  45.2
2    美国新屋销售总数年化报告  1970-03-01  37.3   NaN  46.1
3    美国新屋销售总数年化报告  1970-04-01  38.9   NaN  37.3
4    美国新屋销售总数年化报告  1970-05-01  44.5   NaN  38.9
..            ...         ...   ...   ...   ...
646  美国新屋销售总数年化报告  2023-12-22  59.0  69.5  67.2
647  美国新屋销售总数年化报告  2024-01-25  66.4  64.5  61.5
648  美国新屋销售总数年化报告  2024-02-26  66.1  68.0  65.1
649  美国新屋销售总数年化报告  2024-03-25  66.2  67.5  66.4
650  美国新屋销售总数年化报告  2024-04-23   NaN   NaN  66.2
[651 rows x 5 columns]
```
