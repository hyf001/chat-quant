---
title: "macro_usa_gdp_monthly - 美国GDP"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_usa_gdp_monthly

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 美国宏观 > 经济状况 > 美国GDP
- 描述: 美国国内生产总值(GDP)报告, 数据区间从 20080228-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_usa_gdp
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 美国GDP

接口: macro_usa_gdp_monthly

目标地址: https://datacenter.jin10.com/reportType/dc_usa_gdp

描述: 美国国内生产总值(GDP)报告, 数据区间从 20080228-至今

限量: 单次返回所有历史数据

说明: 当前接口使用 Jin10 历史数据接口; 经 2026-07 校验, 该上游链路未继续提供最新数据, 返回结果可能仅更新至 2025 年附近, 不代表 AKShare 本地缓存异常

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称  | 类型      | 描述      |
|-----|---------|---------|
| 商品  | object  | -       |
| 日期  | object  | -       |
| 今值  | float64 | 注意单位: % |
| 预测值 | float64 | 注意单位: % |
| 前值  | float64 | 注意单位: % |

接口示例

```python
import akshare as ak

macro_usa_gdp_monthly_df = ak.macro_usa_gdp_monthly()
print(macro_usa_gdp_monthly_df)
```

数据示例

```
                商品          日期   今值  预测值   前值
0    美国国内生产总值(GDP)  2008-02-28  0.6  0.7  0.6
1    美国国内生产总值(GDP)  2008-03-27  0.6  0.6  0.6
2    美国国内生产总值(GDP)  2008-04-30  0.6  0.2  0.6
3    美国国内生产总值(GDP)  2008-06-26  2.7  1.0  0.9
4    美国国内生产总值(GDP)  2008-07-31  1.9  2.0  1.0
..             ...         ...  ...  ...  ...
188  美国国内生产总值(GDP)  2023-12-21  4.9  5.2  2.1
189  美国国内生产总值(GDP)  2024-01-25  3.3  2.0  4.9
190  美国国内生产总值(GDP)  2024-02-28  3.2  3.3  4.9
191  美国国内生产总值(GDP)  2024-03-28  3.4  3.2  4.9
192  美国国内生产总值(GDP)  2024-04-25  NaN  NaN  3.4
[193 rows x 5 columns]
```
