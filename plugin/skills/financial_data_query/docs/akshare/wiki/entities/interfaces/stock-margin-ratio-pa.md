---
title: "stock_margin_ratio_pa - 标的证券名单及保证金比例查询"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_margin_ratio_pa

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 融资融券 > 标的证券名单及保证金比例查询
- 描述: 融资融券-标的证券名单及保证金比例查询
- 目标地址: https://stock.pingan.com/static/webinfo/margin/business.html?businessType=0
- 限量: 单次返回指定交易所和交易日的所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 标的证券名单及保证金比例查询

接口: stock_margin_ratio_pa

目标地址: https://stock.pingan.com/static/webinfo/margin/business.html?businessType=0

描述: 融资融券-标的证券名单及保证金比例查询

限量: 单次返回指定交易所和交易日的所有历史数据

输入参数

| 名称     | 类型  | 描述                                         |
|--------|-----|--------------------------------------------|
| symbol | str | symbol="深市"; choice of {"深市", "沪市", "北交所"} |
| date   | str | date="20260113"                            |

输出参数

| 名称   | 类型      | 描述 |
|------|---------|----|
| 证券代码 | object  | -  |
| 证券简称 | object  | -  |
| 融资比例 | float64 | -  |
| 融券比例 | float64 | -  |

接口示例

```python
import akshare as ak

stock_margin_ratio_pa_df = ak.stock_margin_ratio_pa(symbol="沪市", date="20260113")
print(stock_margin_ratio_pa_df)
```

数据示例

```
      证券代码   证券简称  融资比例 融券比例
0     510050    50ETF   0.8   1.0
1     510100  SZ50ETF   0.8   1.0
2     510150    消费ETF   0.8   1.0
3     510180   180ETF   0.8   1.0
4     510210    综指ETF   0.8   1.0
...      ...      ...   ...   ...
1950  688807     优迅股份   1.0   1.8
1951  688809     强一股份   1.0   1.8
1952  688819     天能股份   0.8   1.5
1953  688981     中芯国际   0.8   1.5
1954  689009     九号公司   1.3   1.5
[1955 rows x 4 columns]
```
