---
title: "macro_global_sox_index - 费城半导体指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_global_sox_index

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 费城半导体指数
- 描述: 费城半导体指数数据, 数据区间从 19940504-至今
- 目标地址: https://data.eastmoney.com/cjsj/hyzs_list_EMI00055562.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 费城半导体指数

接口: macro_global_sox_index

目标地址: https://data.eastmoney.com/cjsj/hyzs_list_EMI00055562.html

描述: 费城半导体指数数据, 数据区间从 19940504-至今

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

macro_global_sox_index_df = ak.macro_global_sox_index()
print(macro_global_sox_index_df)
```

数据示例

```
         日期     最新值    涨跌幅  ...     近1年涨跌幅   近2年涨跌幅      近3年涨跌幅
0     1994-05-04   119.0       NaN  ...        NaN         NaN         NaN
1     1994-05-05   118.3 -0.588235  ...        NaN         NaN         NaN
2     1994-05-06   117.7 -0.507185  ...        NaN         NaN         NaN
3     1994-05-09   115.6 -1.784197  ...        NaN         NaN         NaN
4     1994-05-10   117.4  1.557093  ...        NaN         NaN         NaN
          ...     ...       ...  ...        ...         ...         ...
6957  2022-03-25  3525.3 -0.209472  ...  19.102801  139.397788  154.948472
6958  2022-03-28  3547.2  0.621224  ...  14.194471  138.267003  158.203523
6959  2022-03-29  3625.6  2.210194  ...  18.691953  143.533165  159.804659
6960  2022-03-30  3508.6 -3.227052  ...  15.241990  127.048295  151.420628
6961  2022-03-31  3429.0 -2.268711  ...   9.730107  126.997398  145.716620
```
