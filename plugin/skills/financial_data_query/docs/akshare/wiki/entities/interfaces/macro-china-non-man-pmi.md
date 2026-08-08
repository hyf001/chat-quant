---
title: "macro_china_non_man_pmi - 中国官方非制造业PMI"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_non_man_pmi

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 产业指标 > 中国官方非制造业PMI
- 描述: 中国官方非制造业 PMI, 数据区间从 20160101-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_chinese_non_manufacturing_pmi
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 中国官方非制造业PMI

接口: macro_china_non_man_pmi

目标地址: https://datacenter.jin10.com/reportType/dc_chinese_non_manufacturing_pmi

描述: 中国官方非制造业 PMI, 数据区间从 20160101-至今

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

macro_china_non_man_pmi_df = ak.macro_china_non_man_pmi()
print(macro_china_non_man_pmi_df)
```

数据示例

```
                商品          日期    今值   预测值    前值
0    中国官方非制造业PMI报告  2007-02-01  60.4   NaN   NaN
1    中国官方非制造业PMI报告  2007-03-01  60.6   NaN  60.4
2    中国官方非制造业PMI报告  2007-04-01  58.2   NaN  60.6
3    中国官方非制造业PMI报告  2007-05-01  60.4   NaN  58.2
4    中国官方非制造业PMI报告  2007-06-01  62.2   NaN  60.4
..             ...         ...   ...   ...   ...
204  中国官方非制造业PMI报告  2023-11-30  50.2  51.1  50.6
205  中国官方非制造业PMI报告  2023-12-31  50.4  50.5  50.2
206  中国官方非制造业PMI报告  2024-01-31  50.7  50.6  50.4
207  中国官方非制造业PMI报告  2024-03-01  51.4  50.9  50.7
208  中国官方非制造业PMI报告  2024-03-31  53.0  51.3  51.4
[209 rows x 5 columns]
```
