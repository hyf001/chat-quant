---
title: "macro_uk_retail_yearly - 零售销售年率"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_uk_retail_yearly

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 英国宏观 > 零售销售年率
- 描述: 东方财富-经济数据-英国-零售销售年率
- 目标地址: http://data.eastmoney.com/cjsj/foreign_4_9.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 零售销售年率

接口: macro_uk_retail_yearly

目标地址: http://data.eastmoney.com/cjsj/foreign_4_9.html

描述: 东方财富-经济数据-英国-零售销售年率

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称   | 类型      | 描述  |
|------|---------|-----|
| 时间   | object  | -   |
| 前值   | float64 | -   |
| 现值   | float64 | -   |
| 发布日期 | object  | -   |

接口示例

```python
import akshare as ak

macro_uk_retail_yearly_df = ak.macro_uk_retail_yearly()
print(macro_uk_retail_yearly_df)
```

数据示例

```
     时间   前值   现值        发布日期
0    2008年01月  2.7  5.6  2008-02-20
1    2008年02月  5.6  5.5  2008-03-22
2    2008年03月  5.5  4.6  2008-04-20
3    2008年04月  4.6  4.2  2008-05-21
4    2008年05月  4.2  8.1  2008-06-20
..        ...  ...  ...         ...
170  2022年06月 -4.7 -5.8  2022-07-22
171  2022年07月 -5.8 -3.4  2022-08-19
172  2022年08月 -3.4 -5.4  2022-09-16
173  2022年09月 -5.4 -0.4  2022-10-21
174  2022年10月 -0.4  NaN  2022-11-18
```
