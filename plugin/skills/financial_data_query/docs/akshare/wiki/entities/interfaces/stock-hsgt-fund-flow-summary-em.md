---
title: "stock_hsgt_fund_flow_summary_em - 沪深港通资金流向"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_hsgt_fund_flow_summary_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 沪深港通资金流向
- 描述: 东方财富网-数据中心-资金流向-沪深港通资金流向
- 目标地址: https://data.eastmoney.com/hsgt/index.html#lssj
- 限量: 单次获取沪深港通资金流向数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

### 沪深港通资金流向

接口: stock_hsgt_fund_flow_summary_em

目标地址: https://data.eastmoney.com/hsgt/index.html#lssj

描述: 东方财富网-数据中心-资金流向-沪深港通资金流向

限量: 单次获取沪深港通资金流向数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称     | 类型      | 描述       |
|--------|---------|----------|
| 交易日    | object  | -        |
| 类型     | object  | -        |
| 板块     | object  | -        |
| 资金方向   | object  | -        |
| 交易状态   | int64   | 3 为收盘    |
| 成交净买额  | float64 | 注意单位: 亿元 |
| 资金净流入  | float64 | 注意单位: 亿元 |
| 当日资金余额 | float64 | 注意单位: 亿元 |
| 上涨数    | int64   | -        |
| 持平数    | int64   | -        |
| 下跌数    | int64   | -        |
| 相关指数   | object  | -        |
| 指数涨跌幅  | float64 | 注意单位: %  |

接口示例

```python
import akshare as ak

stock_hsgt_fund_flow_summary_em_df = ak.stock_hsgt_fund_flow_summary_em()
print(stock_hsgt_fund_flow_summary_em_df)
```

数据示例

```
      交易日    类型      板块 资金方向  交易状态  ... 上涨数  持平数  下跌数  相关指数  指数涨跌幅
0  2022-11-25  沪港通     沪股通   北向     3  ...  302    8  284  上证指数   0.40
1  2022-11-25  沪港通  港股通(沪)   南向     3  ...  179   16  186  恒生指数  -0.49
2  2022-11-25  深港通     深股通   北向     3  ...  283   29  621  深证成指  -0.48
3  2022-11-25  深港通  港股通(深)   南向     3  ...  247   33  268  恒生指数  -0.49
[4 rows x 13 columns]
```
