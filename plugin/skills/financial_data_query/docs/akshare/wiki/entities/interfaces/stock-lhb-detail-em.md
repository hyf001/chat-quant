---
title: "stock_lhb_detail_em - 龙虎榜详情"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_lhb_detail_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 龙虎榜 > 龙虎榜-东财 > 龙虎榜详情
- 描述: 东方财富网-数据中心-龙虎榜单-龙虎榜详情
- 目标地址: https://data.eastmoney.com/stock/tradedetail.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 龙虎榜详情

接口: stock_lhb_detail_em

目标地址: https://data.eastmoney.com/stock/tradedetail.html

描述: 东方财富网-数据中心-龙虎榜单-龙虎榜详情

限量: 单次返回所有历史数据

输入参数

| 名称         | 类型  | 描述                    |
|------------|-----|-----------------------|
| start_date | str | start_date="20220314" |
| end_date   | str | end_date="20220315"   |

输出参数

| 名称       | 类型      | 描述      |
|----------|---------|---------|
| 序号       | int64   | -       |
| 代码       | object  | -       |
| 名称       | object  | -       |
| 上榜日      | object  | -       |
| 解读       | object  | -       |
| 收盘价      | float64 | -       |
| 涨跌幅      | float64 | 注意单位: % |
| 龙虎榜净买额   | float64 | 注意单位: 元 |
| 龙虎榜买入额   | float64 | 注意单位: 元 |
| 龙虎榜卖出额   | float64 | 注意单位: 元 |
| 龙虎榜成交额   | float64 | 注意单位: 元 |
| 市场总成交额   | int64   | 注意单位: 元 |
| 净买额占总成交比 | float64 | 注意单位: % |
| 成交额占总成交比 | float64 | 注意单位: % |
| 换手率      | float64 | 注意单位: % |
| 流通市值     | float64 | 注意单位: 元 |
| 上榜原因     | object  | -       |
| 上榜后1日    | float64 | 注意单位: % |
| 上榜后2日    | float64 | 注意单位: % |
| 上榜后5日    | float64 | 注意单位: % |
| 上榜后10日   | float64 | 注意单位: % |

接口示例

```python
import akshare as ak

stock_lhb_detail_em_df = ak.stock_lhb_detail_em(start_date="20230403", end_date="20230417")
print(stock_lhb_detail_em_df)
```

数据示例

```
      序号  代码    名称    上榜日  ...     上榜后1日      上榜后2日      上榜后5日    上榜后10日
0      1  000021   深科技  2023-04-06  ... -1.304348  -0.193237  -8.212560       NaN
1      2  000021   深科技  2023-04-03  ...  2.338227  12.561175  11.201740  7.667210
2      3  000021   深科技  2023-04-03  ...  2.338227  12.561175  11.201740  7.667210
3      4  000032  深桑达A  2023-04-06  ...  2.087576  -2.214868  -2.265784       NaN
4      5  000063  中兴通讯  2023-04-07  ... -3.783784  -5.270270  -7.027027       NaN
..   ...     ...   ...         ...  ...       ...        ...        ...       ...
630  631  688698  伟创电气  2023-04-12  ... -4.407407  -2.592593        NaN       NaN
631  632  688787  海天瑞声  2023-04-10  ...  2.028249   5.644068   6.073446       NaN
632  633  873593  鼎智科技  2023-04-17  ... -7.805655        NaN        NaN       NaN
633  634  900915  中路B股  2023-04-12  ...  2.981030   1.490515        NaN       NaN
634  635  900915  中路B股  2023-04-03  ...  5.807365   3.824363  12.039660  3.399433
```
