---
title: "macro_china_vegetable_basket - 菜篮子产品批发价格指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_vegetable_basket

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 菜篮子产品批发价格指数
- 描述: 菜篮子产品批发价格指数, 数据区间从 20050927-至今
- 目标地址: https://data.eastmoney.com/cjsj/hyzs_list_EMI00009275.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 菜篮子产品批发价格指数

接口: macro_china_vegetable_basket

目标地址: https://data.eastmoney.com/cjsj/hyzs_list_EMI00009275.html

描述: 菜篮子产品批发价格指数, 数据区间从 20050927-至今

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

macro_china_vegetable_basket_df = ak.macro_china_vegetable_basket()
print(macro_china_vegetable_basket_df)
```

数据示例

```
        日期     最新值       涨跌幅  ...    近1年涨跌幅  近2年涨跌幅  近3年涨跌幅
0     2005-09-27  123.80       NaN  ...       NaN       NaN        NaN
1     2005-09-28  123.00 -0.646204  ...       NaN       NaN        NaN
2     2005-09-29  123.10  0.081301  ...       NaN       NaN        NaN
3     2005-09-30  124.10  0.812348  ...       NaN       NaN        NaN
4     2005-10-08  122.20 -1.531023  ...       NaN       NaN        NaN
          ...     ...       ...  ...       ...       ...        ...
4100  2022-03-28  137.93  0.561388  ...  6.026597  6.608440  15.470908
4101  2022-03-29  138.45  0.377003  ...  6.952491  7.010357  15.712495
4102  2022-03-30  138.85  0.288913  ...  7.410846  7.978847  16.046803
4103  2022-03-31  139.38  0.381707  ...  8.180689  8.289954  16.489762
4104  2022-04-01  139.70  0.229588  ...  8.775208  8.622969  16.484616
```
