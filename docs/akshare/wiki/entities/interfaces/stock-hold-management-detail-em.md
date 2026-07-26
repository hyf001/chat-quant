---
title: "stock_hold_management_detail_em - 董监高及相关人员持股变动明细"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_hold_management_detail_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 机构推荐 > 董监高及相关人员持股变动明细
- 描述: 东方财富网-数据中心-特色数据-高管持股-董监高及相关人员持股变动明细
- 目标地址: https://data.eastmoney.com/executive/list.html
- 限量: 单次返回所有数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 董监高及相关人员持股变动明细

接口: stock_hold_management_detail_em

目标地址: https://data.eastmoney.com/executive/list.html

描述: 东方财富网-数据中心-特色数据-高管持股-董监高及相关人员持股变动明细

限量: 单次返回所有数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称         | 类型      | 描述 |
|------------|---------|----|
| 日期         | object  | -  |
| 代码         | object  | -  |
| 名称         | object  | -  |
| 变动人        | object  | -  |
| 变动股数       | int64   | -  |
| 成交均价       | int64   | -  |
| 变动金额       | float64 | -  |
| 变动原因       | object  | -  |
| 变动比例       | float64 | -  |
| 变动后持股数     | float64 | -  |
| 持股种类       | object  | -  |
| 董监高人员姓名    | object  | -  |
| 职务         | object  | -  |
| 变动人与董监高的关系 | object  | -  |
| 开始时持有      | float64 | -  |
| 结束后持有      | float64 | -  |

接口示例

```python
import akshare as ak

stock_hold_management_detail_em_df = ak.stock_hold_management_detail_em()
print(stock_hold_management_detail_em_df)
```

数据示例

```
        日期      代码    名称  ... 变动人与董监高的关系    开始时持有  结束后持有
0       2023-08-08  001308  康冠科技  ...         本人  64350.0     74350.0
1       2023-08-08  001308  康冠科技  ...         本人      0.0     38800.0
2       2023-08-07  002533  金杯电工  ...         本人      NaN  45718400.0
3       2023-08-07  300389   艾比森  ...         本人      NaN     50600.0
4       2023-08-07  300827  上能电气  ...         本人      NaN  31879000.0
            ...     ...   ...  ...        ...      ...         ...
141380  2006-05-26  600500  中化国际  ...         本人      0.0      9000.0
141381  2006-03-02  000045  深纺织A  ...         本人      0.0      7050.0
141382  2006-02-17  002039  黔源电力  ...         本人      0.0     10000.0
141383  2005-09-22  000999  华润三九  ...         本人      0.0      2000.0
141384  2004-11-29  000030  富奥股份  ...         本人      0.0      6000.0
[141385 rows x 16 columns]
```
