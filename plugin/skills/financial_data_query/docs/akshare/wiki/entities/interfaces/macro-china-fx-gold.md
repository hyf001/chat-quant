---
title: "macro_china_fx_gold - 外汇和黄金储备"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_fx_gold

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 外汇和黄金储备
- 描述: 中国外汇和黄金储备, 数据区间从 200801 至今, 月度数据
- 目标地址: http://data.eastmoney.com/cjsj/hjwh.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 外汇和黄金储备

接口: macro_china_fx_gold

目标地址: http://data.eastmoney.com/cjsj/hjwh.html

描述: 中国外汇和黄金储备, 数据区间从 200801 至今, 月度数据

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称        | 类型      | 描述        |
|-----------|---------|-----------|
| 月份        | object  | 年度和月份     |
| 黄金储备-数值   | float64 | 注意单位: 万盎司 |
| 黄金储备-同比   | float64 | 注意单位: 万盎司 |
| 黄金储备-环比   | float64 | 注意单位: 万盎司 |
| 国家外汇储备-数值 | float64 | 注意单位: 亿美元 |
| 国家外汇储备-同比 | float64 | 注意单位: 亿美元 |
| 国家外汇储备-环比 | float64 | 注意单位: 亿美元 |

接口示例

```python
import akshare as ak

macro_china_fx_gold_df = ak.macro_china_fx_gold()
print(macro_china_fx_gold_df)
```

数据示例

```
       月份  黄金储备-数值    黄金储备-同比   黄金储备-环比   国家外汇储备-数值  国家外汇储备-同比  国家外汇储备-环比
0    2008年01月份      NaN        NaN       NaN  15898.1040  43.914387   4.028224
1    2008年02月份      NaN        NaN       NaN  16471.3371  42.316677   3.605670
2    2008年03月份      NaN        NaN       NaN  16821.7700  39.944557   2.127532
3    2008年04月份      NaN        NaN       NaN  17566.5514  40.919594   4.427485
4    2008年05月份      NaN        NaN       NaN  17969.6074  39.011455   2.294451
..         ...      ...        ...       ...         ...        ...        ...
170  2022年03月份  1216.63  14.849008  1.690906  31879.9400   0.566714  -0.803808
171  2022年04月份  1197.31   8.126829 -1.587993  31197.2000  -2.453270  -2.141598
172  2022年05月份  1151.83  -3.223828 -3.798515  31277.8000  -2.918335   0.258357
173  2022年06月份  1138.23   3.053871 -1.180730  30712.7200  -4.441119  -1.806649
174  2022年07月份  1098.39  -3.963383 -3.500171  31040.7100  -4.073655   1.067929
```
