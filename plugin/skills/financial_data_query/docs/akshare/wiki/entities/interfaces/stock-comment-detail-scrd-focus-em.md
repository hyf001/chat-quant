---
title: "stock_comment_detail_scrd_focus_em - 用户关注指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_comment_detail_scrd_focus_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 千股千评详情 > 市场热度 > 用户关注指数
- 描述: 东方财富网-数据中心-特色数据-千股千评-市场热度-用户关注指数
- 目标地址: https://data.eastmoney.com/stockcomment/stock/600000.html
- 限量: 单次获取所有数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 用户关注指数

接口: stock_comment_detail_scrd_focus_em

目标地址: https://data.eastmoney.com/stockcomment/stock/600000.html

描述: 东方财富网-数据中心-特色数据-千股千评-市场热度-用户关注指数

限量: 单次获取所有数据

输入参数

| 名称     | 类型  | 描述              |
|--------|-----|-----------------|
| symbol | str | symbol="600000" |

输出参数

| 名称     | 类型      | 描述 |
|--------|---------|----|
| 交易日    | object  | -  |
| 用户关注指数 | float64 | -  |

接口示例

```python
import akshare as ak

stock_comment_detail_scrd_focus_em_df = ak.stock_comment_detail_scrd_focus_em(symbol="600000")
print(stock_comment_detail_scrd_focus_em_df)
```

数据示例

```
       交易日  用户关注指数
0   2024-08-15    91.2
1   2024-08-16    91.6
2   2024-08-19    92.4
3   2024-08-20    92.4
4   2024-08-21    92.0
5   2024-08-22    92.0
6   2024-08-23    92.4
7   2024-08-26    92.4
8   2024-08-27    91.6
9   2024-08-28    92.0
10  2024-08-29    92.0
11  2024-08-30    91.2
12  2024-09-02    91.2
13  2024-09-03    91.2
14  2024-09-04    91.2
15  2024-09-05    91.2
16  2024-09-06    91.2
17  2024-09-09    92.4
18  2024-09-10    92.0
19  2024-09-11    91.6
20  2024-09-12    91.6
21  2024-09-13    93.2
22  2024-09-18    93.2
23  2024-09-19    92.8
24  2024-09-20    92.4
25  2024-09-23    92.8
26  2024-09-24    93.2
27  2024-09-25    93.2
28  2024-09-26    93.2
29  2024-09-27    92.4
```
