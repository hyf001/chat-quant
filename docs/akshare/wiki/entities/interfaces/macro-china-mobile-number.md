---
title: "macro_china_mobile_number - 手机出货量"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_mobile_number

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 手机出货量
- 描述: 手机出货量, 数据区间从 201201-至今
- 目标地址: https://data.eastmoney.com/cjsj/hyzs_list_EMI00225823.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 手机出货量

接口: macro_china_mobile_number

目标地址: https://data.eastmoney.com/cjsj/hyzs_list_EMI00225823.html

描述: 手机出货量, 数据区间从 201201-至今

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

macro_china_mobile_number_df = ak.macro_china_mobile_number()
print(macro_china_mobile_number_df)
```

数据示例

```
        日期     最新值     涨跌幅  ...     近1年涨跌幅      近2年涨跌幅     近3年涨跌幅
0    2012-01-01  2400.6        NaN  ...        NaN         NaN        NaN
1    2012-02-01  2998.9  24.922936  ...        NaN         NaN        NaN
2    2012-03-01  3958.6  32.001734  ...        NaN         NaN        NaN
3    2012-04-01  3528.7 -10.859900  ...        NaN         NaN        NaN
4    2012-05-01  3586.8   1.646499  ...        NaN         NaN        NaN
..          ...     ...        ...  ...        ...         ...        ...
117  2021-10-01  3357.5  56.599813  ...  28.379153   -6.655731 -12.866893
118  2021-11-01  3525.2   4.994788  ...  19.159005    1.176741  -0.333616
119  2021-12-01  3340.1  -5.250766  ...  25.591277    9.712916  -6.371587
120  2022-01-01  3302.2  -1.134697  ... -17.691924   58.660453  -3.013393
121  2022-02-01  1486.4 -54.987584  ... -31.688037  132.832080   2.432637
```
