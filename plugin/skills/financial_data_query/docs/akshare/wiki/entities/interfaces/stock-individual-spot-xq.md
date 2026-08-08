---
title: "stock_individual_spot_xq - 实时行情数据-雪球"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_individual_spot_xq

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: AKShare 股票数据 > A股 > 实时行情数据 > 实时行情数据-雪球
- 描述: 雪球-行情中心-个股
- 目标地址: https://xueqiu.com/S/SH513520
- 限量: 单次获取指定 symbol 的最新行情数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 实时行情数据-雪球

接口: stock_individual_spot_xq

目标地址: https://xueqiu.com/S/SH513520

描述: 雪球-行情中心-个股

限量: 单次获取指定 symbol 的最新行情数据

输入参数

| 名称      | 类型    | 描述                                                             |
|---------|-------|----------------------------------------------------------------|
| symbol  | str   | symbol="SH600000"; 证券代码，可以是 A 股个股代码，A 股场内基金代码，A 股指数，美股代码, 美股指数 |
| token   | float | token=None; 默认不设置token                                         |
| timeout | float | timeout=None; 默认不设置超时参数                                        |

输出参数

| 名称    | 类型     | 描述 |
|-------|--------|----|
| item  | object | -  |
| value | object | -  |

接口示例

```python
import akshare as ak

stock_individual_spot_xq_df = ak.stock_individual_spot_xq(symbol="SH600000")
print(stock_individual_spot_xq_df)
```

数据示例

```
        item                value
0         代码             SH600000
1      52周最高                11.02
2        流通股          29352178996
3         跌停                 8.69
4         最高                10.29
5        流通值       299392225759.0
6     最小交易单位                  100
7         涨跌                 0.55
8       每股收益                 1.54
9         昨收                 9.65
10       成交量            149422915
11       周转率                 0.51
12     52周最低               6.8673
13        名称                 浦发银行
14       交易所                   SH
15    市盈率(动)                6.615
16  基金份额/总股本          29352178996
17   净资产中的商誉             0.726713
18        均价               10.048
19        涨幅                  5.7
20        振幅                  5.6
21        现价                 10.2
22    今年以来涨幅                -0.87
23      发行日期  1999-11-10 00:00:00
24        最低                 9.75
25  资产净值/总市值       299392225759.0
26   股息(TTM)                0.321
27  股息率(TTM)                3.147
28        货币                  CNY
29     每股净资产                22.36
30    市盈率(静)                6.615
31       成交额         1501459278.0
32       市净率                0.456
33        涨停                10.62
34  市盈率(TTM)                6.615
35        时间  2025-04-08 15:00:00
36        今开                 9.77
```
