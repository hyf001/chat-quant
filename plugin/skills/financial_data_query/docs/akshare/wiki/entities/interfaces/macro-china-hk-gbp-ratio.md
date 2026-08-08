---
title: "macro_china_hk_gbp_ratio - GDP 同比"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_hk_gbp_ratio

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国香港宏观 > GDP 同比
- 描述: 东方财富-经济数据一览-中国香港-香港 GDP 同比
- 目标地址: https://data.eastmoney.com/cjsj/foreign_8_4.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### GDP 同比

接口: macro_china_hk_gbp_ratio

目标地址: https://data.eastmoney.com/cjsj/foreign_8_4.html

描述: 东方财富-经济数据一览-中国香港-香港 GDP 同比

限量: 单次返回所有历史数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称   | 类型      | 描述      |
|------|---------|---------|
| 时间   | object  | -       |
| 前值   | float64 | 注意单位: % |
| 现值   | float64 | 注意单位: % |
| 发布日期 | object  | -       |

接口示例

```python
import akshare as ak

macro_china_hk_gbp_ratio_df = ak.macro_china_hk_gbp_ratio()
print(macro_china_hk_gbp_ratio_df)
```

数据示例

```
        时间    前值   现值      发布日期
0   2008第1季度  12.3  9.7  2008-05-15
1   2008第2季度   9.7  6.0  2008-08-15
2   2008第3季度   6.0  2.9  2008-11-15
3   2008第4季度   2.9 -3.4  2009-02-14
4   2009第1季度  -3.4 -7.1  2009-05-15
..       ...   ...  ...         ...
60  2023第1季度  -2.9  5.2  2023-05-12
61  2023第2季度   5.2  4.9  2023-08-11
62  2023第3季度   4.9  7.1  2023-11-10
63  2023第4季度   7.1  8.5  2024-02-28
64  2024第1季度   8.5  NaN  2024-05-17
[65 rows x 4 columns]
```
