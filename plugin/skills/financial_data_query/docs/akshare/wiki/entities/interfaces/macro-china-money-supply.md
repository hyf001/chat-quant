---
title: "macro_china_money_supply - 中国货币供应量"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_money_supply

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 中国货币供应量
- 描述: 东方财富-经济数据-中国宏观-中国货币供应量; 数据区间从 200801 至今, 月度数据
- 目标地址: http://data.eastmoney.com/cjsj/hbgyl.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 中国货币供应量

接口: macro_china_money_supply

目标地址: http://data.eastmoney.com/cjsj/hbgyl.html

描述: 东方财富-经济数据-中国宏观-中国货币供应量; 数据区间从 200801 至今, 月度数据

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称                | 类型      | 描述    |
|-------------------|---------|-------|
| 月份                | object  | 年度和月份 |
| 货币和准货币(M2)-数量(亿元) | float64 | -     |
| 货币和准货币(M2)-同比增长   | float64 | -     |
| 货币和准货币(M2)-环比增长   | float64 | -     |
| 货币(M1)-数量(亿元)     | float64 | -     |
| 货币(M1)-同比增长       | float64 | -     |
| 货币(M1)-环比增长       | float64 | -     |
| 流通中的现金(M0)-数量(亿元) | float64 | -     |
| 流通中的现金(M0)-同比增长   | float64 | -     |
| 流通中的现金(M0)-环比增长   | float64 | -     |

接口示例

```python
import akshare as ak

macro_china_money_supply_df = ak.macro_china_money_supply()
print(macro_china_money_supply_df)
```

数据示例

```
            月份  货币和准货币(M2)-数量(亿元)  ...  流通中的现金(M0)-同比增长  流通中的现金(M0)-环比增长
0    2022年10月份         2612914.57  ...            14.30        -0.258787
1    2022年09月份         2626600.92  ...            13.60         1.482068
2    2022年08月份         2595068.27  ...            14.30         0.747950
3    2022年07月份         2578078.57  ...            13.90         0.518710
4    2022年06月份         2581451.20  ...            13.80         0.485950
..         ...                ...  ...              ...              ...
173  2008年05月份          436221.60  ...            12.88        -2.014673
174  2008年04月份          429313.72  ...            10.70         1.171555
175  2008年03月份          423054.53  ...            11.12        -6.228418
176  2008年02月份          421037.84  ...             5.96       -11.503457
177  2008年01月份          417846.17  ...            31.21        20.896562
```
