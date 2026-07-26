---
title: "stock_ipo_benefit_ths - IPO 受益股"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_ipo_benefit_ths

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > IPO 受益股
- 描述: 同花顺-数据中心-新股数据-IPO受益股
- 目标地址: https://data.10jqka.com.cn/ipo/syg/
- 限量: 单次返回当前交易日的所有数据; 该数据每周更新一次, 返回最近一周的数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

### IPO 受益股

接口: stock_ipo_benefit_ths

目标地址: https://data.10jqka.com.cn/ipo/syg/

描述: 同花顺-数据中心-新股数据-IPO受益股

限量: 单次返回当前交易日的所有数据; 该数据每周更新一次, 返回最近一周的数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称     | 类型      | 描述      |
|--------|---------|---------|
| 序号     | int64   | -       |
| 股票代码   | object  | -       |
| 股票简称   | object  | -       |
| 收盘价    | float64 | 注意单位: 元 |
| 涨跌幅    | float64 | 注意单位: % |
| 市值     | object  | 注意单位: 元 |
| 参股家数   | int64   | -       |
| 投资总额   | object  | 注意单位: 元 |
| 投资占市值比 | float64 | 注意单位: % |
| 参股对象   | object  | -       |

接口示例

```python
import akshare as ak

stock_ipo_benefit_ths_df = ak.stock_ipo_benefit_ths()
print(stock_ipo_benefit_ths_df)
```

数据示例

```
    序号  股票代码  股票简称 收盘价  涨跌幅  市值  参股家数    投资总额  投资占市值比 参股对象
0      1  601601  中国太保  29.12 -0.206  1993.28亿     2  34.17亿    1.71   明细
1      2  600716  凤凰股份   3.82 -1.036    35.76亿     1   4.76亿   13.33   明细
2      3  600649  城投控股   4.08 -0.730   103.21亿     1   4.67亿    4.52   明细
3      4  601963  重庆银行   8.59 -1.151   162.82亿     1   3.79亿    2.33   明细
4      5  600639  浦东金桥  11.10 -0.893    94.38亿     2   3.18亿    3.37   明细
..   ...     ...   ...    ...    ...       ...   ...     ...     ...  ...
107  108  000685  中山公用   8.59 -0.116   126.71亿     1      0万    0.00   明细
108  109  600052  浙江广厦   3.98 -2.690    33.60亿     1      0万    0.00   明细
109  110  600261  阳光照明   3.62 -0.550    52.57亿     1      0万    0.00   明细
110  111  600496  精工钢构   3.90 -2.500    78.50亿     1      0万    0.00   明细
111  112  603987   康德莱  20.00  0.200    88.31亿     1      0万    0.00   明细
```
