---
title: "macro_china_energy_index - 能源指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_energy_index

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 能源指数
- 描述: 能源指数数据, 数据区间从 20111205-至今
- 目标地址: https://data.eastmoney.com/cjsj/hyzs_list_EMI00662539.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 能源指数

接口: macro_china_energy_index

目标地址: https://data.eastmoney.com/cjsj/hyzs_list_EMI00662539.html

描述: 能源指数数据, 数据区间从 20111205-至今

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

macro_china_energy_index_df = ak.macro_china_energy_index()
print(macro_china_energy_index_df)
```

数据示例

```
         日期   最新值    涨跌幅  ...     近1年涨跌幅    近2年涨跌幅  近3年涨跌幅
0     2011-12-05  1003       NaN  ...        NaN        NaN        NaN
1     2011-12-12   995 -0.797607  ...        NaN        NaN        NaN
2     2011-12-19   987 -0.804020  ...        NaN        NaN        NaN
3     2011-12-26   983 -0.405268  ...        NaN        NaN        NaN
4     2012-01-02   984  0.101729  ...        NaN        NaN        NaN
          ...   ...       ...  ...        ...        ...        ...
2972  2022-03-29  1208 -0.247729  ...  48.220859  84.992343  48.768473
2973  2022-03-30  1206 -0.165563  ...  47.252747  88.437500  48.522167
2974  2022-03-31  1207  0.082919  ...  47.735618  90.378549  48.645320
2975  2022-04-01  1207  0.000000  ...  48.098160  91.283677  48.828607
2976  2022-04-02  1208  0.082850  ...  47.858017  91.442155  47.858017
```
