---
title: "stock_lhb_stock_detail_em - 个股龙虎榜详情"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_lhb_stock_detail_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 营业部详情数据-东财 > 个股龙虎榜详情
- 描述: 东方财富网-数据中心-龙虎榜单-个股龙虎榜详情
- 目标地址: https://data.eastmoney.com/stock/lhb/600077.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 个股龙虎榜详情

接口: stock_lhb_stock_detail_em

目标地址: https://data.eastmoney.com/stock/lhb/600077.html

描述: 东方财富网-数据中心-龙虎榜单-个股龙虎榜详情

限量: 单次返回所有历史数据

输入参数

| 名称     | 类型  | 描述                                                                                            |
|--------|-----|-----------------------------------------------------------------------------------------------|
| symbol | str | symbol="600077";                                                                              |
| date   | str | date="20220310"; 需要通过 ak.stock_lhb_stock_detail_date_em(symbol="600077") 接口获取相应股票的有龙虎榜详情数据的日期 |
| flag   | str | flag="卖出";  choice of {"买入", "卖出"}                                                            |

输出参数

| 名称          | 类型      | 描述               |
|-------------|---------|------------------|
| 序号          | int64   | -                |
| 交易营业部名称     | object  | -                |
| 买入金额        | float64 | -                |
| 买入金额-占总成交比例 | float64 | -                |
| 卖出金额-占总成交比例 | float64 | -                |
| 净额          | float64 | -                |
| 类型          | object  | 该字段主要处理多种龙虎榜标准问题 |

接口示例

```python
import akshare as ak

stock_lhb_stock_detail_em_df = ak.stock_lhb_stock_detail_em(symbol="600077", date="20070416", flag="买入")
print(stock_lhb_stock_detail_em_df)
```

数据示例

```
   序号                  交易营业部名称  ...          净额                        类型
0   1           国泰君安证券股份有限公司总部  ...  5025114.99  有价格涨跌幅限制的日换手率达到20％的前三只证券
1   2  中银国际证券有限责任公司武汉黄孝河路证券营业部  ...  3435790.02  有价格涨跌幅限制的日换手率达到20％的前三只证券
2   3    华泰证券有限责任公司梧州蝶山二路证券营业部  ...  2723460.00  有价格涨跌幅限制的日换手率达到20％的前三只证券
3   4    东吴证券有限责任公司昆山前进中路证券营业部  ...  1844064.62  有价格涨跌幅限制的日换手率达到20％的前三只证券
4   5    国信证券有限责任公司深圳红岭中路证券营业部  ...  1770274.92  有价格涨跌幅限制的日换手率达到20％的前三只证券
[5 rows x 8 columns]
```
