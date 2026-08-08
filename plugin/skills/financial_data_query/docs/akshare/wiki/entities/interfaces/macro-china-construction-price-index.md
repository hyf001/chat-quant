---
title: "macro_china_construction_price_index - 建材价格指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_construction_price_index

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 建材价格指数
- 描述: 建材价格指数数据, 数据区间从 20100615-至今
- 目标地址: https://data.eastmoney.com/cjsj/hyzs_list_EMI00237146.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 建材价格指数

接口: macro_china_construction_price_index

目标地址: https://data.eastmoney.com/cjsj/hyzs_list_EMI00237146.html

描述: 建材价格指数数据, 数据区间从 20100615-至今

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

macro_china_construction_price_index_df = ak.macro_china_construction_price_index()
print(macro_china_construction_price_index_df)
```

数据示例

```
       日期        最新值    涨跌幅  ...    近1年涨跌幅   近2年涨跌幅  近3年涨跌幅
0     2010-06-15  1230.40       NaN  ...       NaN       NaN       NaN
1     2010-06-16  1245.10  1.194733  ...       NaN       NaN       NaN
2     2010-08-01  1281.60  2.931491  ...       NaN       NaN       NaN
3     2010-08-02  1214.90 -5.204432  ...       NaN       NaN       NaN
4     2010-08-03  1218.90  0.329245  ...       NaN       NaN       NaN
          ...      ...       ...  ...       ...       ...       ...
3841  2022-02-25  1099.01  1.567395  ...  1.467995  1.493295  2.177410
3842  2022-02-26  1088.05 -0.997261  ...  0.456094  0.481142  1.521824
3843  2022-02-27  1097.41  0.860255  ...  1.120479  1.345536  2.198733
3844  2022-02-28  1088.05 -0.852917  ...  0.977244  0.481142  1.549302
3845  2022-03-01  1097.41  0.860255  ...  1.419528  0.749139  2.051425
```
