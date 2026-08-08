---
title: "macro_china_cpi_yearly - 中国 CPI 年率报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_cpi_yearly

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 国民经济运行状况 > 物价水平 > 中国 CPI 年率报告
- 描述: 中国年度 CPI 数据, 数据区间从 19860201-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_chinese_cpi_yoy
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 中国 CPI 年率报告

接口: macro_china_cpi_yearly

目标地址: https://datacenter.jin10.com/reportType/dc_chinese_cpi_yoy

描述: 中国年度 CPI 数据, 数据区间从 19860201-至今

限量: 单次返回所有历史数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

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

macro_china_cpi_yearly_df = ak.macro_china_cpi_yearly()
print(macro_china_cpi_yearly_df)
```

数据示例

```
            商品          日期   今值  预测值   前值
0    中国CPI年率报告  1986-02-01  7.1  NaN  NaN
1    中国CPI年率报告  1986-03-01  7.1  NaN  7.1
2    中国CPI年率报告  1986-04-01  7.1  NaN  7.1
3    中国CPI年率报告  1986-05-01  7.1  NaN  7.1
4    中国CPI年率报告  1986-06-01  7.1  NaN  7.1
..         ...         ...  ...  ...  ...
454  中国CPI年率报告  2023-12-09 -0.5 -0.1 -0.2
455  中国CPI年率报告  2024-01-12 -0.3 -0.4 -0.5
456  中国CPI年率报告  2024-02-08 -0.8 -0.5 -0.3
457  中国CPI年率报告  2024-03-09  0.7  0.3 -0.8
458  中国CPI年率报告  2024-04-11  NaN  NaN  0.7
[459 rows x 5 columns]
```
