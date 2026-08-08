---
title: "macro_usa_ism_pmi - 美国ISM制造业PMI报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_usa_ism_pmi

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 美国宏观 > 产业指标 > 制造业 > 美国ISM制造业PMI报告
- 描述: 美国 ISM 制造业 PMI 报告, 数据区间从 19700101-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_usa_ism_pmi
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 美国ISM制造业PMI报告

接口: macro_usa_ism_pmi

目标地址: https://datacenter.jin10.com/reportType/dc_usa_ism_pmi

描述: 美国 ISM 制造业 PMI 报告, 数据区间从 19700101-至今

限量: 单次返回所有历史数据

说明: 当前接口使用 Jin10 历史数据接口; 经 2026-07 校验, 该上游链路未继续提供最新数据, 返回结果可能仅更新至 2025 年附近, 不代表 AKShare 本地缓存异常

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称  | 类型      | 描述 |
|-----|---------|----|
| 商品  | object  | -  |
| 日期  | object  | -  |
| 今值  | float64 | -  |
| 预测值 | float64 | -  |
| 前值  | float64 | -  |

接口示例

```python
import akshare as ak

macro_usa_ism_pmi_df = ak.macro_usa_ism_pmi()
print(macro_usa_ism_pmi_df)
```

数据示例

```
                商品          日期    今值   预测值    前值
0    美国ISM制造业PMI报告  1970-01-01  52.0   NaN   NaN
1    美国ISM制造业PMI报告  1970-02-01  48.7   NaN  52.0
2    美国ISM制造业PMI报告  1970-03-01  47.4   NaN  48.7
3    美国ISM制造业PMI报告  1970-04-01  46.9   NaN  47.4
4    美国ISM制造业PMI报告  1970-05-01  45.0   NaN  46.9
..             ...         ...   ...   ...   ...
648  美国ISM制造业PMI报告  2023-12-01  46.7  47.6  46.7
649  美国ISM制造业PMI报告  2024-01-03  47.4  47.1  46.7
650  美国ISM制造业PMI报告  2024-02-01  49.1  47.2  47.1
651  美国ISM制造业PMI报告  2024-03-01  47.8  49.5  49.1
652  美国ISM制造业PMI报告  2024-04-01  50.3  48.5  47.8
[653 rows x 5 columns]
```
