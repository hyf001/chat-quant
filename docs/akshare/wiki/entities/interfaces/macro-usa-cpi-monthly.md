---
title: "macro_usa_cpi_monthly - 美国CPI月率报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_usa_cpi_monthly

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 美国宏观 > 物价水平 > 美国CPI月率报告
- 描述: 美国 CPI 月率报告, 数据区间从 19700101-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_usa_cpi
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 美国CPI月率报告

接口: macro_usa_cpi_monthly

目标地址: https://datacenter.jin10.com/reportType/dc_usa_cpi

描述: 美国 CPI 月率报告, 数据区间从 19700101-至今

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

macro_usa_cpi_monthly_df = ak.macro_usa_cpi_monthly()
print(macro_usa_cpi_monthly_df)
```

数据示例

```
          商品        日期   今值  预测值   前值
0    美国CPI月率  1970-01-01  0.5  NaN  NaN
1    美国CPI月率  1970-02-01  0.5  NaN  0.5
2    美国CPI月率  1970-03-01  0.5  NaN  0.5
3    美国CPI月率  1970-04-01  0.5  NaN  0.5
4    美国CPI月率  1970-05-01  0.5  NaN  0.5
..       ...         ...  ...  ...  ...
647  美国CPI月率  2023-12-12  0.1  0.0  0.1
648  美国CPI月率  2024-01-11  0.3  0.2  0.2
649  美国CPI月率  2024-02-13  0.3  0.2  0.2
650  美国CPI月率  2024-03-12  0.4  0.4  0.3
651  美国CPI月率  2024-04-10  NaN  0.3  0.4
[652 rows x 5 columns]
```
