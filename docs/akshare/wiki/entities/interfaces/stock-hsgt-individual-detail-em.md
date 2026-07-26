---
title: "stock_hsgt_individual_detail_em - 沪深港通持股-个股详情"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_hsgt_individual_detail_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 沪深港通持股 > 沪深港通持股-个股详情
- 描述: 东方财富网-数据中心-沪深港通-沪深港通持股-具体股票-个股详情
- 目标地址: http://data.eastmoney.com/hsgtcg/StockHdStatistics/002008.html(示例)
- 限量: 单次获取指定 symbol 的在 start_date 和 end_date 之间的所有数据; 注意只能返回 90 个交易日内的数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 沪深港通持股-个股详情

接口: stock_hsgt_individual_detail_em

目标地址: http://data.eastmoney.com/hsgtcg/StockHdStatistics/002008.html(示例)

描述: 东方财富网-数据中心-沪深港通-沪深港通持股-具体股票-个股详情

限量: 单次获取指定 symbol 的在 start_date 和 end_date 之间的所有数据; 注意只能返回 90 个交易日内的数据

输入参数

| 名称         | 类型  | 描述                                              |
|------------|-----|-------------------------------------------------|
| symbol     | str | symbol="002008"                                 |
| start_date | str | start_date="20210830"; 注意只能返回离最近交易日 90 个交易日内的数据 |
| end_date   | str | end_date="20211026"; 注意只能返回离最近交易日 90 个交易日内的数据   |

输出参数

| 名称         | 类型      | 描述      |
|------------|---------|---------|
| 持股日期       | object  | -       |
| 当日收盘价      | float64 | 注意单位: 元 |
| 当日涨跌幅      | float64 | 注意单位: % |
| 机构名称       | object  | -       |
| 持股数量       | int64   | 注意单位: 股 |
| 持股市值       | float64 | 注意单位: 元 |
| 持股数量占A股百分比 | float64 | 注意单位: % |
| 持股市值变化-1日  | float64 | 注意单位: 元 |
| 持股市值变化-5日  | float64 | 注意单位: 元 |
| 持股市值变化-10日 | float64 | 注意单位: 元 |

接口示例

```python
import akshare as ak

stock_hsgt_individual_detail_em_df = ak.stock_hsgt_individual_detail_em(
	symbol="002008",
	start_date="20210830",
	end_date="20211026"
)
print(stock_hsgt_individual_detail_em_df)
```

数据示例

```
      持股日期  当日收盘价   当日涨跌幅  ...  持股市值变化-1日  持股市值变化-5日  持股市值变化-10日
0     2021-10-25  40.05  0.5271  ...   112008.0 -9329832.0    211866.0
1     2021-10-25  40.05  0.5271  ...     1155.0     3795.0     12210.0
2     2021-10-25  40.05  0.5271  ...     8442.0    27738.0    437280.0
3     2021-10-25  40.05  0.5271  ...    26922.0    88458.0    224076.0
4     2021-10-25  40.05  0.5271  ...     1071.0     3519.0     11322.0
          ...    ...     ...  ...        ...        ...         ...
1791  2021-08-30  46.53  5.3668  ...    10428.0    29732.0    142362.0
1792  2021-08-30  46.53  5.3668  ...   120633.0  2329002.0   2330955.0
1793  2021-08-30  46.53  5.3668  ...  5289183.0  4723917.0   7891389.0
1794  2021-08-30  46.53  5.3668  ...   -15768.0  -225276.0         0.0
1795  2021-08-30  46.53  5.3668  ...      474.0      556.0     -3168.0
```
