---
title: "macro_china_pmi_yearly - 官方制造业 PMI"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_pmi_yearly

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 产业指标 > 官方制造业 PMI
- 描述: 中国年度PMI数据, 数据区间从 20050201-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_chinese_manufacturing_pmi
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 官方制造业 PMI

接口: macro_china_pmi_yearly

目标地址: https://datacenter.jin10.com/reportType/dc_chinese_manufacturing_pmi

描述: 中国年度PMI数据, 数据区间从 20050201-至今

限量: 单次返回所有历史数据

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

macro_china_pmi_yearly_df = ak.macro_china_pmi_yearly()
print(macro_china_pmi_yearly_df)
```

数据示例

```
             商品        日期      今值   预测值 前值
0    中国官方制造业PMI  2005-02-01  54.7   NaN   NaN
1    中国官方制造业PMI  2005-03-01  54.5   NaN  54.7
2    中国官方制造业PMI  2005-04-01  57.9   NaN  54.5
3    中国官方制造业PMI  2005-05-01  56.7   NaN  57.9
4    中国官方制造业PMI  2005-06-01  52.9   NaN  56.7
..          ...         ...   ...   ...   ...
228  中国官方制造业PMI  2023-11-30  49.4  49.7  49.5
229  中国官方制造业PMI  2023-12-31  49.0  49.5  49.4
230  中国官方制造业PMI  2024-01-31  49.2  49.2  49.0
231  中国官方制造业PMI  2024-03-01  49.1  49.1  49.2
232  中国官方制造业PMI  2024-03-31  50.8  50.1  49.1
[233 rows x 5 columns]
```
