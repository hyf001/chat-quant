---
title: "macro_euro_services_pmi - 欧元区服务业PMI终值报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_euro_services_pmi

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 欧元区宏观 > 产业指标 > 欧元区服务业PMI终值报告
- 描述: 欧元区服务业 PMI 终值报告, 数据区间从 20080222-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_eurozone_services_pmi
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 欧元区服务业PMI终值报告

接口: macro_euro_services_pmi

目标地址: https://datacenter.jin10.com/reportType/dc_eurozone_services_pmi

描述: 欧元区服务业 PMI 终值报告, 数据区间从 20080222-至今

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

macro_euro_services_pmi_df = ak.macro_euro_services_pmi()
print(macro_euro_services_pmi_df)
```

数据示例

```
              商品          日期    今值   预测值    前值
0    欧元区服务业PMI终值  2008-02-22  52.3  51.0  50.6
1    欧元区服务业PMI终值  2008-03-05  52.3  52.3  52.3
2    欧元区服务业PMI终值  2008-04-03  51.6   0.0  51.7
3    欧元区服务业PMI终值  2008-04-23  51.8  51.4  51.6
4    欧元区服务业PMI终值  2008-05-06  52.0  51.8  51.8
..           ...         ...   ...   ...   ...
351  欧元区服务业PMI终值  2022-09-23  48.9  49.0  49.8
352  欧元区服务业PMI终值  2022-10-05  48.8  48.9  49.8
353  欧元区服务业PMI终值  2022-10-24  48.2  48.2  48.8
354  欧元区服务业PMI终值  2022-11-04   NaN  48.2  48.2
355  欧元区服务业PMI终值  2022-11-23   NaN  48.2  48.8
```
