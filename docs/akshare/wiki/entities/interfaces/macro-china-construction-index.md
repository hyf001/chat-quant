---
title: "macro_china_construction_index - 建材指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_construction_index

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 建材指数
- 描述: 建材指数数据, 数据区间从 20111205-至今
- 目标地址: https://data.eastmoney.com/cjsj/hyzs_list_EMI00662541.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 建材指数

接口: macro_china_construction_index

目标地址: https://data.eastmoney.com/cjsj/hyzs_list_EMI00662541.html

描述: 建材指数数据, 数据区间从 20111205-至今

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

macro_china_construction_index_df = ak.macro_china_construction_index()
print(macro_china_construction_index_df)
```

数据示例

```
         日期   最新值       涨跌幅  ...    近1年涨跌幅     近2年涨跌幅     近3年涨跌幅
0     2011-12-05  1014       NaN  ...       NaN        NaN        NaN
1     2011-12-12  1013 -0.098619  ...       NaN        NaN        NaN
2     2011-12-19  1005 -0.789733  ...       NaN        NaN        NaN
3     2011-12-26   993 -1.194030  ...       NaN        NaN        NaN
4     2012-01-02   991 -0.201410  ...       NaN        NaN        NaN
          ...   ...       ...  ...       ...        ...        ...
3179  2024-03-31   962  0.000000  ... -8.901515 -25.077882 -23.285486
3180  2024-04-01   958 -0.415800  ... -9.280303 -25.505443 -23.726115
3181  2024-04-02   960  0.208768  ... -9.090909 -25.407925 -24.170616
3182  2024-04-03   960  0.000000  ... -9.176916 -25.407925 -24.170616
3183  2024-04-04   960  0.000000  ... -8.745247 -25.407925 -24.170616
[3184 rows x 8 columns]
```
