---
title: "get_futures_daily - 内盘-历史行情数据-交易所"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, futures, parameters, returns, example]
sources: [raw/data-dictionary/futures/futures.md]
confidence: high
---
# get_futures_daily

- 分类: [[futures-futures|AKShare 期货数据]]
- 主题路径: 此处的合约需要是近期的合约, 否则会报错 > 内盘-历史行情数据-交易所
- 描述: 提供各交易所各品种的网站的历史行情数据, 其中 20040625, 20070604, 20081226, 20090119 原网页数据缺失
- 目标地址: 各交易所网站
- 限量: 单次返回指定时间段指定交易所的所有期货品种历史数据
- 来源页面: https://akshare.akfamily.xyz/data/futures/futures.html

## 相关

- [[futures-futures|AKShare 期货数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 内盘-历史行情数据-交易所

接口: get_futures_daily

目标地址: 各交易所网站

描述: 提供各交易所各品种的网站的历史行情数据, 其中 20040625, 20070604, 20081226, 20090119 原网页数据缺失

限量: 单次返回指定时间段指定交易所的所有期货品种历史数据

输入参数

| 名称         | 类型  | 描述                                                                      |
|------------|-----|-------------------------------------------------------------------------|
| start_date | str | start_date="20200701"                                                   |
| end_date   | str | end_date="20200716"                                                     |
| market     | str | market="DCE"; choice of {"CFFEX", "INE", "CZCE", "DCE", "SHFE", "GFEX"} |

输出参数

| 名称            | 类型    | 描述   |
|---------------|-------|------|
| symbol        | str   | 合约   |
| date          | str   | 交易日  |
| open          | float | 开盘价  |
| high          | float | 最高价  |
| low           | float | 最低价  |
| close         | str   | 收盘价  |
| volume        | str   | 成交量  |
| open_interest | str   | 持仓量  |
| turnover      | float | 成交额  |
| settle        | float | 结算价  |
| pre_settle    | float | 前结算价 |
| variety       | str   | 品种   |

接口示例

```python
import akshare as ak

get_futures_daily_df = ak.get_futures_daily(start_date="20200701", end_date="20200716", market="DCE")
print(get_futures_daily_df)
```

数据示例

```
     symbol      date     open  ...   settle pre_settle variety
0     A2007  20200701     6160  ...     6122       5643       A
1     A2009  20200701     4871  ...     4874       4839       A
2     A2011  20200701     4480  ...     4424       4411       A
3     A2101  20200701     4402  ...     4385       4395       A
4     A2103  20200701     4422  ...     4394       4412       A
     ...       ...      ...  ...      ...        ...     ...
2749   PG99  20200716  3899.35  ...  3881.69    3879.72      PG
2750    P99  20200716   5257.2  ...  5269.32    5212.02       P
2751    L99  20200716  7213.86  ...  7156.44    7220.27       L
2752    M99  20200716  2858.98  ...  2862.43    2855.63       M
2753   JM99  20200716  1193.58  ...  1195.49    1197.92      JM
```
