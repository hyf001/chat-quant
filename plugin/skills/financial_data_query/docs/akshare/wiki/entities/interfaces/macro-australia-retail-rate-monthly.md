---
title: "macro_australia_retail_rate_monthly - 零售销售月率"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_australia_retail_rate_monthly

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 澳大利亚宏观 > 零售销售月率
- 描述: 东方财富-经济数据-澳大利亚-零售销售月率
- 目标地址: http://data.eastmoney.com/cjsj/foreign_5_0.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 零售销售月率

接口: macro_australia_retail_rate_monthly

目标地址: http://data.eastmoney.com/cjsj/foreign_5_0.html

描述: 东方财富-经济数据-澳大利亚-零售销售月率

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

macro_australia_retail_rate_monthly_df = ak.macro_australia_retail_rate_monthly()
print(macro_australia_retail_rate_monthly_df)
```

数据示例

```
       时间    前值    现值      发布日期
0    2008年01月  23.4 -23.6  2008-03-06
1    2008年02月 -23.6  -7.7  2008-04-06
2    2008年03月  -7.7   6.1  2008-05-05
3    2008年04月   6.1  -1.5  2008-06-05
4    2008年05月  -1.5   3.7  2008-07-05
..        ...   ...   ...         ...
199  2024年08月   1.2   2.2  2024-10-01
200  2024年09月   2.2  -1.7  2024-10-31
201  2024年10月  -1.7   5.7  2024-12-02
202  2024年11月   5.7   7.8  2025-01-09
203  2024年12月   7.8   NaN  2025-02-03
[204 rows x 4 columns]
```
