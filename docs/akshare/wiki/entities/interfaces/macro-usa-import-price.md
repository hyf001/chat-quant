---
title: "macro_usa_import_price - 美国进口物价指数报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_usa_import_price

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 美国宏观 > 物价水平 > 美国进口物价指数报告
- 描述: 美国进口物价指数报告, 数据区间从 19890201-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_usa_import_price
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 美国进口物价指数报告

接口: macro_usa_import_price

目标地址: https://datacenter.jin10.com/reportType/dc_usa_import_price

描述: 美国进口物价指数报告, 数据区间从 19890201-至今

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

macro_usa_import_price_df = ak.macro_usa_import_price()
print(macro_usa_import_price_df)
```

数据示例

```
           商品          日期   今值  预测值   前值
0    美国进口物价指数  1989-02-01  2.0  NaN  NaN
1    美国进口物价指数  1989-03-01 -0.5  NaN  2.0
2    美国进口物价指数  1989-04-01  0.8  NaN -0.5
3    美国进口物价指数  1989-05-01  0.8  NaN  0.8
4    美国进口物价指数  1989-06-01  0.7  NaN  0.8
..        ...         ...  ...  ...  ...
420  美国进口物价指数  2023-12-14 -0.4 -0.8 -0.6
421  美国进口物价指数  2024-01-17  0.0 -0.5 -0.5
422  美国进口物价指数  2024-02-15  0.8  0.0 -0.7
423  美国进口物价指数  2024-03-15  0.3  0.3  0.8
424  美国进口物价指数  2024-04-12  NaN  0.2  0.3
[425 rows x 5 columns]
```
