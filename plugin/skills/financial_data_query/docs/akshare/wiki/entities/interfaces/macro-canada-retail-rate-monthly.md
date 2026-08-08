---
title: "macro_canada_retail_rate_monthly - 零售销售月率"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_canada_retail_rate_monthly

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 加拿大宏观 > 零售销售月率
- 描述: 东方财富-经济数据-加拿大-零售销售月率
- 目标地址: http://data.eastmoney.com/cjsj/foreign_7_3.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 零售销售月率

接口: macro_canada_retail_rate_monthly

目标地址: http://data.eastmoney.com/cjsj/foreign_7_3.html

描述: 东方财富-经济数据-加拿大-零售销售月率

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

macro_canada_retail_rate_monthly_df = ak.macro_canada_retail_rate_monthly()
print(macro_canada_retail_rate_monthly_df)
```

数据示例

```
           时间   前值   现值        发布日期
0    2022年10月  1.2  NaN  2022-12-20
1    2022年09月  0.5  1.2  2022-11-22
2    2022年08月 -0.1  0.5  2022-10-21
3    2022年07月  1.9 -0.1  2022-09-23
4    2022年06月  5.2  1.9  2022-08-19
..        ...  ...  ...         ...
167  2008年05月  0.6  0.4  2008-07-22
168  2008年04月  0.1  0.6  2008-06-22
169  2008年03月 -0.7  0.1  2008-05-22
170  2008年02月  1.5 -0.7  2008-04-23
171  2008年01月  0.6  1.5  2008-03-23
```
