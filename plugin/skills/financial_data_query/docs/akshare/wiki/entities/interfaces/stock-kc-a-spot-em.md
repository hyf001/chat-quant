---
title: "stock_kc_a_spot_em - 科创板"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_kc_a_spot_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: AKShare 股票数据 > A股 > 实时行情数据 > 实时行情数据-东财 > 科创板
- 描述: 东方财富网-科创板-实时行情
- 目标地址: http://quote.eastmoney.com/center/gridlist.html#kcb_board
- 限量: 单次返回所有科创板的实时行情数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 科创板

接口: stock_kc_a_spot_em

目标地址: http://quote.eastmoney.com/center/gridlist.html#kcb_board

描述: 东方财富网-科创板-实时行情

限量: 单次返回所有科创板的实时行情数据

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

stock_kc_a_spot_em_df = ak.stock_kc_a_spot_em()
print(stock_kc_a_spot_em_df)
```

数据示例

```
    序号   代码     名称     最新价  ...  涨速 5分钟涨跌 60日涨跌幅 年初至今涨跌幅
0      1  688545    N兴福   27.39  ...  0.11   0.59  134.50   134.50
1      2  688205    德科立  108.13  ... -1.30   2.01  102.87    18.82
2      3  688577   浙海德曼   47.20  ... -0.13  -0.44   30.03    20.47
3      4  688246   嘉和美康   23.99  ...  0.00   0.00  -17.13    -3.27
4      5  688622   禾信仪器   69.00  ...  0.09   0.19  131.70    13.84
..   ...     ...    ...     ...  ...   ...    ...     ...      ...
582  583  688410    山外山   10.13  ... -0.10  -0.10  -11.37    -9.23
583  584  688311   盟升电子   27.78  ... -0.04  -0.22   -8.26   -16.10
584  585  688085   三友医疗   18.52  ... -1.17  -1.23  -14.62   -12.60
585  586  688165  埃夫特-U   33.70  ... -0.09  -0.82  243.53    27.65
586  587  688408    中信博   61.18  ...  0.30   0.30  -23.46   -15.03
[587 rows x 23 columns]
```
