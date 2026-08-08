---
title: "macro_usa_cftc_c_holding - 商品类非商业持仓报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_usa_cftc_c_holding

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 重要机构 > 美国商品期货交易委员会 > 商品类非商业持仓报告
- 描述: 美国商品期货交易委员会CFTC商品类非商业持仓报告, 数据区间从 19830107-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_cftc_c_report
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 商品类非商业持仓报告

接口: macro_usa_cftc_c_holding

目标地址: https://datacenter.jin10.com/reportType/dc_cftc_c_report

描述: 美国商品期货交易委员会CFTC商品类非商业持仓报告, 数据区间从 19830107-至今

限量: 单次返回所有历史数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称        | 类型      | 描述 |
|-----------|---------|----|
| 日期        | object  | -  |
| 纽约原油-多头仓位 | float64 | -  |
| ...       | ...     | -  |
| 玉米-净仓位    | float64 | -  |

接口示例

```python
import akshare as ak

macro_usa_cftc_c_holding_df = ak.macro_usa_cftc_c_holding()
print(macro_usa_cftc_c_holding_df)
```

数据示例

```
            日期  纽约原油-多头仓位  纽约原油-空头仓位  ...   玉米-多头仓位   玉米-空头仓位    玉米-净仓位
0     1986-01-15        0.0        0.0  ...   45615.0   16565.0   29050.0
1     1986-01-31        0.0        0.0  ...   32135.0   34145.0   -2010.0
2     1986-02-14        0.0        0.0  ...   14030.0   50275.0  -36245.0
3     1986-02-28        0.0        0.0  ...   17735.0   59835.0  -42100.0
4     1986-03-14        0.0        0.0  ...   18725.0   58090.0  -39365.0
          ...        ...        ...  ...       ...       ...       ...
1802  2024-02-27   353996.0   129206.0  ...  295676.0  528280.0 -232604.0
1803  2024-03-05   342161.0   103649.0  ...  291829.0  522716.0 -230887.0
1804  2024-03-12   329318.0    95530.0  ...  297244.0  486274.0 -189030.0
1805  2024-03-19   366016.0    88259.0  ...  294129.0  469642.0 -175513.0
1806  2024-03-26   376903.0    98876.0  ...  293932.0  471953.0 -178021.0
[1807 rows x 37 columns]
```
