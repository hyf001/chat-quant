---
title: "stock_zh_ab_comparison_em - AB 股比价"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_zh_ab_comparison_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: AKShare 股票数据 > A股 > 实时行情数据 > 实时行情数据-东财 > AB 股比价
- 描述: 东方财富网-行情中心-沪深京个股-AB股比价-全部AB股比价
- 目标地址: https://quote.eastmoney.com/center/gridlist.html#ab_comparison
- 限量: 单次返回全部 AB 股比价的实时行情数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

###### AB 股比价

接口: stock_zh_ab_comparison_em

目标地址: https://quote.eastmoney.com/center/gridlist.html#ab_comparison

描述: 东方财富网-行情中心-沪深京个股-AB股比价-全部AB股比价

限量: 单次返回全部 AB 股比价的实时行情数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称   | 类型      | 描述 |
|------|---------|----|
| 序号   | int64   | -  |
| B股代码 | object  | -  |
| B股名称 | object  | -  |
| 最新价B | float64 | -  |
| 涨跌幅B | float64 | -  |
| A股代码 | object  | -  |
| A股名称 | object  | -  |
| 最新价A | float64 | -  |
| 涨跌幅A | float64 | -  |
| 比价   | float64 | -  |

接口示例

```python
import akshare as ak

stock_zh_ab_comparison_em_df = ak.stock_zh_ab_comparison_em()
print(stock_zh_ab_comparison_em_df)
```

数据示例

```
    序号 B股代码   B股名称   最新价B 涨跌幅B A股代码  A股名称 最新价A 涨跌幅A   比价
0    1  200026    飞亚达Ｂ  14.38  10.02  000026    飞亚达  6.70  0.60  2.35
1    2  200030     富奥B   6.05   2.54  000030   富奥股份  3.09  0.65  2.14
2    3  900917    海欣Ｂ股   6.70   2.13  600851   海欣股份  2.63  0.38  3.55
3    4  900916    凤凰B股  13.00   1.72  600679   上海凤凰  3.47  0.58  5.22
4    5  900920    动力Ｂ股   6.23   1.63  600841   动力新科  1.97  1.03  4.41
..  ..     ...     ...    ...    ...     ...    ...   ...   ...   ...
68  69  900942    黄山Ｂ股  11.67  -2.99  600054   黄山旅游  7.25 -0.55  2.24
69  70  900902    市北B股   5.12  -4.30  600604   市北高新  1.63  0.00  4.38
70  71  900946    天雁B股   8.27  -5.05  600698   湖南天雁  2.13 -1.84  5.41
71  72  900906    中毅达B  16.88  -5.06  600610    中毅达  2.77 -0.72  8.49
72  73  900952  *ST锦港B    NaN    NaN  600190  *ST锦港   NaN   NaN  2.82
[73 rows x 10 columns]
```
