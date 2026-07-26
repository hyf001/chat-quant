---
title: "stock_zygc_em - 主营构成-东财"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_zygc_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 主营构成-东财
- 描述: 东方财富网-个股-主营构成
- 目标地址: https://emweb.securities.eastmoney.com/PC_HSF10/BusinessAnalysis/Index?type=web&code=SH688041#
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

### 主营构成-东财

接口: stock_zygc_em

目标地址: https://emweb.securities.eastmoney.com/PC_HSF10/BusinessAnalysis/Index?type=web&code=SH688041#

描述: 东方财富网-个股-主营构成

限量: 单次返回所有历史数据

输入参数

| 名称     | 类型  | 描述                |
|--------|-----|-------------------|
| symbol | str | symbol="SH688041" |

输出参数

| 名称   | 类型      | 描述      |
|------|---------|---------|
| 股票代码 | object  | -       |
| 报告日期 | object  | -       |
| 分类类型 | object  | -       |
| 主营构成 | int64   | -       |
| 主营收入 | float64 | 注意单位: 元 |
| 收入比例 | float64 | -       |
| 主营成本 | float64 | 注意单位: 元 |
| 成本比例 | float64 | -       |
| 主营利润 | float64 | 注意单位: 元 |
| 利润比例 | float64 | -       |
| 毛利率  | float64 | -       |

接口示例

```python
import akshare as ak

stock_zygc_em_df = ak.stock_zygc_em(symbol="SH688041")
print(stock_zygc_em_df)
```

数据示例

```
    股票代码  报告日期   分类类型  ...      主营利润      利润比例       毛利率
0   688041  2024-06-30  按产品分类  ...  2.385020e+09  0.999313  0.634303
1   688041  2024-06-30  按产品分类  ...  1.639645e+06  0.000687  0.575505
2   688041  2024-06-30  按地区分类  ...  2.386659e+09  1.000000  0.634259
3   688041  2023-12-31  按行业分类  ...  3.587141e+09  0.999963  0.596682
4   688041  2023-12-31  按行业分类  ...  1.337029e+05  0.000037  0.708626
..     ...         ...    ...  ...           ...       ...       ...
60  688041  2018-12-31  按产品分类  ...  3.538980e+07  0.874818  0.841592
61  688041  2018-12-31  按产品分类  ...  4.352600e+06  0.107594  0.792982
62  688041  2018-12-31  按产品分类  ...           NaN       NaN       NaN
63  688041  2018-12-31  按地区分类  ...           NaN       NaN       NaN
64  688041  2018-12-31  按地区分类  ...           NaN       NaN       NaN
[65 rows x 11 columns]
```
