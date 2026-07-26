---
title: "macro_china_pmi - 采购经理人指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_pmi

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 采购经理人指数
- 描述: 采购经理人指数, 数据区间从 200801 至今, 月度数据
- 目标地址: http://data.eastmoney.com/cjsj/pmi.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 采购经理人指数

接口: macro_china_pmi

目标地址: http://data.eastmoney.com/cjsj/pmi.html

描述: 采购经理人指数, 数据区间从 200801 至今, 月度数据

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称        | 类型      | 描述      |
|-----------|---------|---------|
| 月份        | object  | -       |
| 制造业-指数    | float64 | -       |
| 制造业-同比增长  | float64 | 注意单位: % |
| 非制造业-指数   | float64 | -       |
| 非制造业-同比增长 | float64 | 注意单位: % |

接口示例

```python
import akshare as ak

macro_china_pmi_df = ak.macro_china_pmi()
print(macro_china_pmi_df)
```

数据示例

```
    月份  制造业-指数  制造业-同比增长  非制造业-指数  非制造业-同比增长
0    2022年10月份    49.2  0.000000     48.7  -7.061069
1    2022年09月份    50.1  1.008065     50.6  -4.887218
2    2022年08月份    49.4 -1.397206     52.6  10.736842
3    2022年07月份    49.0 -2.777778     53.8   0.938086
4    2022年06月份    50.2 -1.375246     54.7   2.242991
..         ...     ...       ...      ...        ...
173  2008年05月份    53.3 -4.308797     57.4  -7.717042
174  2008年04月份    59.2  1.023891     58.4  -3.311258
175  2008年03月份    58.4  4.099822     58.9   1.202749
176  2008年02月份    53.4  0.564972     59.3  -2.145215
177  2008年01月份    53.0 -3.811252     60.2  -0.331126
```
