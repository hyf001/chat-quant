---
title: "macro_usa_house_price_index - 美国FHFA房价指数月率报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_usa_house_price_index

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 美国宏观 > 产业指标 > 房地产 > 美国FHFA房价指数月率报告
- 描述: 美国 FHFA 房价指数月率报告, 数据区间从 19910301-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_usa_house_price_index
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 美国FHFA房价指数月率报告

接口: macro_usa_house_price_index

目标地址: https://datacenter.jin10.com/reportType/dc_usa_house_price_index

描述: 美国 FHFA 房价指数月率报告, 数据区间从 19910301-至今

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

macro_usa_house_price_index_df = ak.macro_usa_house_price_index()
print(macro_usa_house_price_index_df)
```

数据示例

```
                 商品          日期   今值  预测值   前值
0    美国FHFA房价指数月率报告  1991-03-01  0.5  NaN  NaN
1    美国FHFA房价指数月率报告  1991-04-01  0.0  NaN  0.5
2    美国FHFA房价指数月率报告  1991-05-01 -0.2  NaN  0.0
3    美国FHFA房价指数月率报告  1991-06-01  0.1  NaN -0.2
4    美国FHFA房价指数月率报告  1991-07-01  0.1  NaN  0.1
..              ...         ...  ...  ...  ...
392  美国FHFA房价指数月率报告  2023-11-28  0.6  0.4  0.7
393  美国FHFA房价指数月率报告  2023-12-26  0.3  0.5  0.7
394  美国FHFA房价指数月率报告  2024-01-30  0.3  0.2  0.3
395  美国FHFA房价指数月率报告  2024-02-27  0.1  0.3  0.4
396  美国FHFA房价指数月率报告  2024-03-26 -0.1  0.2  0.1
[397 rows x 5 columns]
```
