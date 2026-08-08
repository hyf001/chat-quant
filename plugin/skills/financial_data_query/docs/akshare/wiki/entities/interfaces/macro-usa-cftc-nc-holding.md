---
title: "macro_usa_cftc_nc_holding - 外汇类非商业持仓报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_usa_cftc_nc_holding

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 重要机构 > 美国商品期货交易委员会 > 外汇类非商业持仓报告
- 描述: 美国商品期货交易委员会CFTC外汇类非商业持仓报告, 数据区间从 19830107-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_cftc_nc_report
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 外汇类非商业持仓报告

接口: macro_usa_cftc_nc_holding

目标地址: https://datacenter.jin10.com/reportType/dc_cftc_nc_report

描述: 美国商品期货交易委员会CFTC外汇类非商业持仓报告, 数据区间从 19830107-至今

限量: 单次返回所有历史数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称      | 类型      | 描述 |
|---------|---------|----|
| 日期      | object  | -  |
| 美元-多头仓位 | float64 | -  |
| ...     | ...     | -  |
| 澳元-净仓位  | float64 | -  |

接口示例

```python
import akshare as ak

macro_usa_cftc_nc_holding_df = ak.macro_usa_cftc_nc_holding()
print(macro_usa_cftc_nc_holding_df)
```

数据示例

```
              日期   美元-多头仓位   美元-空头仓位  ...  澳元-多头仓位   澳元-空头仓位    澳元-净仓位
0     1986-01-15       0.0       0.0  ...      0.0       0.0       0.0
1     1986-01-31       0.0       0.0  ...      0.0       0.0       0.0
2     1986-02-14       0.0       0.0  ...      0.0       0.0       0.0
3     1986-02-28       0.0       0.0  ...      0.0       0.0       0.0
4     1986-03-14       0.0       0.0  ...      0.0       0.0       0.0
          ...       ...       ...  ...      ...       ...       ...
1802  2024-02-27  577840.0  509268.0  ...  49640.0  128816.0  -79176.0
1803  2024-03-05  608135.0  540058.0  ...  53966.0  138709.0  -84743.0
1804  2024-03-12  581059.0  517852.0  ...  41591.0  132431.0  -90840.0
1805  2024-03-19  632995.0  528809.0  ...  38207.0  145745.0 -107538.0
1806  2024-03-26  656753.0  513199.0  ...  34438.0  139890.0 -105452.0
[1807 rows x 28 columns]
```
