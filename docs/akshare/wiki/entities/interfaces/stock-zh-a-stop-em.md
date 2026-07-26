---
title: "stock_zh_a_stop_em - 两网及退市"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_zh_a_stop_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 两网及退市
- 描述: 东方财富网-行情中心-沪深个股-两网及退市
- 目标地址: http://quote.eastmoney.com/center/gridlist.html#staq_net_board
- 限量: 单次返回当前交易日两网及退市的所有股票的行情数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

### 两网及退市

接口: stock_zh_a_stop_em

目标地址: http://quote.eastmoney.com/center/gridlist.html#staq_net_board

描述: 东方财富网-行情中心-沪深个股-两网及退市

限量: 单次返回当前交易日两网及退市的所有股票的行情数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称     | 类型      | 描述      |
|--------|---------|---------|
| 序号     | int64   | -       |
| 代码     | object  | -       |
| 名称     | object  | -       |
| 最新价    | float64 | -       |
| 涨跌幅    | float64 | 注意单位: % |
| 涨跌额    | float64 | -       |
| 成交量    | float64 | -       |
| 成交额    | float64 | -       |
| 振幅     | float64 | 注意单位: % |
| 最高     | float64 | -       |
| 最低     | float64 | -       |
| 今开     | float64 | -       |
| 昨收     | float64 | -       |
| 量比     | float64 | -       |
| 换手率    | float64 | 注意单位: % |
| 市盈率-动态 | float64 | -       |
| 市净率    | float64 | -       |

接口示例

```python
import akshare as ak

stock_zh_a_stop_em_df = ak.stock_zh_a_stop_em()
print(stock_zh_a_stop_em_df)
```

数据示例

```
      序号 代码    名称      最新价 涨跌幅 涨跌额  ... 今开 昨收 量比 换手率 市盈率-动态市净率
0      1  400010  鹫  峰 5  1.90  4.97  0.09  ... NaN  1.81 NaN  NaN  -87.16  20.41
1      2  400069     吉恩5  9.96  4.95  0.47  ... NaN  9.49 NaN  NaN   19.61   3.78
2      3  400073    上普A5  7.08  4.89  0.33  ... NaN  6.75 NaN  NaN   97.79  11.69
3      4  400008   水仙Ａ 5  4.96  4.86  0.23  ... NaN  4.73 NaN  NaN -539.13  992.0
4      5  400059     天珑5  3.50  4.79  0.16  ... NaN  3.34 NaN  NaN   50.29   3.72
..   ...     ...     ...   ...   ...   ...  ...  ..   ...  ..  ...     ...    ...
100  101  400027  生  态 5  1.05 -4.55 -0.05  ... NaN   1.1 NaN  NaN  -57.07    4.7
101  102  400036     天创5  1.64 -4.65 -0.08  ... NaN  1.72 NaN  NaN   103.8   1.57
102  103  400005   海国实 5  1.01 -4.72 -0.05  ... NaN  1.06 NaN  NaN  -91.82   15.3
103  104  400039  华  圣 5  0.95 -5.00 -0.05  ... NaN   1.0 NaN  NaN  -65.97   4.64
104  105  400028  金  马 5  0.95 -5.00 -0.05  ... NaN   1.0 NaN  NaN -226.19    9.3
```
