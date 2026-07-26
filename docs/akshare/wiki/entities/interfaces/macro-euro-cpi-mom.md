---
title: "macro_euro_cpi_mom - 欧元区CPI月率报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_euro_cpi_mom

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 欧元区宏观 > 国民经济运行状况 > 物价水平 > 欧元区CPI月率报告
- 描述: 欧元区 CPI 月率报告, 数据区间从 19900301-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_eurozone_cpi_mom
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 欧元区CPI月率报告

接口: macro_euro_cpi_mom

目标地址: https://datacenter.jin10.com/reportType/dc_eurozone_cpi_mom

描述: 欧元区 CPI 月率报告, 数据区间从 19900301-至今

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

macro_euro_cpi_mom_df = ak.macro_euro_cpi_mom()
print(macro_euro_cpi_mom_df)
```

数据示例

```
          商品          日期   今值  预测值   前值
0    欧元区CPI月率  1990-03-01  0.4  NaN  NaN
1    欧元区CPI月率  1990-04-01  0.2  NaN  0.4
2    欧元区CPI月率  1990-05-01  0.4  NaN  0.2
3    欧元区CPI月率  1990-06-01  0.2  NaN  0.4
4    欧元区CPI月率  1990-07-01  0.1  NaN  0.2
..        ...         ...  ...  ...  ...
421  欧元区CPI月率  2022-09-16  0.6  0.5  0.1
422  欧元区CPI月率  2022-09-30  1.2  0.9  0.6
423  欧元区CPI月率  2022-10-19  1.2  1.2  0.6
424  欧元区CPI月率  2022-10-31  1.5  NaN  1.2
425  欧元区CPI月率  2022-11-17  NaN  1.2  1.2
```
