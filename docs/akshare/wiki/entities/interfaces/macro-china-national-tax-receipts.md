---
title: "macro_china_national_tax_receipts - 全国税收收入"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_national_tax_receipts

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 全国税收收入
- 描述: 中国全国税收收入数据, 数据区间从 2005 一季度-至今
- 目标地址: http://data.eastmoney.com/cjsj/nationaltaxreceipts.aspx
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 全国税收收入

接口: macro_china_national_tax_receipts

目标地址: http://data.eastmoney.com/cjsj/nationaltaxreceipts.aspx

描述: 中国全国税收收入数据, 数据区间从 2005 一季度-至今

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称     | 类型      | 描述       |
|--------|---------|----------|
| 季度     | object  | 日期       |
| 税收收入合计 | float64 | 注意单位: 亿元 |
| 较上年同期  | float64 | 注意单位: %  |
| 季度环比   | float64 | -        |

接口示例

```python
import akshare as ak

macro_china_national_tax_receipts_df = ak.macro_china_national_tax_receipts()
print(macro_china_national_tax_receipts_df)
```

数据示例

```
             季度     税收收入合计  较上年同期      季度环比
0   2022年第1-3季度  124365.00  -11.6  0.171811
1   2022年第1-2季度   85564.00  -14.8 -0.368718
2     2022年第1季度   52452.00    7.7  0.637641
3   2021年第1-4季度  172731.00   11.9 -0.204070
4   2021年第1-3季度  140702.00   18.4 -0.222216
..          ...        ...    ...       ...
64  2006年第1-2季度   18484.80   22.0  0.142837
65    2006年第1季度    8626.32   19.0       NaN
66  2005年第1-3季度   21855.35   15.9 -0.151249
67  2005年第1-2季度   15149.73   13.4  0.089860
68    2005年第1季度    7249.16   10.7       NaN
```
