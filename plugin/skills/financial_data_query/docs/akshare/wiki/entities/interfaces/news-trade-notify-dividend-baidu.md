---
title: "news_trade_notify_dividend_baidu - 分红派息"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# news_trade_notify_dividend_baidu

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 分红派息
- 描述: 百度股市通-交易提醒-分红派息
- 目标地址: https://gushitong.baidu.com/calendar
- 限量: 单次获取指定 date 的分红派息数据, 提供港股的分红派息数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

### 分红派息

接口: news_trade_notify_dividend_baidu

目标地址: https://gushitong.baidu.com/calendar

描述: 百度股市通-交易提醒-分红派息

限量: 单次获取指定 date 的分红派息数据, 提供港股的分红派息数据

输入参数

| 名称     | 类型  | 描述              |
|--------|-----|-----------------|
| date   | str | date="20241107" |
| cookie | str | 可以指定 cookie     |

输出参数

| 名称   | 类型     | 描述  |
|------|--------|-----|
| 股票代码 | object |     |
| 除权日  | object |     |
| 分红   | object |     |
| 送股   | object |     |
| 转增   | object |     |
| 实物   | object |     |
| 交易所  | object |     |
| 股票简称 | object |     |
| 报告期  | object |     |

接口示例

```python
import akshare as ak

news_trade_notify_dividend_baidu_df = ak.news_trade_notify_dividend_baidu(date="20251126")
print(news_trade_notify_dividend_baidu_df)
```

数据示例

```
      股票代码   除权日     分红 送股 转增 实物 交易所    股票简称 报告期
0   601788  2025-11-26   1.10元  -  -  -  SH    光大证券  2025-11-26
1   600482  2025-11-26   0.82元  -  -  -  SH    中国动力  2025-11-26
2   603298  2025-11-26   2.00元  -  -  -  SH    杭叉集团  2025-11-26
3   000088  2025-11-26   0.88元  -  -  -  SZ     盐田港  2025-11-26
4    06808  2025-11-26  0.08港元  -  -  -  HK    高鑫零售  2025-11-26
5   603040  2025-11-26   2.50元  -  -  -  SH     新坐标  2025-11-26
6   603008  2025-11-26   2.80元  -  -  -  SH     喜临门  2025-11-26
7   603676  2025-11-26   1.47元  -  -  -  SH     卫信康  2025-11-26
8   920112  2025-11-26   5.00元  -  -  -  BJ     巴兰仕  2025-11-26
9   301023  2025-11-26   4.00元  -  -  -  SZ    江南奕帆  2025-11-26
10  001228  2025-11-26   3.00元  -  -  -  SZ     永泰运  2025-11-26
11   00331  2025-11-26  0.18港元  -  -  -  HK  丰盛生活服务  2025-11-26
12  300246  2025-11-26   0.50元  -  -  -  SZ     宝莱特  2025-11-26
13  688193  2025-11-26   1.50元  -  -  -  SH    仁度生物  2025-11-26
14   06668  2025-11-26  0.05港元  -  -  -  HK    星盛商业  2025-11-26
```
