---
title: "stock_ipo_summary_cninfo - 上市相关-巨潮资讯"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_ipo_summary_cninfo

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 年报季报 > 上市相关-巨潮资讯
- 描述: 巨潮资讯-个股-上市相关
- 目标地址: https://webapi.cninfo.com.cn/#/company
- 限量: 单次获取指定 symbol 的上市相关数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 上市相关-巨潮资讯

接口: stock_ipo_summary_cninfo

目标地址: https://webapi.cninfo.com.cn/#/company

描述: 巨潮资讯-个股-上市相关

限量: 单次获取指定 symbol 的上市相关数据

输入参数

| 名称         | 类型  | 描述                    |
|------------|-----|-----------------------|
| symbol     | str | symbol="600030"       |

输出参数

| 名称       | 类型      | 描述       |
|----------|---------|----------|
| 股票代码     | object  | -        |
| 招股公告日期   | object  | -        |
| 中签率公告日   | object  | -        |
| 每股面值     | float64 | 注意单位: 元  |
| 总发行数量    | float64 | 注意单位: 万股 |
| 发行前每股净资产 | float64 | 注意单位: 元  |
| 摊薄发行市盈率  | float64 | -        |
| 募集资金净额   | float64 | 注意单位: 万元 |
| 上网发行日期   | object  | -        |
| 上市日期     | object  | -        |
| 发行价格     | float64 | 注意单位: 元  |
| 发行费用总额   | float64 | 注意单位: 万元 |
| 发行后每股净资产 | float64 | 注意单位: 元  |
| 上网发行中签率  | float64 | 注意单位: %  |
| 主承销商     | float64 | -        |

接口示例

```python
import akshare as ak

stock_ipo_summary_cninfo_df = ak.stock_ipo_summary_cninfo(symbol="600030")
print(stock_ipo_summary_cninfo_df)
```

数据示例

```
   股票代码      招股公告日期 中签率公告日  每股面值  ...     发行费用总额  发行后每股净资产  上网发行中签率        主承销商
0  600030  2002-12-13    NaT   1.0  ...  4032.6625      2.11    0.282  广发证券股份有限公司
[1 rows x 15 columns]
```
