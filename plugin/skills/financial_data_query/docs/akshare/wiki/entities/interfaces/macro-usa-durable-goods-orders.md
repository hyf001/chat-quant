---
title: "macro_usa_durable_goods_orders - 美国耐用品订单月率报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_usa_durable_goods_orders

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 美国宏观 > 产业指标 > 工业 > 美国耐用品订单月率报告
- 描述: 美国耐用品订单月率报告, 数据区间从 20080227-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_usa_durable_goods_orders
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 美国耐用品订单月率报告

接口: macro_usa_durable_goods_orders

目标地址: https://datacenter.jin10.com/reportType/dc_usa_durable_goods_orders

描述: 美国耐用品订单月率报告, 数据区间从 20080227-至今

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

macro_usa_durable_goods_orders_df = ak.macro_usa_durable_goods_orders()
print(macro_usa_durable_goods_orders_df)
```

数据示例

```
              商品          日期   今值  预测值   前值
0    美国耐用品订单月率报告  2008-02-27 -5.3 -4.0  5.0
1    美国耐用品订单月率报告  2008-03-26 -1.7  0.8 -5.3
2    美国耐用品订单月率报告  2008-04-24 -0.3  0.0 -1.1
3    美国耐用品订单月率报告  2008-05-28 -0.5 -1.5 -0.3
4    美国耐用品订单月率报告  2008-06-25  0.0  0.0 -0.6
..           ...         ...  ...  ...  ...
198  美国耐用品订单月率报告  2023-12-22  5.4  1.7 -5.1
199  美国耐用品订单月率报告  2024-01-25  0.0  1.1  5.5
200  美国耐用品订单月率报告  2024-02-27 -6.1 -4.9 -0.3
201  美国耐用品订单月率报告  2024-03-26  1.4  1.2 -6.9
202  美国耐用品订单月率报告  2024-04-24  NaN  NaN  1.3
[203 rows x 5 columns]
```
