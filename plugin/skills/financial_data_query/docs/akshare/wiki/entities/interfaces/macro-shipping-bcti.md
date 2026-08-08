---
title: "macro_shipping_bcti - 成品油运输指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_shipping_bcti

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 成品油运输指数
- 描述: 成品油运输指数, 数据区间从 20011217-至今
- 目标地址: https://data.eastmoney.com/cjsj/hyzs_list_EMI00107669.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 成品油运输指数

接口: macro_shipping_bcti

目标地址: https://data.eastmoney.com/cjsj/hyzs_list_EMI00107669.html

描述: 成品油运输指数, 数据区间从 20011217-至今

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

macro_shipping_bcti_df = ak.macro_shipping_bcti()
print(macro_shipping_bcti_df)
```

数据示例

```
    日期  最新值       涨跌幅  ...     近1年涨跌幅     近2年涨跌幅     近3年涨跌幅
0     2001-12-27  693       NaN  ...        NaN        NaN        NaN
1     2001-12-28  691 -0.288600  ...        NaN        NaN        NaN
2     2002-01-02  688 -0.434153  ...        NaN        NaN        NaN
3     2002-01-03  687 -0.145349  ...        NaN        NaN        NaN
4     2002-01-04  687  0.000000  ...        NaN        NaN        NaN
          ...  ...       ...  ...        ...        ...        ...
5148  2023-03-03  789 -1.743462  ... -20.383451  62.012320  22.136223
5149  2023-03-06  782 -0.887199  ... -20.930233  60.245902  14.160584
5150  2023-03-07  784  0.255754  ... -26.797386  60.655738  14.452555
5151  2023-03-08  827  5.484694  ... -21.163012  67.748479  20.729927
5152  2023-03-09  871  5.320435  ... -15.682478  73.161034  21.478382
```
