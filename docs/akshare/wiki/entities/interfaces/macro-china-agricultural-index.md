---
title: "macro_china_agricultural_index - 农副指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_agricultural_index

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 农副指数
- 描述: 农副指数数据, 数据区间从 20111205-至今
- 目标地址: https://data.eastmoney.com/cjsj/hyzs_list_EMI00662543.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 农副指数

接口: macro_china_agricultural_index

目标地址: https://data.eastmoney.com/cjsj/hyzs_list_EMI00662543.html

描述: 农副指数数据, 数据区间从 20111205-至今

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

macro_china_agricultural_index_df = ak.macro_china_agricultural_index()
print(macro_china_agricultural_index_df)
```

数据示例

```
          日期   最新值   涨跌幅  ...    近1年涨跌幅   近2年涨跌幅   近3年涨跌幅
0     2011-12-05   995       NaN  ...       NaN        NaN        NaN
1     2011-12-12   986 -0.904523  ...       NaN        NaN        NaN
2     2011-12-19   990  0.405680  ...       NaN        NaN        NaN
3     2011-12-26   988 -0.202020  ...       NaN        NaN        NaN
4     2012-01-02   993  0.506073  ...       NaN        NaN        NaN
          ...   ...       ...  ...       ...        ...        ...
2971  2022-03-28  1316 -0.679245  ...  7.428571  24.385633  55.739645
2972  2022-03-29  1311 -0.379939  ...  7.635468  23.913043  55.331754
2973  2022-03-30  1305 -0.457666  ...  7.495881  22.881356  54.620853
2974  2022-03-31  1303 -0.153257  ...  8.222591  22.347418  54.383886
2975  2022-04-01  1289 -1.074444  ...  6.090535  21.489161  52.906287
```
