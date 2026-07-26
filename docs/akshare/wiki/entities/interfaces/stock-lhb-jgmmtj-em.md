---
title: "stock_lhb_jgmmtj_em - 机构买卖每日统计"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_lhb_jgmmtj_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 龙虎榜 > 龙虎榜-东财 > 机构买卖每日统计
- 描述: 东方财富网-数据中心-龙虎榜单-机构买卖每日统计
- 目标地址: https://data.eastmoney.com/stock/jgmmtj.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 机构买卖每日统计

接口: stock_lhb_jgmmtj_em

目标地址: https://data.eastmoney.com/stock/jgmmtj.html

描述: 东方财富网-数据中心-龙虎榜单-机构买卖每日统计

限量: 单次返回所有历史数据

输入参数

| 名称         | 类型  | 描述                    |
|------------|-----|-----------------------|
| start_date | str | start_date="20240417" |
| end_date   | str | end_date="20240430"   |

输出参数

| 名称          | 类型      | 描述       |
|-------------|---------|----------|
| 序号          | int64   | -        |
| 代码          | object  | -        |
| 名称          | object  | -        |
| 收盘价         | float64 | -        |
| 涨跌幅         | float64 | -        |
| 买方机构数       | float64 | -        |
| 卖方机构数       | float64 | -        |
| 机构买入总额      | float64 | 注意单位: 元  |
| 机构卖出总额      | float64 | 注意单位: 元  |
| 机构买入净额      | float64 | 注意单位: 元  |
| 市场总成交额      | float64 | 注意单位: 元  |
| 机构净买额占总成交额比 | float64 | -        |
| 换手率         | float64 | -        |
| 流通市值        | float64 | 注意单位: 亿元 |
| 上榜原因        | object  | -        |
| 上榜日期        | object  | -        |

接口示例

```python
import akshare as ak

stock_lhb_jgmmtj_em_df = ak.stock_lhb_jgmmtj_em(start_date="20240417", end_date="20240430")
print(stock_lhb_jgmmtj_em_df)
```

数据示例

```
      序号  代码  ...                                    上榜原因                   上榜日期
0      1  600919  ...           有价格涨跌幅限制的日收盘价格跌幅偏离值达到7%的前五只证券  2024-04-26
1      2  603486  ...  非ST、*ST和S证券连续三个交易日内收盘价格涨幅偏离值累计达到20%的证券  2024-04-22
2      3  688019  ...             有价格涨跌幅限制的日收盘价格涨幅达到15%的前五只证券  2024-04-29
3      4  002920  ...                        日跌幅偏离值达到7%的前5只证券  2024-04-19
4      5  000628  ...                         日换手率达到20%的前5只证券  2024-04-29
..   ...     ...  ...                                     ...         ...
334  335  000628  ...                连续三个交易日内，涨幅偏离值累计达到20%的证券  2024-04-26
335  336  000099  ...                        日涨幅偏离值达到7%的前5只证券  2024-04-18
336  337  688027  ...             有价格涨跌幅限制的日收盘价格涨幅达到15%的前五只证券  2024-04-26
337  338  002085  ...                        日涨幅偏离值达到7%的前5只证券  2024-04-24
338  339  603882  ...           有价格涨跌幅限制的日收盘价格跌幅偏离值达到7%的前五只证券  2024-04-26
[339 rows x 16 columns]
```
