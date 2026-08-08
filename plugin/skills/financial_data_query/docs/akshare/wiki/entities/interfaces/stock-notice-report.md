---
title: "stock_notice_report - 沪深京 A 股公告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_notice_report

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 沪深京 A 股公告
- 描述: 东方财富网-数据中心-公告大全-沪深京 A 股公告
- 目标地址: https://data.eastmoney.com/notices/hsa/5.html
- 限量: 单次获取指定 symbol 和 date 的数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 沪深京 A 股公告

接口: stock_notice_report

目标地址: https://data.eastmoney.com/notices/hsa/5.html

描述: 东方财富网-数据中心-公告大全-沪深京 A 股公告

限量: 单次获取指定 symbol 和 date 的数据

输入参数

| 名称     | 类型  | 描述                                                                                      |
|--------|-----|-----------------------------------------------------------------------------------------|
| symbol | str | symbol='财务报告'; choice of {"全部", "重大事项", "财务报告", "融资公告", "风险提示", "资产重组", "信息变更", "持股变动"} |
| date   | str | date="20220511"; 指定日期                                                                   |

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

stock_notice_report_df = ak.stock_notice_report(symbol='财务报告', date="20240613")
print(stock_notice_report_df)
```

数据示例

```
      代码  ...                                       网址
0    123122  ...  https://data.eastmoney.com/notices/detail/1231...
1    123107  ...  https://data.eastmoney.com/notices/detail/1231...
2    300941  ...  https://data.eastmoney.com/notices/detail/3009...
3    300689  ...  https://data.eastmoney.com/notices/detail/3006...
4    300854  ...  https://data.eastmoney.com/notices/detail/3008...
..      ...  ...                                                ...
134  000159  ...  https://data.eastmoney.com/notices/detail/0001...
135  688478  ...  https://data.eastmoney.com/notices/detail/6884...
136  688513  ...  https://data.eastmoney.com/notices/detail/6885...
137  600583  ...  https://data.eastmoney.com/notices/detail/6005...
138  001301  ...  https://data.eastmoney.com/notices/detail/0013...
[139 rows x 6 columns]
```
