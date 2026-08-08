---
title: "macro_china_hk_market_info - 人民币香港银行同业拆息"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_hk_market_info

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 人民币香港银行同业拆息
- 描述: 香港同业拆借报告, 数据区间从 20170320-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_hk_market_info
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 人民币香港银行同业拆息

接口: macro_china_hk_market_info

目标地址: https://datacenter.jin10.com/reportType/dc_hk_market_info

描述: 香港同业拆借报告, 数据区间从 20170320-至今

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称      | 类型      | 描述    |
|---------|---------|-------|
| 日期      | object  | 日期    |
| O/N-定价  | float64 | -     |
| O/N-涨跌幅 | float64 | 单位: 点 |
| 1W-定价   | float64 | -     |
| 1W-涨跌幅  | float64 | 单位: 点 |
| 2W-定价   | float64 | -     |
| 2W-涨跌幅  | float64 | 单位: 点 |
| 1M-定价   | float64 | -     |
| 1M-涨跌幅  | float64 | 单位: 点 |
| 3M-定价   | float64 | -     |
| 3M-涨跌幅  | float64 | 单位: 点 |
| 6M-定价   | float64 | -     |
| 6M-涨跌幅  | float64 | 单位: 点 |
| 9M-定价   | float64 | -     |
| 9M-涨跌幅  | float64 | 单位: 点 |
| 1Y-定价   | float64 | -     |
| 1Y-涨跌幅  | float64 | 单位: 点 |
| ON-定价   | float64 | -     |
| ON-涨跌幅  | float64 | 单位: 点 |
| 2M-定价   | float64 | -     |
| 2M-涨跌幅  | float64 | 单位: 点 |

接口示例

```python
import akshare as ak

macro_china_hk_market_info_df = ak.macro_china_hk_market_info()
print(macro_china_hk_market_info_df)
```

数据示例

```
         日期   1W-定价  1W-涨跌幅   2W-定价  ...   ON-定价  ON-涨跌幅   2M-定价  2M-涨跌幅
0     2017-03-20  3.9428     NaN  4.2417  ...  2.0283     NaN  4.5915     NaN
1     2017-03-21  3.9094   -3.34  4.1647  ...  2.3883   36.00  4.6113    1.98
2     2017-03-22  4.3795   47.01  4.5853  ...  2.3100   -7.83  4.8365   22.52
3     2017-03-23  4.3538   -2.57  4.3930  ...  2.2263   -8.37  4.5410  -29.55
4     2017-03-24  4.3542    0.03  4.4410  ...  2.2438    1.75  4.6405    9.95
          ...     ...     ...     ...  ...     ...     ...     ...     ...
1729  2024-03-27  3.9303   26.59  3.9194  ...  5.9838  170.12  3.7000    7.86
1730  2024-03-28  4.6167   68.64  4.4297  ...  5.4012  -58.26  3.7000    0.00
1731  2024-04-02  4.7386   12.20  4.5751  ...  5.1127  -28.85  3.9600   26.00
1732  2024-04-03  4.7218   -1.68  4.5127  ...  5.0232   -8.96  4.0177    5.77
1733  2024-04-05  4.4933  -22.85  4.3118  ...  3.1500 -187.32  3.9300   -8.77
[1734 rows x 17 columns]
```
