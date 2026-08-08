---
title: "macro_china_bank_financing - 银行理财产品发行数量"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_bank_financing

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 银行理财产品发行数量
- 描述: 银行理财产品发行数量, 数据区间从 2000 一月-至今
- 目标地址: https://data.eastmoney.com/cjsj/hyzs_list_EMI01516267.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 银行理财产品发行数量

接口: macro_china_bank_financing

目标地址: https://data.eastmoney.com/cjsj/hyzs_list_EMI01516267.html

描述: 银行理财产品发行数量, 数据区间从 2000 一月-至今

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

macro_china_bank_financing_df = ak.macro_china_bank_financing()
print(macro_china_bank_financing_df)
```

数据示例

```
        日期   最新值         涨跌幅  ...   近1年涨跌幅   近2年涨跌幅  近3年涨跌幅
0    2000-03-01     4         NaN  ...         NaN         NaN         NaN
1    2004-02-01     2  -50.000000  ...  -50.000000  -50.000000  -50.000000
2    2004-03-01     8  300.000000  ...  100.000000  100.000000  100.000000
3    2004-04-01     3  -62.500000  ...  -25.000000  -25.000000  -25.000000
4    2004-05-01     6  100.000000  ...   50.000000   50.000000   50.000000
..          ...   ...         ...  ...         ...         ...         ...
213  2021-10-01  2640  -27.829415  ...  -51.710262  -70.054446  -74.346516
214  2021-11-01  3424   29.696970  ...  -45.347167  -59.541534  -70.644719
215  2021-12-01  3876   13.200935  ...  -44.422139  -44.117647  -64.904020
216  2022-01-01  2793  -27.941176  ...  -45.406568  -50.478723  -77.035027
217  2022-02-01  1779  -36.305048  ...  -54.893509  -66.204407  -78.496313
```
