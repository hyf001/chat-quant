---
title: "macro_australia_ppi_quarterly - 生产者物价指数季率"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_australia_ppi_quarterly

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 澳大利亚宏观 > 生产者物价指数季率
- 描述: 东方财富-经济数据-澳大利亚-生产者物价指数季率
- 目标地址: http://data.eastmoney.com/cjsj/foreign_5_3.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 生产者物价指数季率

接口: macro_australia_ppi_quarterly

目标地址: http://data.eastmoney.com/cjsj/foreign_5_3.html

描述: 东方财富-经济数据-澳大利亚-生产者物价指数季率

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

macro_australia_ppi_quarterly_df = ak.macro_australia_ppi_quarterly()
print(macro_australia_ppi_quarterly_df)
```

数据示例

```
    时间   前值   现值        发布日期
0   2008年03月  0.7  1.9  2008-04-29
1   2008年06月  1.9  1.0  2008-07-30
2   2008年09月  1.0  1.9  2008-10-30
3   2008年12月  1.9  1.4  2009-01-29
4   2009年03月  1.4 -0.3  2009-04-29
..       ...  ...  ...         ...
63  2023年12月  1.8  0.9  2024-02-02
64  2024年03月  0.9  0.9  2024-04-26
65  2024年06月  0.9  1.0  2024-08-02
66  2024年09月  1.0  0.9  2024-11-01
67  2024年12月  0.9  NaN  2025-01-31
[68 rows x 4 columns]
```
