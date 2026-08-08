---
title: "macro_shipping_bci - 海岬型运费指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_shipping_bci

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 海岬型运费指数
- 描述: 海岬型运费指数, 数据区间从 19990430-至今
- 目标地址: https://data.eastmoney.com/cjsj/hyzs_list_EMI00107666.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 海岬型运费指数

接口: macro_shipping_bci

目标地址: https://data.eastmoney.com/cjsj/hyzs_list_EMI00107666.html

描述: 海岬型运费指数, 数据区间从 19990430-至今

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

macro_shipping_bci_df = ak.macro_shipping_bci()
print(macro_shipping_bci_df)
```

数据示例

```
      日期   最新值   涨跌幅  ...     近1年涨跌幅     近2年涨跌幅      近3年涨跌幅
0     1999-04-30   940        NaN  ...        NaN        NaN         NaN
1     1999-05-04   947   0.744681  ...        NaN        NaN         NaN
2     1999-05-05   960   1.372756  ...        NaN        NaN         NaN
3     1999-05-06   969   0.937500  ...        NaN        NaN         NaN
4     1999-05-07   981   1.238390  ...        NaN        NaN         NaN
          ...   ...        ...  ...        ...        ...         ...
5988  2023-03-03  1195  19.500000  ... -27.089689 -28.741801  445.375723
5989  2023-03-06  1329  11.213389  ... -18.715596 -25.504484  525.961538
5990  2023-03-07  1471  10.684725  ... -15.894797 -17.544843  571.474359
5991  2023-03-08  1550   5.370496  ... -18.248945 -15.068493  596.794872
5992  2023-03-09  1662   7.225806  ... -27.169150 -14.769231  546.774194
```
