---
title: "macro_euro_manufacturing_pmi - 欧元区制造业PMI初值报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_euro_manufacturing_pmi

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 欧元区宏观 > 产业指标 > 欧元区制造业PMI初值报告
- 描述: 欧元区制造业 PMI 初值报告, 数据区间从 20080222-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_eurozone_manufacturing_pmi
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 欧元区制造业PMI初值报告

接口: macro_euro_manufacturing_pmi

目标地址: https://datacenter.jin10.com/reportType/dc_eurozone_manufacturing_pmi

描述: 欧元区制造业 PMI 初值报告, 数据区间从 20080222-至今

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

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

macro_euro_manufacturing_pmi_df = ak.macro_euro_manufacturing_pmi()
print(macro_euro_manufacturing_pmi_df)
```

数据示例

```
              商品          日期    今值   预测值    前值
0    欧元区制造业PMI初值  2008-02-22  52.3  52.5  52.8
1    欧元区制造业PMI初值  2008-03-03  52.3  52.3  52.3
2    欧元区制造业PMI初值  2008-03-20  52.0  52.0  52.3
3    欧元区制造业PMI初值  2008-04-01  52.0  52.0  52.0
4    欧元区制造业PMI初值  2008-04-23  51.8  51.6  52.0
..           ...         ...   ...   ...   ...
353  欧元区制造业PMI初值  2022-09-23  48.5  48.7  49.6
354  欧元区制造业PMI初值  2022-10-03  48.4  48.5  49.6
355  欧元区制造业PMI初值  2022-10-24  46.6  47.8  48.4
356  欧元区制造业PMI初值  2022-11-02  46.4  46.6  48.4
357  欧元区制造业PMI初值  2022-11-23   NaN   NaN  46.4
```
