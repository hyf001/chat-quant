---
title: "stock_cy_a_spot_em - 创业板"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_cy_a_spot_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: AKShare 股票数据 > A股 > 实时行情数据 > 实时行情数据-东财 > 创业板
- 描述: 东方财富网-创业板-实时行情
- 目标地址: https://quote.eastmoney.com/center/gridlist.html#gem_board
- 限量: 单次返回所有创业板的实时行情数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 创业板

接口: stock_cy_a_spot_em

目标地址: https://quote.eastmoney.com/center/gridlist.html#gem_board

描述: 东方财富网-创业板-实时行情

限量: 单次返回所有创业板的实时行情数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称      | 类型      | 描述      |
|---------|---------|---------|
| 序号      | int64   | -       |
| 代码      | object  | -       |
| 名称      | object  | -       |
| 最新价     | float64 | -       |
| 涨跌幅     | float64 | 注意单位: % |
| 涨跌额     | float64 | -       |
| 成交量     | float64 | 注意单位: 手 |
| 成交额     | float64 | 注意单位: 元 |
| 振幅      | float64 | 注意单位: % |
| 最高      | float64 | -       |
| 最低      | float64 | -       |
| 今开      | float64 | -       |
| 昨收      | float64 | -       |
| 量比      | float64 | -       |
| 换手率     | float64 | 注意单位: % |
| 市盈率-动态  | float64 | -       |
| 市净率     | float64 | -       |
| 总市值     | float64 | 注意单位: 元 |
| 流通市值    | float64 | 注意单位: 元 |
| 涨速      | float64 | -       |
| 5分钟涨跌   | float64 | 注意单位: % |
| 60日涨跌幅  | float64 | 注意单位: % |
| 年初至今涨跌幅 | float64 | 注意单位: % |

接口示例

```python
import akshare as ak

stock_cy_a_spot_em_df = ak.stock_cy_a_spot_em()
print(stock_cy_a_spot_em_df)
```

数据示例

```
     序号      代码   名称    最新价  ...    涨速  5分钟涨跌 60日涨跌幅 年初至今涨跌幅
0        1  301602    N超研  32.10  ...  0.25   3.65  379.10   379.10
1        2  300996   普联软件  20.63  ...  0.00   0.00    2.84    13.85
2        3  300117  *ST嘉寓   1.08  ...  0.00   0.00  -31.21    -0.92
3        4  300843   胜蓝股份  37.90  ... -0.21   1.64   21.28     8.25
4        5  300476   胜宏科技  58.50  ...  0.10   0.00   28.09    38.99
...    ...     ...    ...    ...  ...   ...    ...     ...      ...
1396  1397  300043   星辉娱乐   3.66  ...  0.00   0.00   14.73     0.55
1397  1398  300827   上能电气  41.48  ... -0.05   0.12    2.37    -5.51
1398  1399  300377    赢时胜  27.62  ...  0.00  -1.81  100.87     0.22
1399  1400  300515   三德科技  16.00  ... -2.20  -3.50   30.93    34.34
1400  1401  300853   申昊科技  18.67  ...  0.05   0.32    4.59   -25.56
[1401 rows x 23 columns]
```
