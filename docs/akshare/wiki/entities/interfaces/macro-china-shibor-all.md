---
title: "macro_china_shibor_all - 上海银行业同业拆借报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_shibor_all

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 上海银行业同业拆借报告
- 描述: 上海银行业同业拆借报告, 数据区间从 20170317-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_shibor
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 上海银行业同业拆借报告

接口: macro_china_shibor_all

目标地址: https://datacenter.jin10.com/reportType/dc_shibor

描述: 上海银行业同业拆借报告, 数据区间从 20170317-至今

限量: 单次返回所有历史数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称      | 类型      | 默 描述  |
|---------|---------|-------|
| 日期      | object  | -     |
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
| 1Y-涨跌幅  | float   | 单位: 点 |
| ON-定价   | float64 | -     |
| ON-涨跌幅  | float64 | 单位: 点 |
| 2M-定价   | float64 | -     |
| 2M-涨跌幅  | float64 | 单位: 点 |

接口示例

```python
import akshare as ak

macro_china_shibor_all_df = ak.macro_china_shibor_all()
print(macro_china_shibor_all_df)
```

数据示例

```
              日期  O/N-定价  O/N-涨跌幅   1W-定价  ...   9M-定价  9M-涨跌幅   1Y-定价  1Y-涨跌幅
0     2015-05-08  1.4430      NaN  2.3340  ...  4.3960     NaN  4.5000     NaN
1     2017-03-17  2.6330   119.00  2.7250  ...  4.1340  -26.20  4.1246  -37.54
2     2017-03-20  2.6325    -0.05  2.7471  ...  4.1504    1.64  4.1435    1.89
3     2017-03-21  2.6477     1.52  2.7680  ...  4.1621    1.17  4.1559    1.24
4     2017-03-22  2.6507     0.30  2.7910  ...  4.1713    0.92  4.1649    0.90
          ...     ...      ...     ...  ...     ...     ...     ...     ...
1753  2024-03-28  1.7340    -3.60  1.9480  ...  2.2380    0.00  2.2670    0.10
1754  2024-03-29  1.7180    -1.60  1.9670  ...  2.2380    0.00  2.2680    0.10
1755  2024-04-01  1.7280     1.00  1.8570  ...  2.2350   -0.30  2.2650   -0.30
1756  2024-04-02  1.7040    -2.40  1.8330  ...  2.2330   -0.20  2.2620   -0.30
1757  2024-04-03  1.6850    -1.90  1.8210  ...  2.2270   -0.60  2.2560   -0.60
[1758 rows x 17 columns]
```
