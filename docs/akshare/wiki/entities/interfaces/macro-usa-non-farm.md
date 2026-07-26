---
title: "macro_usa_non_farm - 美国非农就业人数报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_usa_non_farm

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 美国宏观 > 劳动力市场 > 就业人口 > 美国非农就业人数报告
- 描述: 美国非农就业人数报告, 数据区间从 19700102-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_nonfarm_payrolls
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 美国非农就业人数报告

接口: macro_usa_non_farm

目标地址: https://datacenter.jin10.com/reportType/dc_nonfarm_payrolls

描述: 美国非农就业人数报告, 数据区间从 19700102-至今

限量: 单次返回所有历史数据

说明: 当前接口使用 Jin10 历史数据接口; 经 2026-07 校验, 该上游链路未继续提供最新数据, 返回结果可能仅更新至 2025 年附近, 不代表 AKShare 本地缓存异常

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

macro_usa_non_farm_df = ak.macro_usa_non_farm()
print(macro_usa_non_farm_df)
```

数据示例

```
           商品          日期    今值   预测值    前值
0    美国非农就业人数  1970-01-02  15.3   NaN  -3.3
1    美国非农就业人数  1970-02-06  -6.4   NaN  15.3
2    美国非农就业人数  1970-03-06  12.8   NaN  -6.4
3    美国非农就业人数  1970-04-03  14.8   NaN  12.8
4    美国非农就业人数  1970-05-01 -10.4   NaN  14.8
..        ...         ...   ...   ...   ...
647  美国非农就业人数  2023-12-08  19.9  18.0  15.0
648  美国非农就业人数  2024-01-05  21.6  17.0  17.3
649  美国非农就业人数  2024-02-02  35.3  18.7  33.3
650  美国非农就业人数  2024-03-08  27.5  19.8  22.9
651  美国非农就业人数  2024-04-05   NaN  21.2  27.5
[652 rows x 5 columns]
```
