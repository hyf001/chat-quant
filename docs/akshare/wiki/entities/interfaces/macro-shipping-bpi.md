---
title: "macro_shipping_bpi - 巴拿马型运费指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_shipping_bpi

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 巴拿马型运费指数
- 描述: 巴拿马型运费指数, 数据区间从 19981231-至今
- 目标地址: https://data.eastmoney.com/cjsj/hyzs_list_EMI00107665.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 巴拿马型运费指数

接口: macro_shipping_bpi

目标地址: https://data.eastmoney.com/cjsj/hyzs_list_EMI00107665.html

描述: 巴拿马型运费指数, 数据区间从 19981231-至今

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

macro_shipping_bpi_df = ak.macro_shipping_bpi()
print(macro_shipping_bpi_df)
```

数据示例

```
     日期   最新值       涨跌幅  ...     近1年涨跌幅     近2年涨跌幅     近3年涨跌幅
0     1998-12-31   732       NaN  ...        NaN        NaN        NaN
1     1999-01-04   717 -2.049180  ...        NaN        NaN        NaN
2     1999-01-05   709 -1.115760  ...        NaN        NaN        NaN
3     1999-01-06   729  2.820874  ...        NaN        NaN        NaN
4     1999-01-07   734  0.685871  ...        NaN        NaN        NaN
          ...   ...       ...  ...        ...        ...        ...
5951  2023-03-03  1565  0.578406  ... -42.015561 -27.579824  67.379679
5952  2023-03-06  1582  1.086262  ... -43.195691 -29.406515  48.127341
5953  2023-03-07  1580 -0.126422  ... -45.536022 -29.495761  47.940075
5954  2023-03-08  1592  0.759494  ... -47.648800 -29.495128  49.063670
5955  2023-03-09  1624  2.010050  ... -49.154665 -27.435210  52.202437
```
