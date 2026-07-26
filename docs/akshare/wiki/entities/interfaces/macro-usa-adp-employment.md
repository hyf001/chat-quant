---
title: "macro_usa_adp_employment - 美国ADP就业人数报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_usa_adp_employment

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 美国宏观 > 劳动力市场 > 就业人口 > 美国ADP就业人数报告
- 描述: 美国 ADP 就业人数报告, 数据区间从 20010601-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_adp_nonfarm_employment
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 美国ADP就业人数报告

接口: macro_usa_adp_employment

目标地址: https://datacenter.jin10.com/reportType/dc_adp_nonfarm_employment

描述: 美国 ADP 就业人数报告, 数据区间从 20010601-至今

限量: 单次返回所有历史数据

输入参数

| 名称 | 类型   | 描述 |
|----|------|----|
| -  | -  - |

输出参数

| 名称  | 类型      | 描述       |
|-----|---------|----------|
| 商品  | object  | -        |
| 日期  | object  | -        |
| 今值  | float64 | 注意单位: 万人 |
| 预测值 | float64 | 注意单位: 万人 |
| 前值  | float64 | 注意单位: 万人 |

接口示例

```python
import akshare as ak

macro_usa_adp_employment_df = ak.macro_usa_adp_employment()
print(macro_usa_adp_employment_df)
```

数据示例

```
            商品          日期    今值   预测值    前值
0    美国ADP就业人数  2001-06-01 -17.5   NaN   NaN
1    美国ADP就业人数  2001-07-01 -23.0   NaN -17.5
2    美国ADP就业人数  2001-08-01 -20.3   NaN -23.0
3    美国ADP就业人数  2001-09-01 -24.6   NaN -20.3
4    美国ADP就业人数  2001-10-01 -26.1   NaN -24.6
..         ...         ...   ...   ...   ...
271  美国ADP就业人数  2023-12-06  10.3  13.0  10.6
272  美国ADP就业人数  2024-01-04  16.4  11.5  10.1
273  美国ADP就业人数  2024-01-31  10.7  14.5  15.8
274  美国ADP就业人数  2024-03-06  14.0  14.9  11.1
275  美国ADP就业人数  2024-04-03  18.4  14.8  15.5
[276 rows x 5 columns]
```
