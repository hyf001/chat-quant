---
title: "stock_margin_szse - 融资融券汇总"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_margin_szse

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 融资融券 > 深圳证券交易所 > 融资融券汇总
- 描述: 深圳证券交易所-融资融券数据-融资融券汇总数据
- 目标地址: https://www.szse.cn/disclosure/margin/margin/index.html
- 限量: 单次返回指定时间内的所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 融资融券汇总

接口: stock_margin_szse

目标地址: https://www.szse.cn/disclosure/margin/margin/index.html

描述: 深圳证券交易所-融资融券数据-融资融券汇总数据

限量: 单次返回指定时间内的所有历史数据

输入参数

| 名称   | 类型  | 描述                    |
|------|-----|-----------------------|
| date | str | date="20240411"; 交易日期 |

输出参数

| 名称     | 类型      | 描述          |
|--------|---------|-------------|
| 融资买入额  | float64 | 注意单位: 亿元    |
| 融资余额   | float64 | 注意单位: 亿元    |
| 融券卖出量  | float64 | 注意单位: 亿股/亿份 |
| 融券余量   | float64 | 注意单位: 亿股/亿份 |
| 融券余额   | float64 | 注意单位: 亿元    |
| 融资融券余额 | float64 | 注意单位: 亿元    |

接口示例

```python
import akshare as ak

stock_margin_sse_df = ak.stock_margin_szse(date="20240411")
print(stock_margin_sse_df)
```

数据示例

```
    融资买入额     融资余额  融券卖出量   融券余量   融券余额   融资融券余额
0  321.08  7077.67   0.28  24.34  157.3  7234.97
```
