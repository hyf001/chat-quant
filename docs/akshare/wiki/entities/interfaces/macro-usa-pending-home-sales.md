---
title: "macro_usa_pending_home_sales - 美国成屋签约销售指数月率报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_usa_pending_home_sales

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 美国宏观 > 产业指标 > 房地产 > 美国成屋签约销售指数月率报告
- 描述: 美国成屋签约销售指数月率报告, 数据区间从 20010301-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_usa_pending_home_sales
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 美国成屋签约销售指数月率报告

接口: macro_usa_pending_home_sales

目标地址: https://datacenter.jin10.com/reportType/dc_usa_pending_home_sales

描述: 美国成屋签约销售指数月率报告, 数据区间从 20010301-至今

限量: 单次返回所有历史数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

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

macro_usa_pending_home_sales_df = ak.macro_usa_pending_home_sales()
print(macro_usa_pending_home_sales_df)
```

数据示例

```
                 商品          日期   今值  预测值   前值
0    美国成屋签约销售指数月率报告  2001-03-01  5.1  NaN  NaN
1    美国成屋签约销售指数月率报告  2001-04-01 -4.7  NaN  5.1
2    美国成屋签约销售指数月率报告  2001-05-01 -2.9  NaN -4.7
3    美国成屋签约销售指数月率报告  2001-06-01  2.7  NaN -2.9
4    美国成屋签约销售指数月率报告  2001-07-01 -3.4  NaN  2.7
..              ...         ...  ...  ...  ...
274  美国成屋签约销售指数月率报告  2023-12-28  0.0  1.0 -1.2
275  美国成屋签约销售指数月率报告  2024-01-26  8.3  1.5  0.0
276  美国成屋签约销售指数月率报告  2024-02-29 -4.9  1.4  5.7
277  美国成屋签约销售指数月率报告  2024-03-28  1.6  1.4 -4.7
278  美国成屋签约销售指数月率报告  2024-04-25  NaN  NaN  1.6
[279 rows x 5 columns]
```
