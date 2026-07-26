---
title: "macro_usa_industrial_production - 美国工业产出月率报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_usa_industrial_production

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 美国宏观 > 产业指标 > 工业 > 美国工业产出月率报告
- 描述: 美国工业产出月率报告, 数据区间从 19700101-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_usa_industrial_production
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 美国工业产出月率报告

接口: macro_usa_industrial_production

目标地址: https://datacenter.jin10.com/reportType/dc_usa_industrial_production

描述: 美国工业产出月率报告, 数据区间从 19700101-至今

限量: 单次返回所有历史数据

说明: 当前接口使用 Jin10 历史数据接口; 经 2026-07 校验, 该上游链路未继续提供最新数据, 返回结果可能仅更新至 2025 年附近, 不代表 AKShare 本地缓存异常

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

macro_usa_industrial_production_df = ak.macro_usa_industrial_production()
print(macro_usa_industrial_production_df)
```

数据示例

```
             商品          日期   今值  预测值   前值
0    美国工业产出月率报告  1970-01-01 -0.3  NaN  NaN
1    美国工业产出月率报告  1970-02-01 -1.9  NaN -0.3
2    美国工业产出月率报告  1970-03-01 -0.1  NaN -1.9
3    美国工业产出月率报告  1970-04-01 -0.1  NaN -0.1
4    美国工业产出月率报告  1970-05-01 -0.3  NaN -0.1
..          ...         ...  ...  ...  ...
647  美国工业产出月率报告  2023-12-15  0.2  0.3 -0.9
648  美国工业产出月率报告  2024-01-17  0.1  0.0  0.0
649  美国工业产出月率报告  2024-02-15 -0.1  0.2  0.1
650  美国工业产出月率报告  2024-03-15  0.1  0.0 -0.5
651  美国工业产出月率报告  2024-04-16  NaN  NaN  0.1
[652 rows x 5 columns]
```
