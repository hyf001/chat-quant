---
title: "macro_china_whxd - 外汇贷款数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_whxd

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 外汇贷款数据
- 描述: 外汇贷款数据, 数据区间从 200802 至今, 月度数据
- 目标地址: http://data.eastmoney.com/cjsj/whxd.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 外汇贷款数据

接口: macro_china_whxd

目标地址: http://data.eastmoney.com/cjsj/whxd.html

描述: 外汇贷款数据, 数据区间从 200802 至今, 月度数据

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称   | 类型      | 描述        |
|------|---------|-----------|
| 月份   | object  | -         |
| 当月   | float64 | 注意单位: 亿美元 |
| 同比增长 | float64 | 注意单位: %   |
| 环比增长 | float64 | 注意单位: %   |
| 累计   | float64 | 注意单位: 亿美元 |

接口示例

```python
import akshare as ak

macro_china_whxd_df = ak.macro_china_whxd()
print(macro_china_whxd_df)
```

数据示例

```
        月份       当月     同比增长   环比增长    累计
0    2008年01月份  169.28  4508.33  1789.29  2367.31
1    2008年02月份  217.02   754.75    28.20  2584.33
2    2008年03月份  103.62   279.28   -52.25  2687.95
3    2008年04月份   21.35    39.82   -79.40  2709.30
4    2008年05月份   30.04   -13.15    40.70  2739.34
..         ...     ...      ...      ...      ...
208  2025年05月份   61.00   191.04   354.17  5394.00
209  2025年06月份  215.00   226.47   252.46  5609.00
210  2025年07月份  -51.00    77.33  -123.72  5558.00
211  2025年08月份  -41.00    61.68    19.61  5517.00
212  2025年09月份   27.00   131.76   165.85  5544.00
[213 rows x 5 columns]
```
