---
title: "macro_canada_new_house_rate - 新屋开工"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_canada_new_house_rate

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 加拿大宏观 > 新屋开工
- 描述: 东方财富-经济数据-加拿大-新屋开工
- 目标地址: http://data.eastmoney.com/cjsj/foreign_7_0.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 新屋开工

接口: macro_canada_new_house_rate

目标地址: http://data.eastmoney.com/cjsj/foreign_7_0.html

描述: 东方财富-经济数据-加拿大-新屋开工

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称   | 类型      | 描述      |
|------|---------|---------|
| 时间   | object  | -       |
| 前值   | float64 | 注意单位: 万 |
| 现值   | float64 | 注意单位: 万 |
| 发布日期 | object  | -       |

接口示例

```python
import akshare as ak

macro_canada_new_house_rate_df = ak.macro_canada_new_house_rate()
print(macro_canada_new_house_rate_df)
```

数据示例

```
     时间     前值     现值        发布日期
0    2022年10月  29.96  26.71  2022-11-16
1    2022年09月  26.74  29.96  2022-10-14
2    2022年08月  27.53  26.74  2022-09-16
3    2022年07月  27.37  27.53  2022-08-16
4    2022年06月  28.73  27.37  2022-07-18
..        ...    ...    ...         ...
173  2008年05月  21.39  22.13  2008-06-09
174  2008年04月  25.47  21.39  2008-05-10
175  2008年03月  25.69  25.47  2008-04-09
176  2008年02月  22.27  25.69  2008-03-11
177  2008年01月  18.75  22.27  2008-02-09
```
