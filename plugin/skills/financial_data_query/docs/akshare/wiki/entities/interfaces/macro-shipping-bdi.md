---
title: "macro_shipping_bdi - 波罗的海干散货指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_shipping_bdi

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 波罗的海干散货指数
- 描述: 波罗的海干散货指数, 数据区间从 19881019-至今
- 目标地址: https://data.eastmoney.com/cjsj/hyzs_list_EMI00107664.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 波罗的海干散货指数

接口: macro_shipping_bdi

目标地址: https://data.eastmoney.com/cjsj/hyzs_list_EMI00107664.html

描述: 波罗的海干散货指数, 数据区间从 19881019-至今

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

macro_shipping_bdi_df = ak.macro_shipping_bdi()
print(macro_shipping_bdi_df)
```

数据示例

```
      日期   最新值    涨跌幅  ...     近1年涨跌幅     近2年涨跌幅      近3年涨跌幅
0     1988-10-19  1317       NaN  ...        NaN        NaN         NaN
1     1988-10-20  1316 -0.075930  ...        NaN        NaN         NaN
2     1988-10-21  1328  0.911854  ...        NaN        NaN         NaN
3     1988-10-24  1361  2.484940  ...        NaN        NaN         NaN
4     1988-10-25  1363  0.146951  ...        NaN        NaN         NaN
          ...   ...       ...  ...        ...        ...         ...
8577  2023-03-03  1211  5.764192  ... -42.442966 -31.310267  120.582878
8578  2023-03-06  1258  3.881090  ... -41.433892 -31.219245  103.889789
8579  2023-03-07  1298  3.179650  ... -41.923937 -29.032258  110.372771
8580  2023-03-08  1327  2.234206  ... -43.579932 -28.386400  115.072934
8581  2023-03-09  1379  3.918613  ... -46.090696 -27.459232  123.863636
```
