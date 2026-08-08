---
title: "macro_china_market_margin_sz - 深圳融资融券报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_market_margin_sz

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 其他指标 > 深圳融资融券报告
- 描述: 深圳融资融券报告, 数据区间从 20100331-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_market_margin_sz
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 深圳融资融券报告

接口: macro_china_market_margin_sz

目标地址: https://datacenter.jin10.com/reportType/dc_market_margin_sz

描述: 深圳融资融券报告, 数据区间从 20100331-至今

限量: 单次返回所有历史数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称     | 类型      | 描述      |
|--------|---------|---------|
| 日期     | object  | -       |
| 融资买入额  | float64 | 注意单位: 元 |
| 融资余额   | float64 | 注意单位: 元 |
| 融券卖出量  | float64 | 注意单位: 股 |
| 融券余量   | float64 | 注意单位: 股 |
| 融券余额   | float64 | 注意单位: 元 |
| 融资融券余额 | float64 | 注意单位: 元 |

接口示例

```python
import akshare as ak

macro_china_market_margin_sz_df = ak.macro_china_market_margin_sz()
print(macro_china_market_margin_sz_df)
```

数据示例

```
         日期       融资买入额  ...          融券余额        融资融券余额
0     2010-03-31  6.845690e+05  ...  7.089500e+04  7.416910e+05
1     2010-04-08  6.713260e+06  ...  5.602300e+04  1.452378e+07
2     2010-04-09  9.357095e+06  ...  1.083620e+05  1.984136e+07
3     2010-04-12  1.040656e+07  ...  8.100000e+03  2.482113e+07
4     2010-04-15  1.660717e+07  ...  9.767600e+04  4.807796e+07
          ...           ...  ...           ...           ...
3374  2024-03-27  3.589356e+10  ...  1.500044e+10  7.222717e+11
3375  2024-03-28  4.240178e+10  ...  1.527372e+10  7.247246e+11
3376  2024-03-29  3.843272e+10  ...  1.540008e+10  7.220648e+11
3377  2024-04-01  5.034045e+10  ...  1.579884e+10  7.264701e+11
3378  2024-04-02  4.460770e+10  ...  1.577416e+10  7.271902e+11
[3379 rows x 7 columns]
```
