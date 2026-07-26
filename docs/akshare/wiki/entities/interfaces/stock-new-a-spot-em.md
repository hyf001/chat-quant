---
title: "stock_new_a_spot_em - 新股"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_new_a_spot_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: AKShare 股票数据 > A股 > 实时行情数据 > 实时行情数据-东财 > 新股
- 描述: 东方财富网-新股-实时行情数据
- 目标地址: http://quote.eastmoney.com/center/gridlist.html#newshares
- 限量: 单次返回所有新股上市公司的实时行情数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 新股

接口: stock_new_a_spot_em

目标地址: http://quote.eastmoney.com/center/gridlist.html#newshares

描述: 东方财富网-新股-实时行情数据

限量: 单次返回所有新股上市公司的实时行情数据

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
| 上市时间    | object  | -       |
| 总市值     | float64 | 注意单位: 元 |
| 流通市值    | float64 | 注意单位: 元 |
| 涨速      | float64 | -       |
| 5分钟涨跌   | float64 | 注意单位: % |
| 60日涨跌幅  | float64 | 注意单位: % |
| 年初至今涨跌幅 | float64 | 注意单位: % |

接口示例

```python
import akshare as ak

stock_new_a_spot_em_df = ak.stock_new_a_spot_em()
print(stock_new_a_spot_em_df)
```

数据示例

```
    序号   代码    名称   最新价    涨跌幅  ... 流通市值   涨速  5分钟涨跌  60日涨跌幅  年初至今涨跌幅
0    1  688583   C思看   91.96   2.17  ...  1175280710  0.09   0.17  174.84   174.84
1    2  301601   C惠通   39.69   1.69  ...  1189592887  0.05  -0.08  236.36   236.36
2    3  688758  赛分科技   15.87   1.54  ...   626933019  0.06   0.00  267.36   267.36
3    4  301458  钧崴电子   40.15  19.99  ...  2452564476  0.00   0.00  286.06   286.06
4    5  603072  天和磁材   38.01  -0.99  ...  2460981244  0.00   0.16  209.02   209.02
..  ..     ...   ...     ...    ...  ...         ...   ...    ...     ...      ...
68  69  301591  肯特股份   36.84   6.17  ...   774745200 -0.08  -0.19   -4.56    -3.79
69  70  688584  上海合晶   18.62  -0.96  ...  1048019122 -0.11  -0.21    5.32    -4.81
70  71  301589  诺瓦星云  163.23   1.45  ...  3018057408 -0.06   0.19  -13.63    -5.97
71  72  688709  成都华微   29.38   1.31  ...  2265703747  0.20  -0.03   33.24    -4.86
72  73  301502  华阳智能   41.98  -0.52  ...   599096580  0.43   0.55   -7.49    -2.60
[73 rows x 24 columns]
```
