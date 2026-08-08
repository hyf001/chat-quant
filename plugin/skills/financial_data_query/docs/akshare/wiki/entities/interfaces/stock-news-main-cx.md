---
title: "stock_news_main_cx - 财经内容精选"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_news_main_cx

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 财经内容精选
- 描述: 财新网-财新数据通-最新
- 目标地址: https://cxdata.caixin.com/pc/
- 限量: 返回最新 100 条新闻数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

### 财经内容精选

接口: stock_news_main_cx

目标地址: https://cxdata.caixin.com/pc/

描述: 财新网-财新数据通-最新

限量: 返回最新 100 条新闻数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称            | 类型     | 描述 |
|---------------|--------|----|
| tag           | object | -  |
| summary       | object | -  |
| url           | object | -  |

接口示例

```python
import akshare as ak

stock_news_main_cx_df = ak.stock_news_main_cx()
print(stock_news_main_cx_df)
```

数据示例

```
      tag  ...                                                url
0    今日热点  ...  https://database.caixin.com/2025-12-25/1023970...
5    市场动态  ...  https://database.caixin.com/2025-12-25/1023969...
6    市场动态  ...  https://database.caixin.com/2025-12-25/1023969...
9    市场动态  ...  https://database.caixin.com/2025-12-25/1023969...
10   市场动态  ...  https://database.caixin.com/2025-12-25/1023969...
..    ...  ...                                                ...
105  市场动态  ...  https://database.caixin.com/2025-12-15/1023934...
106  市场动态  ...  https://database.caixin.com/2025-12-15/1023934...
107  市场动态  ...  https://database.caixin.com/2025-12-15/1023934...
108  市场洞察  ...  https://database.caixin.com/2025-12-15/1023933...
109  市场洞察  ...  https://database.caixin.com/2025-12-15/1023933...
[100 rows x 3 columns]
```
