---
title: "stock_news_em - 个股新闻"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_news_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 个股新闻
- 描述: 东方财富指定个股的新闻资讯数据
- 目标地址: https://so.eastmoney.com/news/s?keyword=603777
- 限量: 指定 symbol 当日最近 100 条新闻资讯数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

### 个股新闻

接口: stock_news_em

目标地址: https://so.eastmoney.com/news/s?keyword=603777

描述: 东方财富指定个股的新闻资讯数据

限量: 指定 symbol 当日最近 100 条新闻资讯数据

输入参数

| 名称     | 类型  | 描述                          |
|--------|-----|-----------------------------|
| symbol | str | symbol="603777"; 股票代码或其他关键词 |

输出参数

| 名称   | 类型     | 描述  |
|------|--------|-----|
| 关键词  | object | -   |
| 新闻标题 | object | -   |
| 新闻内容 | object | -   |
| 发布时间 | object | -   |
| 文章来源 | object | -   |
| 新闻链接 | object | -   |

接口示例

```python
import akshare as ak

stock_news_em_df = ak.stock_news_em(symbol="603777")
print(stock_news_em_df)
```

数据示例

```
       关键词  ...                                               新闻链接
0   603777  ...  http://finance.eastmoney.com/a/202506163431529...
1   603777  ...  http://finance.eastmoney.com/a/202506113427724...
2   603777  ...  http://finance.eastmoney.com/a/202506093425572...
3   603777  ...  http://finance.eastmoney.com/a/202506093425584...
4   603777  ...  http://finance.eastmoney.com/a/202506123429086...
..     ...  ...                                                ...
95  603777  ...  http://finance.eastmoney.com/a/202505123401879...
96  603777  ...  http://finance.eastmoney.com/a/202503203351336...
97  603777  ...  http://finance.eastmoney.com/a/202505133403529...
98  603777  ...  http://finance.eastmoney.com/a/202504293392475...
99  603777  ...  http://finance.eastmoney.com/a/202505123402073...
[100 rows x 6 columns]
```
