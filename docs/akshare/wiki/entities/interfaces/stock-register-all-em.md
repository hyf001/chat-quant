---
title: "stock_register_all_em - 全部"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_register_all_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > IPO审核信息 > 全部
- 描述: 东方财富网-数据中心-新股数据-IPO审核信息-全部
- 目标地址: https://data.eastmoney.com/xg/ipo/
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 全部

接口: stock_register_all_em

目标地址: https://data.eastmoney.com/xg/ipo/

描述: 东方财富网-数据中心-新股数据-IPO审核信息-全部

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称     | 类型     | 描述 |
|--------|--------|----|
| 序号     | int64  | -  |
| 企业名称   | object | -  |
| 最新状态   | object | -  |
| 注册地    | object | -  |
| 行业     | object | -  |
| 保荐机构   | object | -  |
| 律师事务所  | object | -  |
| 会计师事务所 | object | -  |
| 更新日期   | object | -  |
| 受理日期   | object | -  |
| 拟上市地点  | object | -  |
| 招股说明书  | object | -  |

接口示例

```python
import akshare as ak

stock_register_all_em_df = ak.stock_register_all_em()
print(stock_register_all_em_df)
```

数据示例

```
       序号  ...                                    招股说明书
0        1  ...  https://pdf.dfcfw.com/pdf/H2_AN202512251807880...
1        2  ...  https://pdf.dfcfw.com/pdf/H2_AN202506301700470...
2        3  ...  https://pdf.dfcfw.com/pdf/H2_AN202512241807247...
3        4  ...  https://pdf.dfcfw.com/pdf/H2_AN202512241807270...
4        5  ...  https://pdf.dfcfw.com/pdf/H2_AN202512241807300...
...    ...  ...                                                ...
4145  4146  ...  https://pdf.dfcfw.com/pdf/H2_AN201609240017728...
4146  4147  ...  https://pdf.dfcfw.com/pdf/H2_AN201607140016578...
4147  4148  ...  https://pdf.dfcfw.com/pdf/H2_AN201611160102988...
4148  4149  ...  https://pdf.dfcfw.com/pdf/H2_AN201410300007493...
4149  4150  ...  https://pdf.dfcfw.com/pdf/H2_AN201611080074226...
[4150 rows x 12 columns]
```
