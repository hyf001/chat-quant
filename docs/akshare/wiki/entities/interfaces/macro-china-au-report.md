---
title: "macro_china_au_report - 上海黄金交易所报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_au_report

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 其他指标 > 上海黄金交易所报告
- 描述: 上海黄金交易所报告, 数据区间从 20140905-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_sge_report
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 上海黄金交易所报告

接口: macro_china_au_report

目标地址: https://datacenter.jin10.com/reportType/dc_sge_report

描述: 上海黄金交易所报告, 数据区间从 20140905-至今

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称    | 类型      | 描述  |
|-------|---------|-----|
| 日期    | object  | -   |
| 商品    | object  | -   |
| 开盘价   | float64 | -   |
| 最高价   | float64 | -   |
| 最低价   | float64 | -   |
| 收盘价   | float64 | -   |
| 涨跌    | float64 | -   |
| 涨跌幅   | float64 | -   |
| 加权平均价 | float64 | -   |
| 成交量   | float64 | -   |
| 成交金额  | float64 | -   |
| 持仓量   | float64 | -   |
| 交收方向  | object  | -   |
| 交收量   | float64 | -   |

接口示例

```python
import akshare as ak

macro_china_au_report_df = ak.macro_china_au_report()
print(macro_china_au_report_df)
```

数据示例

```
               日期        商品      开盘价  ...        持仓量   交收方向      交收量
0      2014-09-05    Pt9995   293.50  ...        NaN             NaN
1      2014-09-05   Ag(T+D)  4159.00  ...  5252236.0   空支付多      NaN
2      2014-09-05   Ag99.99  4218.00  ...      322.0             NaN
3      2014-09-05   Au(T+D)   250.52  ...   144574.0   多支付空  11848.0
4      2014-09-05  mAu(T+D)   250.87  ...   130808.0   多支付空  23644.0
           ...       ...      ...  ...        ...    ...      ...
24389  2023-03-23  NYAuTN12   437.60  ...    28328.0             NaN
24390  2023-03-23    PGC30g   444.00  ...        NaN             NaN
24391  2023-03-23   Pt99.95   227.20  ...        NaN             NaN
24392  2023-03-23   Au99.99   434.00  ...        NaN             NaN
24393  2023-03-23   Ag(T+D)  5108.00  ...  4965526.0  空支付给多  17670.0
```
