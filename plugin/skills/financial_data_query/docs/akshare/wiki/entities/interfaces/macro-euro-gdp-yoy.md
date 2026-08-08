---
title: "macro_euro_gdp_yoy - 欧元区季度GDP年率报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_euro_gdp_yoy

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 欧元区宏观 > 国民经济运行状况 > 经济状况 > 欧元区季度GDP年率报告
- 描述: 欧元区季度 GDP 年率报告, 数据区间从 20131114-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_eurozone_gdp_yoy
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 欧元区季度GDP年率报告

接口: macro_euro_gdp_yoy

目标地址: https://datacenter.jin10.com/reportType/dc_eurozone_gdp_yoy

描述: 欧元区季度 GDP 年率报告, 数据区间从 20131114-至今

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

macro_euro_gdp_yoy_df = ak.macro_euro_gdp_yoy()
print(macro_euro_gdp_yoy_df)
```

数据示例

```
             商品          日期   今值  预测值   前值
0    欧元区季度GDP年率  2013-11-14 -0.4 -0.3 -0.5
1    欧元区季度GDP年率  2013-12-04 -0.4 -0.4 -0.4
2    欧元区季度GDP年率  2014-01-10 -0.3 -0.4 -0.4
3    欧元区季度GDP年率  2014-02-14  0.5  0.4 -0.3
4    欧元区季度GDP年率  2014-03-05  0.5  0.5  0.5
..          ...         ...  ...  ...  ...
97   欧元区季度GDP年率  2022-07-29  4.0  3.4  5.4
98   欧元区季度GDP年率  2022-08-17  3.9  4.0  4.0
99   欧元区季度GDP年率  2022-09-07  4.1  3.9  5.4
100  欧元区季度GDP年率  2022-10-31  2.1  NaN  4.3
101  欧元区季度GDP年率  2022-11-15  NaN  4.0  2.1
```
