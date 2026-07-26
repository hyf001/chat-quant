---
title: "stock_sse_deal_daily - 上海证券交易所-每日概况"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_sse_deal_daily

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: AKShare 股票数据 > A股 > 股票市场总貌 > 上海证券交易所-每日概况
- 描述: 上海证券交易所-数据-股票数据-成交概况-股票成交概况-每日股票情况
- 目标地址: http://www.sse.com.cn/market/stockdata/overview/day/
- 限量: 单次返回指定日期的每日概况数据, 当前交易日数据需要在收盘后获取; 注意仅支持获取在 20211227（包含）之后的数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 上海证券交易所-每日概况

接口: stock_sse_deal_daily

目标地址: http://www.sse.com.cn/market/stockdata/overview/day/

描述: 上海证券交易所-数据-股票数据-成交概况-股票成交概况-每日股票情况

限量: 单次返回指定日期的每日概况数据, 当前交易日数据需要在收盘后获取; 注意仅支持获取在 20211227（包含）之后的数据

输入参数

| 名称   | 类型  | 描述                                                              |
|------|-----|-----------------------------------------------------------------|
| date | str | date="20250221"; 当前交易日的数据需要交易所收盘后统计; 注意仅支持获取在 20211227（包含）之后的数据 |

输出参数

| 名称   | 类型      | 描述        |
|------|---------|-----------|
| 单日情况 | object  | 包含了网页所有字段 |
| 股票   | float64 | -         |
| 主板A  | float64 | -         |
| 主板B  | float64 | -         |
| 科创板  | float64 | -         |
| 股票回购 | float64 | -         |

接口示例

```python
import akshare as ak

stock_sse_deal_daily_df = ak.stock_sse_deal_daily(date="20250221")
print(stock_sse_deal_daily_df)
```

数据示例

```
    单日情况           股票          主板A       主板B         科创板  股票回购
0    挂牌数    2321.0000    1693.0000   43.0000    585.0000   0.0
1   市价总值  529981.4800  456997.7000  942.6300  72041.1500   0.0
2   流通市值  501613.5100  445348.4700  713.7700  55551.2700   0.0
3   成交金额    8561.3100    6413.6300    4.3000   2143.3700   0.3
4    成交量     608.5800     556.5800    0.7200     51.2900   0.1
5  平均市盈率      14.3200      13.2000    7.1600     45.7800   NaN
6    换手率       1.6154       1.4034    0.4565      2.9752   0.0
7  流通换手率       1.7068       1.4401    0.6029      3.8584   0.0
```
