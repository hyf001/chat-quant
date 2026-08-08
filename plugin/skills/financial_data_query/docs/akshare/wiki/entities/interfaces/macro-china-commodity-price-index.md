---
title: "macro_china_commodity_price_index - 大宗商品价格"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_commodity_price_index

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 大宗商品价格
- 描述: 大宗商品价格数据, 数据区间从 20111205-至今
- 目标地址: https://data.eastmoney.com/cjsj/hyzs_list_EMI00662535.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 大宗商品价格

接口: macro_china_commodity_price_index

目标地址: https://data.eastmoney.com/cjsj/hyzs_list_EMI00662535.html

描述: 大宗商品价格数据, 数据区间从 20111205-至今

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

macro_china_commodity_price_index_df = ak.macro_china_commodity_price_index()
print(macro_china_commodity_price_index_df)
```

数据示例

```
          日期   最新值    涨跌幅  ...     近1年涨跌幅   近2年涨跌幅   近3年涨跌幅
0     2011-12-05   999       NaN  ...        NaN        NaN        NaN
1     2011-12-12   991 -0.800801  ...        NaN        NaN        NaN
2     2011-12-19   990 -0.100908  ...        NaN        NaN        NaN
3     2011-12-26   988 -0.202020  ...        NaN        NaN        NaN
4     2012-01-02   992  0.404858  ...        NaN        NaN        NaN
          ...   ...       ...  ...        ...        ...        ...
2975  2022-03-31  1213  0.000000  ...  21.543086  68.005540  40.556199
2976  2022-04-01  1212 -0.082440  ...  20.958084  69.037657  40.277778
2977  2022-04-02  1212  0.000000  ...  20.717131  70.224719  40.440324
2978  2022-04-03  1212  0.000000  ...  20.837488  70.464135  40.440324
2979  2022-04-04  1212  0.000000  ...  20.837488  70.704225  40.440324
```
