---
title: "stock_hk_spot - 实时行情数据-新浪"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_hk_spot

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 港股 > 实时行情数据-新浪
- 描述: 获取所有港股的实时行情数据 15 分钟延时
- 目标地址: https://vip.stock.finance.sina.com.cn/mkt/#qbgg_hk
- 限量: 单次返回当前时间戳的所有港股的数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 实时行情数据-新浪

接口: stock_hk_spot

目标地址: https://vip.stock.finance.sina.com.cn/mkt/#qbgg_hk

描述: 获取所有港股的实时行情数据 15 分钟延时

限量: 单次返回当前时间戳的所有港股的数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称   | 类型      | 描述 |
|------|---------|----|
| 日期时间 | object  | -  |
| 代码   | object  | -  |
| 中文名称 | object  | -  |
| 英文名称 | object  | -  |
| 交易类型 | object  | -  |
| 最新价  | float64 | -  |
| 涨跌额  | float64 | -  |
| 涨跌幅  | float64 | -  |
| 昨收   | float64 | -  |
| 今开   | float64 | -  |
| 最高   | float64 | -  |
| 最低   | float64 | -  |
| 成交量  | float64 | -  |
| 成交额  | float64 | -  |
| 买一   | float64 | -  |
| 卖一   | float64 | -  |

接口示例

```python
import akshare as ak

stock_hk_spot_df = ak.stock_hk_spot()
print(stock_hk_spot_df)
```

数据示例

```
       日期时间     代码      中文名称  ...         成交额      买一      卖一
0     2025/07/07 16:08:06  00001        长和  ...   198584360   48.00   48.05
1     2025/07/07 16:08:08  00002      中电控股  ...   162263333   66.00   66.05
2     2025/07/07 16:08:08  00003    香港中华煤气  ...   117155173    6.71    6.72
3     2025/07/07 16:08:06  00004     九龙仓集团  ...     9018213   24.55   24.60
4     2025/07/07 16:08:08  00005      汇丰控股  ...  1045740332   95.20   95.25
...                   ...    ...       ...  ...         ...     ...     ...
2557  2025/07/07 16:08:10  83690     美团－ＷＲ  ...     5132670  107.00  109.00
2558  2025/07/07 16:08:10  86618    京东健康－Ｒ  ...           0   38.15   38.45
2559  2025/07/07 16:08:10  89618  京东集团－ＳＷＲ  ...      811085  112.90  126.00
2560  2025/07/07 16:08:10  89888  百度集团－ＳＷＲ  ...      712615   78.00   78.75
2561  2025/07/07 16:08:10  89988   阿里巴巴－ＷＲ  ...     5516825   96.10   96.50
[2562 rows x 16 columns]
```
