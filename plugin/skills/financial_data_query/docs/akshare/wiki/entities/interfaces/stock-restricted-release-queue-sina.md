---
title: "stock_restricted_release_queue_sina - 个股限售解禁-新浪"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_restricted_release_queue_sina

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 限售解禁 > 个股限售解禁-新浪
- 描述: 新浪财经-发行分配-限售解禁
- 目标地址: https://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/xsjj/index.phtml?symbol=sh600000
- 限量: 单次获取指定 symbol 的限售解禁数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 个股限售解禁-新浪

接口: stock_restricted_release_queue_sina

目标地址: https://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/xsjj/index.phtml?symbol=sh600000

描述: 新浪财经-发行分配-限售解禁

限量: 单次获取指定 symbol 的限售解禁数据

输入参数

| 名称     | 类型  | 描述                    |
|--------|-----|-----------------------|
| symbol | str | symbol="600000"; 股票代码 |

输出参数

| 名称      | 类型      | 描述       |
|---------|---------|----------|
| 代码      | object  | -        |
| 名称      | object  | -        |
| 解禁日期    | object  | -        |
| 解禁数量    | float64 | 注意单位: 万股 |
| 解禁股流通市值 | float64 | 注意单位: 亿元 |
| 上市批次    | int64   | -        |
| 公告日期    | object  | -        |

接口示例

```python
import akshare as ak

stock_restricted_release_queue_sina_df = ak.stock_restricted_release_queue_sina(symbol="600000")
print(stock_restricted_release_queue_sina_df)
```

数据示例

```
    代码    名称        解禁日期       解禁数量   解禁股流通市值  上市批次        公告日期
0  600000  浦发银行  2020-09-04  124831.65  127.0786    10  2017-09-06
1  600000  浦发银行  2017-03-20  109946.14  179.1023     9  2016-03-22
2  600000  浦发银行  2015-10-14  373069.43  599.1495     8  2010-10-16
3  600000  浦发银行  2010-09-29  117540.69  151.9801     7  2009-09-30
4  600000  浦发银行  2009-05-12   64917.32  161.1248     6  2006-05-09
5  600000  浦发银行  2008-05-12   41247.84  120.7737     5  2008-05-07
6  600000  浦发银行  2007-11-30   27761.94  144.0567     4  2006-11-21
7  600000  浦发银行  2007-05-14  192834.49  564.2337     3  2007-05-09
```
