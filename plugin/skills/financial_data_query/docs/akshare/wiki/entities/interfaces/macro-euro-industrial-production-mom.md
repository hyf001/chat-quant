---
title: "macro_euro_industrial_production_mom - 欧元区工业产出月率报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_euro_industrial_production_mom

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 欧元区宏观 > 产业指标 > 欧元区工业产出月率报告
- 描述: 欧元区工业产出月率报告, 数据区间从 19910301-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_eurozone_industrial_production_mom
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 欧元区工业产出月率报告

接口: macro_euro_industrial_production_mom

目标地址: https://datacenter.jin10.com/reportType/dc_eurozone_industrial_production_mom

描述: 欧元区工业产出月率报告, 数据区间从 19910301-至今

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

macro_euro_industrial_production_mom_df = ak.macro_euro_industrial_production_mom()
print(macro_euro_industrial_production_mom_df)
```

数据示例

```
            商品          日期   今值  预测值   前值
0    欧元区工业产出月率  1991-03-01 -1.1  NaN  NaN
1    欧元区工业产出月率  1991-04-01 -1.0  NaN -1.1
2    欧元区工业产出月率  1991-05-01 -0.5  NaN -1.0
3    欧元区工业产出月率  1991-06-01 -0.1  NaN -0.5
4    欧元区工业产出月率  1991-07-01  1.9  NaN -0.1
..         ...         ...  ...  ...  ...
380  欧元区工业产出月率  2022-07-13  0.8  0.3  0.5
381  欧元区工业产出月率  2022-08-12  0.7  0.2  2.1
382  欧元区工业产出月率  2022-09-14 -2.3 -1.0  1.1
383  欧元区工业产出月率  2022-10-12  1.5  0.6 -2.3
384  欧元区工业产出月率  2022-11-14  NaN  NaN  1.5
```
