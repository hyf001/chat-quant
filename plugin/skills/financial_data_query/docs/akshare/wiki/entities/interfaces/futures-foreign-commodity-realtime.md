---
title: "futures_foreign_commodity_realtime - 外盘-实时行情数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, futures, parameters, returns, example]
sources: [raw/data-dictionary/futures/futures.md]
confidence: high
---
# futures_foreign_commodity_realtime

- 分类: [[futures-futures|AKShare 期货数据]]
- 主题路径: 此处的合约需要是近期的合约, 否则会报错 > 外盘-实时行情数据
- 描述: 新浪财经-外盘商品期货数据
- 目标地址: https://finance.sina.com.cn/money/future/hf.html
- 限量: 单次返回当前交易日的订阅的所有期货品种的数据
- 来源页面: https://akshare.akfamily.xyz/data/futures/futures.html

## 相关

- [[futures-futures|AKShare 期货数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 外盘-实时行情数据

接口: futures_foreign_commodity_realtime

目标地址: https://finance.sina.com.cn/money/future/hf.html

描述: 新浪财经-外盘商品期货数据

限量: 单次返回当前交易日的订阅的所有期货品种的数据

输入参数

| 名称     | 类型          | 描述                                                                     |
|--------|-------------|------------------------------------------------------------------------|
| symbol | list or str | 需要订阅的合约代码; 调用 **ak.futures_hq_subscribe_exchange_symbol()** 获取字段及代码对应表 |

输出参数

| 名称    | 类型      | 描述  |
|-------|---------|-----|
| 名称    | object  | -   |
| 最新价   | float64 | -   |
| 人民币报价 | float64 | -   |
| 涨跌额   | float64 | -   |
| 涨跌幅   | float64 | -   |
| 开盘价   | float64 | -   |
| 最高价   | float64 | -   |
| 最低价   | float64 | -   |
| 昨日结算价 | float64 | -   |
| 持仓量   | float64 | -   |
| 买价    | float64 | -   |
| 卖价    | float64 | -   |
| 行情时间  | object  | -   |
| 日期    | object  | -   |

接口示例-传入字符串

```python
import akshare as ak

futures_foreign_commodity_realtime_df = ak.futures_foreign_commodity_realtime(symbol='CT,NID')
print(futures_foreign_commodity_realtime_df)
```

数据示例-传入字符串

```
         名称      最新价          人民币报价  ...        卖价      行情时间          日期
0  NYBOT-棉花     81.1   12953.138327  ...     81.13  16:13:34  2024-05-24
1   LME镍3个月  20256.0  146748.643200  ...  20265.00  16:13:08  2024-05-24
[2 rows x 14 columns]
```

接口示例-传入列表

```python
import time
import akshare as ak

print("开始接收实时行情, 每 3 秒刷新一次")
subscribe_list = ak.futures_foreign_commodity_subscribe_exchange_symbol()  # 其中 subscribe_list 为列表
while True:
    time.sleep(3)
    futures_foreign_commodity_realtime_df = ak.futures_foreign_commodity_realtime(symbol=subscribe_list)
    print(futures_foreign_commodity_realtime_df)
```

数据示例-传入列表

```
          名称       最新价    人民币报价  ...         卖价      行情时间       日期
0     新加坡铁矿石    100.955  7.159729e+00  ...    101.000  05:05:00  2024-08-31
1        马棕油   3980.500  9.075850e+02  ...   3979.000  18:00:00  2024-08-30
2        日橡胶    374.790  2.658011e+04  ...    375.000  18:00:46  2024-08-30
3       美国原糖     19.424  1.377550e+00  ...     19.440  01:00:00  2024-08-31
4   CME比特币期货  61300.500  2.173716e+06  ...  61285.000  12:55:15  2024-08-23
5   NYBOT-棉花     69.975  1.094071e+04  ...     69.960  02:19:58  2024-08-31
6    LME镍3个月  16700.000  1.184364e+05  ...  16755.000  01:59:52  2024-08-31
7    LME铅3个月   2067.950  1.466590e+04  ...   2068.000  01:59:02  2024-08-31
8    LME锡3个月  32457.000  2.301850e+05  ...  32440.000  01:47:38  2024-08-31
9    LME锌3个月   2897.150  2.054659e+04  ...   2899.000  01:59:00  2024-08-31
10   LME铝3个月   2445.450  1.734313e+04  ...   2448.000  01:59:54  2024-08-31
11   LME铜3个月   9248.850  6.559284e+04  ...   9254.000  01:59:48  2024-08-31
12   CBOT-黄豆    999.875  2.605537e+03  ...    999.250  02:19:59  2024-08-31
13   CBOT-小麦    552.150  1.438827e+03  ...    552.250  02:19:56  2024-08-31
14   CBOT-玉米    401.525  1.121056e+03  ...    401.500  02:20:00  2024-08-31
15  CBOT-黄豆油     41.855  6.544098e+03  ...     41.900  02:20:00  2024-08-31
16  CBOT-黄豆粉    312.300  2.441852e+03  ...    312.600  02:20:00  2024-08-31
18    COMEX铜    421.755  6.594209e+04  ...    422.000  04:59:55  2024-08-31
19  NYMEX天然气      2.148  1.523362e+01  ...      2.146  04:59:58  2024-08-31
20   NYMEX原油     73.621  3.811477e+03  ...     73.660  04:59:59  2024-08-31
21   COMEX白银     29.229  2.072921e+02  ...     29.250  04:59:55  2024-08-31
22   COMEX黄金   2535.060  5.780135e+02  ...   2536.000  04:59:58  2024-08-31
23   CME-瘦肉猪     82.218  5.830901e+02  ...     82.250  02:04:59  2024-08-31
24     布伦特原油     77.015  3.987190e+03  ...     77.060  05:58:53  2024-08-31
25       伦敦金   2503.290  5.707696e+02  ...   2503.670  04:55:00  2024-08-31
26       伦敦银     28.830  6.573465e+00  ...     28.880  04:55:00  2024-08-31
27      伦敦铂金    930.960  2.122661e+02  ...    931.400  04:59:56  2024-08-31
28      伦敦钯金    961.400  2.192067e+02  ...    962.500  04:58:04  2024-08-31
29     欧洲碳排放     70.185  4.977520e+02  ...     70.260  00:00:00  2024-08-31
[29 rows x 14 columns]
```
