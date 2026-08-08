---
title: "macro_usa_api_crude_stock - 美国 API 原油库存报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_usa_api_crude_stock

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 美国宏观 > 产业指标 > 制造业 > 美国 API 原油库存报告
- 描述: 美国 API 原油库存报告, 数据区间从 20120328-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_usa_api_crude_stock
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 美国 API 原油库存报告

接口: macro_usa_api_crude_stock

目标地址: https://datacenter.jin10.com/reportType/dc_usa_api_crude_stock

描述: 美国 API 原油库存报告, 数据区间从 20120328-至今

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
| 今值  | float64 | 注意单位: 万桶 |
| 预测值 | float64 | 注意单位: 万桶 |
| 前值  | float64 | 注意单位: 万桶 |

接口示例

```python
import akshare as ak

macro_usa_api_crude_stock_df = ak.macro_usa_api_crude_stock()
print(macro_usa_api_crude_stock_df)
```

数据示例

```
            商品          日期     今值    预测值     前值
0    美国API原油库存  2012-03-28  360.0  277.0 -137.0
1    美国API原油库存  2012-04-04  785.0  221.0  360.0
2    美国API原油库存  2012-04-11  658.0  208.0  785.0
3    美国API原油库存  2012-04-18  341.0  157.0  658.0
4    美国API原油库存  2012-04-25  -99.0  293.0  341.0
..         ...         ...    ...    ...    ...
624  美国API原油库存  2024-03-13 -552.1   40.0   42.3
625  美国API原油库存  2024-03-20 -151.9    7.7 -552.1
626  美国API原油库存  2024-03-27  933.7    NaN -151.9
627  美国API原油库存  2024-04-03 -228.6 -200.0  933.7
628  美国API原油库存  2024-04-10    NaN    NaN -228.6
[629 rows x 5 columns]
```
