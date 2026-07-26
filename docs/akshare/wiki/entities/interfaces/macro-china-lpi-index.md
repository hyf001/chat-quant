---
title: "macro_china_lpi_index - 物流景气指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_lpi_index

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 物流景气指数
- 描述: 物流景气指数数据, 数据区间从 20130701-至今
- 目标地址: https://data.eastmoney.com/cjsj/hyzs_list_EMI00352262.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 物流景气指数

接口: macro_china_lpi_index

目标地址: https://data.eastmoney.com/cjsj/hyzs_list_EMI00352262.html

描述: 物流景气指数数据, 数据区间从 20130701-至今

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

macro_china_lpi_index_df = ak.macro_china_lpi_index()
print(macro_china_lpi_index_df)
```

数据示例

```
         日期   最新值   涨跌幅  ...    近1年涨跌幅   近2年涨跌幅 近3年涨跌幅
0    2013-07-01  52.4       NaN  ...       NaN        NaN       NaN
1    2013-08-01  52.9  0.954198  ...       NaN        NaN       NaN
2    2013-09-01  53.3  0.756144  ...       NaN        NaN       NaN
3    2013-10-01  53.6  0.562852  ...       NaN        NaN       NaN
4    2013-11-01  53.0 -1.119403  ...       NaN        NaN       NaN
..          ...   ...       ...  ...       ...        ...       ...
100  2021-11-01  53.6  0.186916  ... -6.782609  -8.998302  7.200000
101  2021-12-01  52.6 -1.865672  ... -7.557118 -10.238908 -3.839122
102  2022-01-01  51.1 -2.851711  ... -6.066176   2.404810 -4.841713
103  2022-02-01  51.2  0.195695  ...  2.811245  95.419847  3.225806
104  2022-03-01  48.7 -4.882812  ... -6.165703  -5.436893 -7.414449
```
