---
title: "news_report_time_baidu - 财报发行"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# news_report_time_baidu

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 财报发行
- 描述: 百度股市通-财报发行
- 目标地址: https://gushitong.baidu.com/calendar
- 限量: 单次获取指定 date 的财报发行, 提供港股的财报发行数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

### 财报发行

接口: news_report_time_baidu

目标地址: https://gushitong.baidu.com/calendar

描述: 百度股市通-财报发行

限量: 单次获取指定 date 的财报发行, 提供港股的财报发行数据

输入参数

| 名称   | 类型  | 描述              |
|------|-----|-----------------|
| date | str | date="20241107" |

输出参数

| 名称   | 类型     | 描述  |
|------|--------|-----|
| 股票代码 | object |     |
| 交易所  | object |     |
| 股票简称 | object |     |
| 财报期  | object |     |

接口示例

```python
import akshare as ak

news_report_time_baidu_df = ak.news_report_time_baidu(date="20241107")
print(news_report_time_baidu_df)
```

数据示例

```
     股票代码 交易所                       股票简称               财报期
0   00945  HK                         宏利金融-S          2024年三季报
1   00981  HK                           中芯国际          2024年三季报
2   01347  HK                          华虹半导体          2024年三季报
3   01665  HK                           槟杰科达          2024年三季报
4   08476  HK                         大洋环球控股           2024年中报
..    ...  ..                            ...               ...
95   XRAY  US                         登士柏西诺德    美东时间发布2024年三季报
96   UPST  US         Upstart Holdings, Inc.  美东时间盘后发布2024年三季报
97    MUR  US                           墨菲石油    美东时间发布2024年三季报
98     SG  US       Sweetgreen, Inc. Class A    美东时间发布2024年三季报
99   STEP  US  StepStone Group, Inc. Class A   美东时间发布24/25年二季报
[100 rows x 4 columns]
```
