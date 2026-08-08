---
title: "macro_china_ppi_yearly - 中国 PPI 年率报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_ppi_yearly

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 国民经济运行状况 > 物价水平 > 中国 PPI 年率报告
- 描述: 中国年度 PPI 数据, 数据区间从 19950801-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_chinese_ppi_yoy
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 中国 PPI 年率报告

接口: macro_china_ppi_yearly

目标地址: https://datacenter.jin10.com/reportType/dc_chinese_ppi_yoy

描述: 中国年度 PPI 数据, 数据区间从 19950801-至今

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

macro_china_ppi_yearly_df = ak.macro_china_ppi_yearly()
print(macro_china_ppi_yearly_df)
```

数据示例

```
            商品          日期    今值  预测值    前值
0    中国PPI年率报告  1995-08-01  13.5  NaN   NaN
1    中国PPI年率报告  1995-09-01  13.0  NaN  13.5
2    中国PPI年率报告  1995-10-01  12.9  NaN  13.0
3    中国PPI年率报告  1995-11-01  12.5  NaN  12.9
4    中国PPI年率报告  1995-12-01  11.1  NaN  12.5
..         ...         ...   ...  ...   ...
340  中国PPI年率报告  2023-12-09  -3.0 -2.8  -2.6
341  中国PPI年率报告  2024-01-12  -2.7 -2.6  -3.0
342  中国PPI年率报告  2024-02-08  -2.5 -2.6  -2.7
343  中国PPI年率报告  2024-03-09  -2.7 -2.5  -2.5
344  中国PPI年率报告  2024-04-11   NaN  NaN  -2.7
[345 rows x 5 columns]
```
