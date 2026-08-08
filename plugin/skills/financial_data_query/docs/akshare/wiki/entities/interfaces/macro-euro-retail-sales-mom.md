---
title: "macro_euro_retail_sales_mom - 欧元区零售销售月率报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_euro_retail_sales_mom

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 欧元区宏观 > 国民经济运行状况 > 物价水平 > 欧元区零售销售月率报告
- 描述: 欧元区零售销售月率报告, 数据区间从 20000301-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_eurozone_retail_sales_mom
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 欧元区零售销售月率报告

接口: macro_euro_retail_sales_mom

目标地址: https://datacenter.jin10.com/reportType/dc_eurozone_retail_sales_mom

描述: 欧元区零售销售月率报告, 数据区间从 20000301-至今

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

macro_euro_retail_sales_mom_df = ak.macro_euro_retail_sales_mom()
print(macro_euro_retail_sales_mom_df)
```

数据示例

```
            商品          日期   今值  预测值   前值
0    欧元区零售销售月率  2000-03-01  0.7  NaN  NaN
1    欧元区零售销售月率  2000-04-01 -0.3  NaN  0.7
2    欧元区零售销售月率  2000-05-01  0.7  NaN -0.3
3    欧元区零售销售月率  2000-06-01  0.3  NaN  0.7
4    欧元区零售销售月率  2000-07-01  0.1  NaN  0.3
..         ...         ...  ...  ...  ...
271  欧元区零售销售月率  2022-07-06  0.2  0.4 -1.4
272  欧元区零售销售月率  2022-08-03 -1.2  0.1  0.4
273  欧元区零售销售月率  2022-09-05  0.3  0.4 -1.0
274  欧元区零售销售月率  2022-10-06 -0.3 -0.4 -0.4
275  欧元区零售销售月率  2022-11-08  NaN -0.4 -0.3
```
