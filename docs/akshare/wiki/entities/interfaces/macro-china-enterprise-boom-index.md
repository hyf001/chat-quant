---
title: "macro_china_enterprise_boom_index - 企业景气及企业家信心指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_enterprise_boom_index

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 企业景气及企业家信心指数
- 描述: 中国企业景气及企业家信心指数数据, 数据区间从 2005 一季度-至今
- 目标地址: http://data.eastmoney.com/cjsj/qyjqzs.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 企业景气及企业家信心指数

接口: macro_china_enterprise_boom_index

目标地址: http://data.eastmoney.com/cjsj/qyjqzs.html

描述: 中国企业景气及企业家信心指数数据, 数据区间从 2005 一季度-至今

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称         | 类型      | 描述      |
|------------|---------|---------|
| 季度         | object  | 日期      |
| 企业景气指数-指数  | float64 | -       |
| 企业景气指数-同比  | float64 | 注意单位: % |
| 企业景气指数-环比  | float64 | 注意单位: % |
| 企业家信心指数-指数 | float64 | -       |
| 企业家信心指数-同比 | float64 | 注意单位: % |
| 企业家信心指数-环比 | float64 | 注意单位: % |

接口示例

```python
import akshare as ak

macro_china_enterprise_boom_index_df = ak.macro_china_enterprise_boom_index()
print(macro_china_enterprise_boom_index_df)
```

数据示例

```
           季度  企业景气指数-指数  企业景气指数-同比  ...  企业家信心指数-指数  企业家信心指数-同比  企业家信心指数-环比
0   2022年第2季度     101.80       1.80  ...         NaN         NaN         NaN
1   2022年第1季度     112.70      12.70  ...         NaN         NaN         NaN
2   2021年第4季度     119.20      19.20  ...         NaN         NaN         NaN
3   2021年第3季度     119.20      19.20  ...      120.90       20.90       -5.10
4   2021年第2季度     123.80      23.80  ...      126.00       26.00       -1.80
..        ...        ...        ...  ...         ...         ...         ...
65  2006年第1季度     131.50      31.50  ...      133.10       33.10        7.70
66  2005年第4季度     131.70      31.70  ...      125.40       25.40       -2.20
67  2005年第3季度     132.00      32.00  ...      127.60       27.60       -0.90
68  2005年第2季度     131.71      31.71  ...      128.50       28.50       -7.35
69  2005年第1季度     132.46      32.46  ...      135.85       35.85        5.04
```
