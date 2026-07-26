---
title: "macro_swiss_svme - SVME 采购经理人指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_swiss_svme

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 瑞士宏观 > SVME 采购经理人指数
- 描述: 东方财富-经济数据-瑞士-SVME采购经理人指数
- 目标地址: http://data.eastmoney.com/cjsj/foreign_2_0.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### SVME 采购经理人指数

接口: macro_swiss_svme

目标地址: http://data.eastmoney.com/cjsj/foreign_2_0.html

描述: 东方财富-经济数据-瑞士-SVME采购经理人指数

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

macro_swiss_svme_df = ak.macro_swiss_svme()
print(macro_swiss_svme_df)
```

数据示例

```
     时间    前值    现值        发布日期
0    2007年12月   NaN  62.2  2008-01-01
1    2008年01月  62.2  62.3  2008-02-01
2    2008年02月  62.3  60.5  2008-03-03
3    2008年03月  60.5  55.3  2008-04-01
4    2008年04月  55.3  56.7  2008-05-02
..        ...   ...   ...         ...
174  2022年06月  60.0  59.1  2022-07-01
175  2022年07月  59.1  58.0  2022-08-02
176  2022年08月  58.0  56.4  2022-09-01
177  2022年09月  56.4  57.1  2022-10-03
178  2022年10月  57.1  54.9  2022-11-01
```
