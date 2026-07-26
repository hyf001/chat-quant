---
title: "macro_usa_factory_orders - 美国工厂订单月率报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_usa_factory_orders

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 美国宏观 > 产业指标 > 工业 > 美国工厂订单月率报告
- 描述: 美国工厂订单月率报告, 数据区间从 19920401-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_usa_factory_orders
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 美国工厂订单月率报告

接口: macro_usa_factory_orders

目标地址: https://datacenter.jin10.com/reportType/dc_usa_factory_orders

描述: 美国工厂订单月率报告, 数据区间从 19920401-至今

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

macro_usa_factory_orders_df = ak.macro_usa_factory_orders()
print(macro_usa_factory_orders_df)
```

数据示例

```
             商品          日期   今值  预测值   前值
0    美国工厂订单月率报告  1992-04-01  4.6  NaN  NaN
1    美国工厂订单月率报告  1992-05-01  1.9  NaN  4.6
2    美国工厂订单月率报告  1992-06-01  1.6  NaN  1.9
3    美国工厂订单月率报告  1992-07-01 -0.5  NaN  1.6
4    美国工厂订单月率报告  1992-08-01 -0.9  NaN -0.5
..          ...         ...  ...  ...  ...
381  美国工厂订单月率报告  2023-12-04 -3.6 -2.8  2.3
382  美国工厂订单月率报告  2024-01-05  2.6  2.1 -3.4
383  美国工厂订单月率报告  2024-02-02  0.2  0.3  2.6
384  美国工厂订单月率报告  2024-03-05 -3.6 -3.1 -0.3
385  美国工厂订单月率报告  2024-04-02  1.4  1.1 -3.8
[386 rows x 5 columns]
```
