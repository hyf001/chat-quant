---
title: "stock_lhb_traderstatistic_em - 营业部统计"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_lhb_traderstatistic_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 营业部详情数据-东财 > 营业部统计
- 描述: 东方财富网-数据中心-龙虎榜单-营业部统计
- 目标地址: https://data.eastmoney.com/stock/traderstatistic.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 营业部统计

接口: stock_lhb_traderstatistic_em

目标地址: https://data.eastmoney.com/stock/traderstatistic.html

描述: 东方财富网-数据中心-龙虎榜单-营业部统计

限量: 单次返回所有历史数据

输入参数

| 名称     | 类型  | 描述                                                   |
|--------|-----|------------------------------------------------------|
| symbol | str | symbol="近一月"; choice of {"近一月", "近三月", "近六月", "近一年"} |

输出参数

| 名称      | 类型      | 描述      |
|---------|---------|---------|
| 序号      | int64   | -       |
| 营业部名称   | object  | -       |
| 龙虎榜成交金额 | float64 | -       |
| 上榜次数    | int64   | -       |
| 买入额     | float64 | 注意单位: 元 |
| 买入次数    | int64   | -       |
| 卖出额     | float64 | 注意单位: 元 |
| 卖出次数    | int64   | -       |

接口示例

```python
import akshare as ak

stock_lhb_traderstatistic_em_df = ak.stock_lhb_traderstatistic_em(symbol="近一月")
print(stock_lhb_traderstatistic_em_df)
```

数据示例

```
    序号                     营业部名称       龙虎榜成交金额  ...  买入次数           卖出额  卖出次数
0        1                     深股通专用  2.143017e+10  ...   269  1.116966e+10   269
1        2     华宝证券股份有限公司上海东大名路证券营业部  1.043461e+10  ...    46  5.103830e+09    42
2        3           华鑫证券有限责任公司上海分公司  7.489912e+09  ...   180  3.422379e+09   155
3        4    国泰君安证券股份有限公司成都双庆路证券营业部  7.023039e+09  ...    14  3.509692e+09    13
4        5                     沪股通专用  6.663151e+09  ...    96  3.758107e+09   107
...    ...                       ...           ...  ...   ...           ...   ...
1620  1621    中信建投证券股份有限公司锦州解放路证券营业部  1.794000e+04  ...     1  0.000000e+00     0
1621  1622      中信证券股份有限公司如皋福寿路证券营业部  1.346730e+04  ...     1  0.000000e+00     0
1622  1623  申万宏源证券有限公司上海浦东新区沪南路证券营业部  1.178100e+04  ...     1  0.000000e+00     0
1623  1624      华泰证券股份有限公司沈阳光荣街证券营业部  1.155000e+04  ...     1  0.000000e+00     0
1624  1625      国信证券股份有限公司天津友谊路证券营业部  6.560000e+02  ...     1  0.000000e+00     0
[1625 rows x 8 columns]
```
