---
title: "stock_financial_cash_new_ths - 现金流量表"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_financial_cash_new_ths

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 财务报表-同花顺 > 现金流量表
- 描述: 同花顺-财务指标-现金流量表；替换 stock_financial_cash_ths 接口
- 目标地址: https://basic.10jqka.com.cn/astockpc/astockmain/index.html#/financen?code=000063
- 限量: 单次获取现金流量表所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 现金流量表

接口: stock_financial_cash_new_ths

目标地址: https://basic.10jqka.com.cn/astockpc/astockmain/index.html#/financen?code=000063

描述: 同花顺-财务指标-现金流量表；替换 stock_financial_cash_ths 接口

限量: 单次获取现金流量表所有历史数据

输入参数

| 名称        | 类型  | 描述                                                                      |
|-----------|-----|-------------------------------------------------------------------------|
| symbol    | str | symbol="000063"; 股票代码                                                   |
| indicator | str | indicator="按报告期"; choice of {"按报告期", "一季度", "二季度", "三季度", "四季度", "按年度"} |

输出参数

| 名称            | 类型      | 描述 |
|---------------|---------|----|
| report_date   | object  | -  |
| report_name   | object  | -  |
| report_period | object  | -  |
| quarter_name  | object  | -  |
| metric_name   | object  | -  |
| value         | float64 | -  |
| single        | object  | -  |
| yoy           | float64 | -  |
| mom           | object  | -  |
| single_yoy    | object  | -  |

接口示例

```python
import akshare as ak

stock_financial_cash_new_ths_df = ak.stock_financial_cash_new_ths(symbol="000063", indicator="按年度")
print(stock_financial_cash_new_ths_df)
```

数据示例

```
     report_date report_name  ...          mom   single_yoy
0     2024-12-31      2024年报  ...         <NA>         <NA>
1     2024-12-31      2024年报  ...  -0.23161757   0.57803131
2     2024-12-31      2024年报  ...   0.36015447  -0.45630237
3     2024-12-31      2024年报  ...   0.17900055  -0.47569575
4     2024-12-31      2024年报  ...   0.05788915  -0.47553164
...          ...         ...  ...          ...          ...
2425  1998-12-31      1998年报  ...         <NA>         <NA>
2426  1998-12-31      1998年报  ...         <NA>         <NA>
2427  1998-12-31      1998年报  ...         <NA>         <NA>
2428  1998-12-31      1998年报  ...         <NA>         <NA>
2429  1998-12-31      1998年报  ...         <NA>         <NA>
[2430 rows x 10 columns]
```
