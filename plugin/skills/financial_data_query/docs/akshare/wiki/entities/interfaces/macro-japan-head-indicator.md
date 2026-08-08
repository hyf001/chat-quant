---
title: "macro_japan_head_indicator - 领先指标终值"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_japan_head_indicator

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 日本宏观 > 领先指标终值
- 描述: 东方财富-经济数据-日本-领先指标终值
- 目标地址: http://data.eastmoney.com/cjsj/foreign_3_4.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 领先指标终值

接口: macro_japan_head_indicator

目标地址: http://data.eastmoney.com/cjsj/foreign_3_4.html

描述: 东方财富-经济数据-日本-领先指标终值

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

macro_japan_head_indicator_df = ak.macro_japan_head_indicator()
print(macro_japan_head_indicator_df)
```

数据示例

```
     时间     前值     现值        发布日期
0    2008年01月  102.1  102.1  2008-03-08
1    2008年02月  102.1  102.4  2008-04-08
2    2008年03月  102.4  100.3  2008-05-07
3    2008年04月  100.3  100.4  2008-06-07
4    2008年05月  100.4  100.0  2008-07-07
..        ...    ...    ...         ...
171  2022年04月  100.8  102.9  2022-06-27
172  2022年05月  102.9  101.2  2022-07-27
173  2022年06月  101.2  100.9  2022-08-29
174  2022年07月  100.9   98.9  2022-09-28
175  2022年08月   98.9  101.3  2022-10-26
```
