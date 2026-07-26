---
title: "macro_usa_business_inventories - 美国商业库存月率报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_usa_business_inventories

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 美国宏观 > 产业指标 > 服务业 > 美国商业库存月率报告
- 描述: 美国商业库存月率报告, 数据区间从 19920301-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_usa_business_inventories
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 美国商业库存月率报告

接口: macro_usa_business_inventories

目标地址: https://datacenter.jin10.com/reportType/dc_usa_business_inventories

描述: 美国商业库存月率报告, 数据区间从 19920301-至今

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

macro_usa_business_inventories_df = ak.macro_usa_business_inventories()
print(macro_usa_business_inventories_df)
```

数据示例

```
             商品          日期   今值  预测值   前值
0    美国商业库存月率报告  1992-03-01  0.2  NaN  NaN
1    美国商业库存月率报告  1992-04-01  0.4  NaN  0.2
2    美国商业库存月率报告  1992-05-01  0.3  NaN  0.4
3    美国商业库存月率报告  1992-06-01 -0.1  NaN  0.3
4    美国商业库存月率报告  1992-07-01  0.7  NaN -0.1
..          ...         ...  ...  ...  ...
381  美国商业库存月率报告  2023-12-14 -0.1  0.0  0.2
382  美国商业库存月率报告  2024-01-17 -0.1 -0.1 -0.1
383  美国商业库存月率报告  2024-02-15  0.4  0.4 -0.1
384  美国商业库存月率报告  2024-03-14  0.0  0.2  0.3
385  美国商业库存月率报告  2024-04-15  NaN  NaN  0.3
[386 rows x 5 columns]
```
