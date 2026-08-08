---
title: "macro_euro_cpi_yoy - 欧元区CPI年率报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_euro_cpi_yoy

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 欧元区宏观 > 国民经济运行状况 > 物价水平 > 欧元区CPI年率报告
- 描述: 欧元区 CPI 年率报告, 数据区间从 19910201-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_eurozone_cpi_yoy
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 欧元区CPI年率报告

接口: macro_euro_cpi_yoy

目标地址: https://datacenter.jin10.com/reportType/dc_eurozone_cpi_yoy

描述: 欧元区 CPI 年率报告, 数据区间从 19910201-至今

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

macro_euro_cpi_yoy_df = ak.macro_euro_cpi_yoy()
print(macro_euro_cpi_yoy_df)
```

数据示例

```
           商品          日期    今值   预测值    前值
0    欧元区CPI年率  1991-02-01   0.0   NaN   NaN
1    欧元区CPI年率  1991-03-01   4.1   NaN   3.9
2    欧元区CPI年率  1991-04-01   3.9   NaN   4.1
3    欧元区CPI年率  1991-05-01   3.9   NaN   3.9
4    欧元区CPI年率  1991-06-01   4.1   NaN   3.9
..        ...         ...   ...   ...   ...
556  欧元区CPI年率  2022-09-16   9.1   9.1   9.1
557  欧元区CPI年率  2022-09-30  10.0   9.7   9.1
558  欧元区CPI年率  2022-10-19   9.9  10.0   9.1
559  欧元区CPI年率  2022-10-31  10.7  10.2   9.9
560  欧元区CPI年率  2022-11-17   NaN  10.0  10.7
```
