---
title: "macro_china_bsi_index - 超灵便型船运价指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_bsi_index

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 超灵便型船运价指数
- 描述: 超灵便型船运价指数数据, 数据区间从 20060103-至今
- 目标地址: https://data.eastmoney.com/cjsj/hyzs_list_EMI00107667.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 超灵便型船运价指数

接口: macro_china_bsi_index

目标地址: https://data.eastmoney.com/cjsj/hyzs_list_EMI00107667.html

描述: 超灵便型船运价指数数据, 数据区间从 20060103-至今

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

macro_china_bsi_index_df = ak.macro_china_bsi_index()
print(macro_china_bsi_index_df)
```

数据示例

```
          日期   最新值   涨跌幅  ...     近1年涨跌幅    近2年涨跌幅    近3年涨跌幅
0     2006-01-03  1819       NaN  ...        NaN         NaN         NaN
1     2006-01-05  1825  0.329852  ...        NaN         NaN         NaN
2     2006-01-09  1814 -0.602740  ...        NaN         NaN         NaN
3     2006-01-11  1784 -1.653804  ...        NaN         NaN         NaN
4     2006-01-12  1759 -1.401345  ...        NaN         NaN         NaN
          ...   ...       ...  ...        ...         ...         ...
3984  2022-04-06  2605 -2.067669  ...  44.002211  437.113402  251.078167
3985  2022-04-07  2547 -2.226488  ...  42.131696  439.618644  243.261456
3986  2022-04-08  2502 -1.766784  ...  40.089586  451.101322  241.336971
3987  2022-04-11  2473 -1.159073  ...  38.932584  460.770975  245.874126
3988  2022-04-12  2448 -1.010918  ...  37.993236  455.102041  244.303797
```
