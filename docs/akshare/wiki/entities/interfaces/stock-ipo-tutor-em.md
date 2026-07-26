---
title: "stock_ipo_tutor_em - IPO辅导信息"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_ipo_tutor_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > IPO辅导信息
- 描述: 东方财富网-数据中心-新股申购-IPO辅导信息
- 目标地址: https://data.eastmoney.com/xg/gh/default.html
- 限量: 单次获取所有数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### IPO辅导信息

接口: stock_ipo_tutor_em

目标地址: https://data.eastmoney.com/xg/gh/default.html

描述: 东方财富网-数据中心-新股申购-IPO辅导信息

限量: 单次获取所有数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称      | 类型     | 描述 |
|---------|--------|----|
| 序号      | int64  | -  |
| 企业名称    | object | -  |
| 辅导机构    | object | -  |
| 辅导状态    | object | -  |
| 报告类型    | object | -  |
| 派出机构    | object | -  |
| 备案日期    | object | -  |

接口示例

```python
import akshare as ak

stock_ipo_tutor_em_df = ak.stock_ipo_tutor_em()
print(stock_ipo_tutor_em_df)
```

数据示例

```
     序号  ...        备案日期
0        1  ...  2025-12-23
1        2  ...  2025-12-23
2        3  ...  2025-12-23
3        4  ...  2025-12-23
4        5  ...  2025-12-23
...    ...  ...         ...
5129  5130  ...         NaT
5130  5131  ...         NaT
5131  5132  ...         NaT
5132  5133  ...         NaT
5133  5134  ...         NaT
[5134 rows x 8 columns]
```
