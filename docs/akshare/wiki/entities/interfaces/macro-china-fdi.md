---
title: "macro_china_fdi - 外商直接投资数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_fdi

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 国民经济运行状况 > 经济状况 > 外商直接投资数据
- 描述: 东方财富-经济数据一览-中国-外商直接投资数据, 数据区间从 200801-202307
- 目标地址: https://data.eastmoney.com/cjsj/fdi.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 外商直接投资数据

接口: macro_china_fdi

目标地址: https://data.eastmoney.com/cjsj/fdi.html

描述: 东方财富-经济数据一览-中国-外商直接投资数据, 数据区间从 200801-202307

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称      | 类型      | 描述       |
|---------|---------|----------|
| 月份      | object  | -        |
| 当月      | int64   | -        |
| 当月-同比增长 | float64 | 注意单位: 美元 |
| 当月-环比增长 | float64 | 注意单位: %  |
| 累计      | float64 | 注意单位: 美元 |
| 累计-同比增长 | float64 | 注意单位: %  |

接口示例

```python
import akshare as ak

macro_china_fdi_df = ak.macro_china_fdi()
print(macro_china_fdi_df)
```

数据示例

```
     月份          当月        当月-同比增长 当月-环比增长  累计  累计-同比增长
0    2008年01月份  11200250.0  116.422424 -14.460445   11200250   109.78
1    2008年02月份   6928190.0   52.801205 -38.142541   18128440    75.19
2    2008年03月份   9285600.0   50.171752  34.026347   27414040    61.26
3    2008年04月份   7602890.0   70.214971 -18.121715   35016930    59.32
4    2008年05月份   7760960.0   58.421856   2.079078   42777890    54.97
..         ...         ...         ...        ...        ...      ...
180  2023年01月份  19020000.0   20.075758  72.126697   19020000    10.00
181  2023年02月份  20690000.0   -6.039964   8.780231   39710000     1.00
182  2023年04月份         NaN         NaN        NaN   73500000    -3.30
183  2023年05月份  10850000.0  -18.421053        NaN   84350000    -5.60
184  2023年07月份         NaN         NaN        NaN  111800000    -9.80
[185 rows x 6 columns]
```
