---
title: "macro_china_hk_ppi - 香港制造业 PPI 年率"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_hk_ppi

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国香港宏观 > 香港制造业 PPI 年率
- 描述: 东方财富-经济数据一览-中国香港-香港制造业PPI年率
- 目标地址: https://data.eastmoney.com/cjsj/foreign_8_8.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 香港制造业 PPI 年率

接口: macro_china_hk_ppi

目标地址: https://data.eastmoney.com/cjsj/foreign_8_8.html

描述: 东方财富-经济数据一览-中国香港-香港制造业PPI年率

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

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

macro_china_hk_ppi_df = ak.macro_china_hk_ppi()
print(macro_china_hk_ppi_df)
```

数据示例

```
       时间   前值   现值     发布日期
0   2008第1季度  4.4  5.9  2008-06-13
1   2008第2季度  5.9  6.9  2008-09-12
2   2008第3季度  6.9  5.8  2008-12-12
3   2008第4季度  5.8  3.9  2009-03-13
4   2009第1季度  3.9 -1.4  2009-06-12
..       ...  ...  ...         ...
60  2023第1季度 -0.3  0.9  2023-06-15
61  2023第2季度  0.9 -0.2  2023-09-13
62  2023第3季度 -0.2  3.0  2023-12-14
63  2023第4季度  3.0  2.7  2024-03-14
64  2024第1季度  2.7  NaN  2024-06-14
[65 rows x 4 columns]
```
