---
title: "stock_individual_info_em - 个股信息查询-东财"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_individual_info_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: AKShare 股票数据 > A股 > 个股信息查询-东财
- 描述: 东方财富-个股-股票信息
- 目标地址: http://quote.eastmoney.com/concept/sh603777.html?from=classic
- 限量: 单次返回指定 symbol 的个股信息
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 个股信息查询-东财

接口: stock_individual_info_em

目标地址: http://quote.eastmoney.com/concept/sh603777.html?from=classic

描述: 东方财富-个股-股票信息

限量: 单次返回指定 symbol 的个股信息

说明: 接口已兼容东方财富返回体偶发新增的顶层元数据字段, 如 `dsc`

输入参数

| 名称      | 类型    | 描述                      |
|---------|-------|-------------------------|
| symbol  | str   | symbol="603777"; 股票代码   |
| timeout | float | timeout=None; 默认不设置超时参数 |

输出参数

| 名称    | 类型     | 描述  |
|-------|--------|-----|
| item  | object | -   |
| value | object | -   |

接口示例

```python
import akshare as ak

stock_individual_info_em_df = ak.stock_individual_info_em(symbol="000001")
print(stock_individual_info_em_df)
```

数据示例

```
   item               value
0    最新               7.05
1  股票代码             000002
2  股票简称            万  科Ａ
3   总股本       11930709471.0
4   流通股        9716935865.0
5   总市值  84111501770.550003
6  流通市值      68504397848.25
7    行业              房地产开发
8  上市时间            19910129
```
