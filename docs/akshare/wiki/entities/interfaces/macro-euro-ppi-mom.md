---
title: "macro_euro_ppi_mom - 欧元区PPI月率报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_euro_ppi_mom

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 欧元区宏观 > 国民经济运行状况 > 物价水平 > 欧元区PPI月率报告
- 描述: 欧元区 PPI 月率报告, 数据区间从 19810301-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_eurozone_ppi_mom
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 欧元区PPI月率报告

接口: macro_euro_ppi_mom

目标地址: https://datacenter.jin10.com/reportType/dc_eurozone_ppi_mom

描述: 欧元区 PPI 月率报告, 数据区间从 19810301-至今

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

macro_euro_ppi_mom_df = ak.macro_euro_ppi_mom()
print(macro_euro_ppi_mom_df)
```

数据示例

```
           商品          日期   今值  预测值   前值
0    欧元区PPI月率  1981-03-01  1.0  NaN  NaN
1    欧元区PPI月率  1981-04-01  0.7  NaN  1.0
2    欧元区PPI月率  1981-05-01  1.5  NaN  0.7
3    欧元区PPI月率  1981-06-01  0.7  NaN  1.5
4    欧元区PPI月率  1981-07-01  0.6  NaN  0.7
..        ...         ...  ...  ...  ...
499  欧元区PPI月率  2022-07-04  0.7  1.0  1.2
500  欧元区PPI月率  2022-08-03  1.1  1.0  0.5
501  欧元区PPI月率  2022-09-02  4.0  2.5  1.3
502  欧元区PPI月率  2022-10-04  5.0  4.9  4.0
503  欧元区PPI月率  2022-11-04  NaN  1.7  5.0
```
