---
title: "macro_usa_phs - 未决房屋销售月率"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_usa_phs

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 美国宏观 > 领先指标 > 未决房屋销售月率
- 描述: 东方财富-经济数据一览-美国-未决房屋销售月率, 数据区间从 20080201-至今
- 目标地址: http://data.eastmoney.com/cjsj/foreign_0_5.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 未决房屋销售月率

接口: macro_usa_phs

目标地址: http://data.eastmoney.com/cjsj/foreign_0_5.html

描述: 东方财富-经济数据一览-美国-未决房屋销售月率, 数据区间从 20080201-至今

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

macro_usa_phs_df = ak.macro_usa_phs()
print(macro_usa_phs_df)
```

数据示例

```
      时间   前值   现值        发布日期
0    2022年10月 -1.5 -5.9  2022-11-18
1    2022年09月 -0.4 -1.5  2022-10-20
2    2022年08月 -5.9 -0.4  2022-09-21
3    2022年07月 -5.4 -5.9  2022-08-18
4    2022年06月 -3.4 -5.4  2022-07-20
..        ...  ...  ...         ...
166  2008年07月  5.3 -3.2  2008-08-28
167  2008年06月 -4.7  5.3  2008-07-29
168  2008年05月  6.3 -4.7  2008-06-28
169  2008年04月  0.0  6.3  2008-05-29
170  2008年01月 -1.5  0.0  2008-02-28
```
