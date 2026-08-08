---
title: "macro_usa_pmi - 美国Markit制造业PMI初值报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_usa_pmi

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 美国宏观 > 产业指标 > 制造业 > 美国Markit制造业PMI初值报告
- 描述: 美国 Markit 制造业 PMI 初值报告, 数据区间从 20120601-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_usa_pmi
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 美国Markit制造业PMI初值报告

接口: macro_usa_pmi

目标地址: https://datacenter.jin10.com/reportType/dc_usa_pmi

描述: 美国 Markit 制造业 PMI 初值报告, 数据区间从 20120601-至今

限量: 单次返回所有历史数据

输入参数

| 名称 | 类型   | 描述 |
|----|------|----|
| -  | -  - |

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

macro_usa_pmi_df = ak.macro_usa_pmi()
print(macro_usa_pmi_df)
```

数据示例

```
                   商品          日期    今值   预测值    前值
0    美国Markit制造业PMI报告  2012-06-01  54.0   NaN  53.9
1    美国Markit制造业PMI报告  2012-07-02  52.5  53.0  52.9
2    美国Markit制造业PMI报告  2012-07-24  51.8  52.1  52.5
3    美国Markit制造业PMI报告  2012-08-01  51.4  51.9  51.8
4    美国Markit制造业PMI报告  2012-08-23  51.9  51.3  51.4
..                ...         ...   ...   ...   ...
280  美国Markit制造业PMI报告  2024-02-22  51.5  50.5  50.7
281  美国Markit制造业PMI报告  2024-03-01  52.2  51.5  50.7
282  美国Markit制造业PMI报告  2024-03-21  52.5  51.8  52.2
283  美国Markit制造业PMI报告  2024-04-01  51.9  52.5  52.2
284  美国Markit制造业PMI报告  2024-04-23   NaN   NaN  51.9
[285 rows x 5 columns]
```
