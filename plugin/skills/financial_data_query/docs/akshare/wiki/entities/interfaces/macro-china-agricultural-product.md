---
title: "macro_china_agricultural_product - 农产品批发价格总指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_agricultural_product

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 农产品批发价格总指数
- 描述: 农产品批发价格总指数, 数据区间从 20050927-至今
- 目标地址: https://data.eastmoney.com/cjsj/hyzs_list_EMI00009274.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 农产品批发价格总指数

接口: macro_china_agricultural_product

目标地址: https://data.eastmoney.com/cjsj/hyzs_list_EMI00009274.html

描述: 农产品批发价格总指数, 数据区间从 20050927-至今

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

macro_china_agricultural_product_df = ak.macro_china_agricultural_product()
print(macro_china_agricultural_product_df)
```

数据示例

```
          日期     最新值    涨跌幅  ...    近1年涨跌幅  近2年涨跌幅  近3年涨跌幅
0     2005-09-27  125.50       NaN  ...       NaN       NaN        NaN
1     2005-09-28  125.00 -0.398406  ...       NaN       NaN        NaN
2     2005-09-29  125.00  0.000000  ...       NaN       NaN        NaN
3     2005-09-30  125.80  0.640000  ...       NaN       NaN        NaN
4     2005-10-08  124.20 -1.271860  ...       NaN       NaN        NaN
          ...     ...       ...  ...       ...       ...        ...
4100  2022-03-28  134.83  0.499404  ...  6.349582  7.374373  15.259019
4101  2022-03-29  135.30  0.348587  ...  7.100451  7.748666  15.492958
4102  2022-03-30  135.03 -0.199557  ...  7.098668  8.127803  15.262484
4103  2022-03-31  136.10  0.792416  ...  8.265054  8.862582  16.175843
4104  2022-04-01  136.38  0.205731  ...  8.790683  9.156395  16.176846
```
