---
title: "stock_hot_search_baidu - 热搜股票"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_hot_search_baidu

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 股票热度 > 热搜股票
- 描述: 百度股市通-热搜股票
- 目标地址: https://gushitong.baidu.com/expressnews
- 限量: 单次返回指定 symbol, date 和 time 的热搜股票数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 热搜股票

接口: stock_hot_search_baidu

目标地址: https://gushitong.baidu.com/expressnews

描述: 百度股市通-热搜股票

限量: 单次返回指定 symbol, date 和 time 的热搜股票数据

输入参数

| 名称     | 类型  | 描述                                              |
|--------|-----|-------------------------------------------------|
| symbol | str | symbol="A股"; choice of {"全部", "A股", "港股", "美股"} |
| date   | str | date="20250616"                                 |
| time   | str | time="今日"; choice of {"今日", "1小时"}              |

输出参数

| 名称    | 类型     | 描述 |
|-------|--------|----|
| 名称/代码 | object | -  |
| 涨跌幅   | object | -  |
| 综合热度  | int64  | -  |

接口示例

```python
import akshare as ak

stock_hot_search_baidu_df = ak.stock_hot_search_baidu(symbol="A股", date="20250616", time="今日")
print(stock_hot_search_baidu_df)
```

数据示例

```
    名称/代码      涨跌幅    综合热度
0    融发核电   +1.72%  866000
1    永安药业   +7.13%  865000
2   中毅达    +10.00%  857000
3    恒宝股份   +9.98%  828000
4    利民股份   +9.98%  788000
5    中超控股   -1.34%  786000
6    百利电气   -4.24%  734000
7     比亚迪   -0.45%  716000
8    贵州茅台   -0.33%  569000
9    元隆雅图   +9.99%  561000
10   宁波韵升   +4.04%  555000
11   长安汽车   -1.47%  553000
```
