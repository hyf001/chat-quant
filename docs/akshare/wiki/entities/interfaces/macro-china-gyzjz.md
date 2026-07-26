---
title: "macro_china_gyzjz - 工业增加值增长"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_gyzjz

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 产业指标 > 工业增加值增长
- 描述: 东方财富-中国工业增加值增长, 数据区间从 2008 - 至今
- 目标地址: https://data.eastmoney.com/cjsj/gyzjz.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 工业增加值增长

接口: macro_china_gyzjz

目标地址: https://data.eastmoney.com/cjsj/gyzjz.html

描述: 东方财富-中国工业增加值增长, 数据区间从 2008 - 至今

限量: 单次返回所有历史数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称   | 类型      | 描述      |
|------|---------|---------|
| 月份   | object  | -       |
| 同比增长 | float64 | 注意单位: % |
| 累计增长 | float64 | 注意单位: % |
| 发布时间 | object  | -       |

接口示例

```python
import akshare as ak

macro_china_gyzjz_df = ak.macro_china_gyzjz()
print(macro_china_gyzjz_df)
```

数据示例

```
           月份  同比增长  累计增长 发布时间
0    2008年02月份  15.4  15.4  2008-02-01
1    2008年03月份  17.8  16.4  2008-03-01
2    2008年04月份  15.7  16.3  2008-04-01
3    2008年05月份  16.0  16.3  2008-05-01
4    2008年06月份  16.0  16.3  2008-06-01
..         ...   ...   ...         ...
165  2023年02月份   NaN   2.4  2023-02-01
166  2023年03月份   3.9   3.0  2023-03-01
167  2023年04月份   5.6   3.6  2023-04-01
168  2023年05月份   3.5   3.6  2023-05-01
169  2023年06月份   4.4   3.8  2023-06-01
[170 rows x 4 columns]
```
