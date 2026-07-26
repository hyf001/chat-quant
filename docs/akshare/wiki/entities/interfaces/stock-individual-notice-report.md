---
title: "stock_individual_notice_report - 沪深京 A 股个股公告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_individual_notice_report

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 沪深京 A 股个股公告
- 描述: 东方财富网-数据中心-公告大全-个股
- 目标地址: https://data.eastmoney.com/notices/stock/300237.html
- 限量: 单次获取指定 security, symbol, begin_date 和 end_date 的数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 沪深京 A 股个股公告

接口: stock_individual_notice_report

目标地址: https://data.eastmoney.com/notices/stock/300237.html

描述: 东方财富网-数据中心-公告大全-个股

限量: 单次获取指定 security, symbol, begin_date 和 end_date 的数据

输入参数

| 名称         | 类型  | 描述                                                                                      |
|------------|-----|-----------------------------------------------------------------------------------------|
| security   | str | security="300237"; 股票代码                                                                 |
| symbol     | str | symbol='财务报告'; choice of {"全部", "重大事项", "财务报告", "融资公告", "风险提示", "资产重组", "信息变更", "持股变动"} |
| begin_date | str | date="20250408"; 指定开始日期; 默认为空即不限制开始日期                                                   |
| end_date   | str | date="20260408"; 指定结束日期; 默认为空即不限制结束日期                                                   |

输出参数

| 名称   | 类型     | 描述  |
|------|--------|-----|
| 代码   | object | -   |
| 名称   | object | -   |
| 公告标题 | object | -   |
| 公告类型 | object | -   |
| 公告日期 | object | -   |
| 网址   | object | -   |

接口示例

```python
import akshare as ak

stock_individual_notice_report_df = ak.stock_individual_notice_report(security="300237", symbol="财务报告", begin_date="20250401", end_date="20260101")
print(stock_individual_notice_report_df)
```

数据示例

```
    代码    名称  ...        公告日期                          网址
0   300237  ST美晨  ...  2025-10-31  https://data.eastmoney.com/notices/detail/3002...
1   300237  ST美晨  ...  2025-10-31  https://data.eastmoney.com/notices/detail/3002...
2   300237  ST美晨  ...  2025-10-31  https://data.eastmoney.com/notices/detail/3002...
3   300237  ST美晨  ...  2025-10-31  https://data.eastmoney.com/notices/detail/3002...
4   300237  ST美晨  ...  2025-08-26  https://data.eastmoney.com/notices/detail/3002...
5   300237  ST美晨  ...  2025-08-26  https://data.eastmoney.com/notices/detail/3002...
6   300237  ST美晨  ...  2025-05-13  https://data.eastmoney.com/notices/detail/3002...
7   300237  ST美晨  ...  2025-04-26  https://data.eastmoney.com/notices/detail/3002...
8   300237  ST美晨  ...  2025-04-22  https://data.eastmoney.com/notices/detail/3002...
9   300237  ST美晨  ...  2025-04-22  https://data.eastmoney.com/notices/detail/3002...
10  300237  ST美晨  ...  2025-04-22  https://data.eastmoney.com/notices/detail/3002...
11  300237  ST美晨  ...  2025-04-22  https://data.eastmoney.com/notices/detail/3002...
12  300237  ST美晨  ...  2025-04-22  https://data.eastmoney.com/notices/detail/3002...
13  300237  ST美晨  ...  2025-04-22  https://data.eastmoney.com/notices/detail/3002...
14  300237  ST美晨  ...  2025-04-22  https://data.eastmoney.com/notices/detail/3002...
15  300237  ST美晨  ...  2025-01-21  https://data.eastmoney.com/notices/detail/3002...
[16 rows x 6 columns]
```
