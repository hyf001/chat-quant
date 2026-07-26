---
title: "macro_china_cx_pmi_yearly - 财新制造业PMI终值"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_cx_pmi_yearly

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 产业指标 > 财新制造业PMI终值
- 描述: 中国年度财新 PMI 数据, 数据区间从 20120120-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_chinese_caixin_manufacturing_pmi
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 财新制造业PMI终值

接口: macro_china_cx_pmi_yearly

目标地址: https://datacenter.jin10.com/reportType/dc_chinese_caixin_manufacturing_pmi

描述: 中国年度财新 PMI 数据, 数据区间从 20120120-至今

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

macro_china_cx_pmi_yearly_df = ak.macro_china_cx_pmi_yearly()
print(macro_china_cx_pmi_yearly_df)
```

数据示例

```
                 商品          日期    今值   预测值    前值
0    中国财新制造业PMI终值报告  2012-01-20  48.8   NaN  48.7
1    中国财新制造业PMI终值报告  2012-02-22  49.7   NaN  48.8
2    中国财新制造业PMI终值报告  2012-03-22  48.1   NaN  49.6
3    中国财新制造业PMI终值报告  2012-04-23  49.1   NaN  48.3
4    中国财新制造业PMI终值报告  2012-05-02  49.3   NaN  49.1
..              ...         ...   ...   ...   ...
196  中国财新制造业PMI终值报告  2023-12-01  50.7  49.3  49.5
197  中国财新制造业PMI终值报告  2024-01-02  50.8  50.4  50.7
198  中国财新制造业PMI终值报告  2024-02-01  50.8  50.8  50.8
199  中国财新制造业PMI终值报告  2024-03-01  50.9  50.7  50.8
200  中国财新制造业PMI终值报告  2024-04-01  51.1  51.0  50.9
[201 rows x 5 columns]
```
