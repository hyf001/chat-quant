---
title: "stock_margin_bse - 融资融券汇总"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_margin_bse

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 融资融券 > 北京证券交易所 > 融资融券汇总
- 描述: 北京证券交易所-融资融券数据-融资融券汇总数据
- 目标地址: https://www.bse.cn/disclosure/rzrq_trans_list.html
- 限量: 单次返回指定交易日的汇总数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 融资融券汇总

接口: stock_margin_bse

目标地址: https://www.bse.cn/disclosure/rzrq_trans_list.html

描述: 北京证券交易所-融资融券数据-融资融券汇总数据

限量: 单次返回指定交易日的汇总数据

输入参数

| 名称   | 类型  | 描述                    |
|------|-----|-----------------------|
| date | str | date="20260721"; 交易日期 |

输出参数

| 名称     | 类型      | 描述        |
|--------|---------|-----------|
| 融资买入额  | float64 | 注意单位: 万元 |
| 融资余额   | float64 | 注意单位: 万元 |
| 融券卖出量  | float64 | 注意单位: 万股 |
| 融券余量   | float64 | 注意单位: 万股 |
| 融券余额   | float64 | 注意单位: 万元 |
| 融资融券余额 | float64 | 注意单位: 万元 |

接口示例

```python
import akshare as ak

stock_margin_bse_df = ak.stock_margin_bse(date="20260721")
print(stock_margin_bse_df)
```

数据示例

```
    融资买入额      融资余额  融券卖出量  融券余量   融券余额   融资融券余额
0  57368.45  835758.44    1.3   1.3  23.28  835781.73
```
