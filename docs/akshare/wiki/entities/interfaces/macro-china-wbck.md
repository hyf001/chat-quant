---
title: "macro_china_wbck - 本外币存款"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_wbck

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 本外币存款
- 描述: 本外币存款, 数据区间从 200802 至今, 月度数据
- 目标地址: http://data.eastmoney.com/cjsj/wbck.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 本外币存款

接口: macro_china_wbck

目标地址: http://data.eastmoney.com/cjsj/wbck.html

描述: 本外币存款, 数据区间从 200802 至今, 月度数据

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称   | 类型      | 描述       |
|------|---------|----------|
| 月份   | object  | -        |
| 当月   | float64 | 注意单位: 亿元 |
| 同比增长 | float64 | 注意单位: %  |
| 环比增长 | float64 | 注意单位: %  |
| 累计   | float64 | 注意单位: 亿元 |

接口示例

```python
import akshare as ak

macro_china_wbck_df = ak.macro_china_wbck()
print(macro_china_wbck_df)
```

数据示例

```
      月份        当月        同比增长        环比增长          累计
0    2022年10月份  -2650.78 -132.917535 -110.068013  2610227.88
1    2022年09月份  26328.73   14.546846  134.206364  2612878.66
2    2022年08月份  11241.68  -19.737487  871.473473  2586549.93
3    2022年07月份  -1457.17   88.621966 -102.976736  2575308.25
4    2022年06月份  48951.94   22.914621   63.520287  2576765.42
..         ...       ...         ...         ...         ...
173  2008年05月份   8763.12  370.965835   22.035258   442540.86
174  2008年04月份   7180.81   69.117415  -33.125126   433777.74
175  2008年03月份  10737.68   25.845804  -19.689339   426596.93
176  2008年02月份  13370.18  152.665137  829.976560   415859.25
177  2008年01月份   1437.69  -72.142704  -59.893939   402489.07
```
