---
title: "stock_sns_sseinfo - 上证e互动"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_sns_sseinfo

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 股票热度 > 互动平台 > 上证e互动
- 描述: 上证e互动-提问与回答
- 目标地址: https://sns.sseinfo.com/company.do?uid=65
- 限量: 单次返回指定 symbol 的提问与回答数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 上证e互动

接口: stock_sns_sseinfo

目标地址: https://sns.sseinfo.com/company.do?uid=65

描述: 上证e互动-提问与回答

限量: 单次返回指定 symbol 的提问与回答数据

输入参数

| 名称     | 类型  | 描述                    |
|--------|-----|-----------------------|
| symbol | str | symbol="603119"; 股票代码 |

输出参数

| 名称   | 类型     | 描述 |
|------|--------|----|
| 股票代码 | object | -  |
| 公司简称 | object | -  |
| 问题   | object | -  |
| 回答   | object | -  |
| 问题时间 | object | -  |
| 回答时间 | object | -  |
| 问题来源 | object | -  |
| 回答来源 | object | -  |
| 用户名  | object | -  |

接口示例

```python
import akshare as ak

stock_sns_sseinfo_df = ak.stock_sns_sseinfo(symbol="603119")
print(stock_sns_sseinfo_df)
```

数据示例

```
       股票代码  公司简称  ... 回答来源              用户名
0    603119  浙江荣泰  ...   网站             YiQi
1    603119  浙江荣泰  ...   网站             YiQi
2    603119  浙江荣泰  ...   网站            春暖花未开
3    603119  浙江荣泰  ...   网站  guest_zT0NfLL0L
4    603119  浙江荣泰  ...   网站              Kgk
..      ...   ...  ...  ...              ...
150  603119  浙江荣泰  ...   网站              龙投宝
151  603119  浙江荣泰  ...   网站       SummerIcey
152  603119  浙江荣泰  ...   网站  guest_Usy8rr8Ik
153  603119  浙江荣泰  ...   网站            赵子龙常山
154  603119  浙江荣泰  ...   网站            赵子龙常山
[155 rows x 9 columns]
```
