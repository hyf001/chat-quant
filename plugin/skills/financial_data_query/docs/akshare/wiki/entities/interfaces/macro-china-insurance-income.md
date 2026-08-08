---
title: "macro_china_insurance_income - 原保险保费收入"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_insurance_income

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 原保险保费收入
- 描述: 原保险保费收入, 数据区间从 200407-至今
- 目标地址: https://data.eastmoney.com/cjsj/hyzs_list_EMM00088870.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 原保险保费收入

接口: macro_china_insurance_income

目标地址: https://data.eastmoney.com/cjsj/hyzs_list_EMM00088870.html

描述: 原保险保费收入, 数据区间从 200407-至今

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称     | 类型      | 描述      |
|--------|---------|---------|
| 日期     | object  | -       |
| 最新值    | int64   | -       |
| 涨跌幅    | float64 | 注意单位: % |
| 近3月涨跌幅 | float64 | 注意单位: % |
| 近6月涨跌幅 | float64 | 注意单位: % |
| 近1年涨跌幅 | float64 | 注意单位: % |
| 近2年涨跌幅 | float64 | 注意单位: % |
| 近3年涨跌幅 | float64 | 注意单位: % |

接口示例

```python
import akshare as ak

macro_china_insurance_income_df = ak.macro_china_insurance_income()
print(macro_china_insurance_income_df)
```

数据示例

```
      日期        最新值        涨跌幅  ...    近1年涨跌幅    近2年涨跌幅     近3年涨跌幅
0    2004-07-01  0.000000e+00        NaN  ...       NaN       NaN        NaN
1    2004-09-01  2.453616e+07        NaN  ...       NaN       NaN        NaN
2    2004-10-01  2.704315e+07  10.217507  ...       NaN       NaN        NaN
3    2004-11-01  2.956397e+07   9.321471  ...       NaN       NaN        NaN
4    2004-12-01  3.193586e+07   8.022916  ...       NaN       NaN        NaN
..          ...           ...        ...  ...       ...       ...        ...
205  2021-09-01  1.979124e+08   9.327015  ... -1.959838  2.790277  -9.435956
206  2021-10-01  2.094363e+08   5.822728  ... -2.107731  2.866552 -10.337719
207  2021-11-01  2.205047e+08   5.284853  ... -2.053675  2.876131 -11.053454
208  2021-12-01  2.357184e+08   6.899490  ... -1.710283  3.594269 -10.239691
209  2022-01-01  7.049640e+07 -70.092958  ... -5.768089  5.429366  12.398597
```
