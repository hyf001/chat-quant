---
title: "macro_china_bdti_index - 原油运输指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_bdti_index

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 原油运输指数
- 描述: 原油运输指数数据, 数据区间从 20011227-至今
- 目标地址: https://data.eastmoney.com/cjsj/hyzs_list_EMI00107668.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 原油运输指数

接口: macro_china_bdti_index

目标地址: https://data.eastmoney.com/cjsj/hyzs_list_EMI00107668.html

描述: 原油运输指数数据, 数据区间从 20011227-至今

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

macro_china_bdti_index_df = ak.macro_china_bdti_index()
print(macro_china_bdti_index_df)
```

数据示例

```
           日期   最新值   涨跌幅  ...      近1年涨跌幅     近2年涨跌幅      近3年涨跌幅
0     2001-12-27   849       NaN  ...         NaN        NaN         NaN
1     2001-12-28   850  0.117786  ...         NaN        NaN         NaN
2     2002-01-02   845 -0.588235  ...         NaN        NaN         NaN
3     2002-01-03   826 -2.248521  ...         NaN        NaN         NaN
4     2002-01-04   811 -1.815981  ...         NaN        NaN         NaN
          ...   ...       ...  ...         ...        ...         ...
4921  2022-04-05  1469  7.304602  ...  110.157368   6.218366  138.087520
4922  2022-04-06  1547  5.309735  ...  125.839416  24.758065  150.729335
4923  2022-04-07  1653  6.851972  ...  144.888889  47.326203  167.909238
4924  2022-04-08  1677  1.451906  ...  154.863222  56.582633  174.918033
4925  2022-04-11  1730  3.160405  ...  167.801858  55.296230  172.870662
```
