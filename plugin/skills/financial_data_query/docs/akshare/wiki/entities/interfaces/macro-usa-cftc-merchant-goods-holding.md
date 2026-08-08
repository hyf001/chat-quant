---
title: "macro_usa_cftc_merchant_goods_holding - 商品类商业持仓报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_usa_cftc_merchant_goods_holding

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 重要机构 > 美国商品期货交易委员会 > 商品类商业持仓报告
- 描述: 美国商品期货交易委员会 CFTC 商品类商业持仓报告, 数据区间从 19860115-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_cftc_merchant_goods
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 商品类商业持仓报告

接口: macro_usa_cftc_merchant_goods_holding

目标地址: https://datacenter.jin10.com/reportType/dc_cftc_merchant_goods

描述: 美国商品期货交易委员会 CFTC 商品类商业持仓报告, 数据区间从 19860115-至今

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

macro_usa_cftc_merchant_goods_holding_df = ak.macro_usa_cftc_merchant_goods_holding()
print(macro_usa_cftc_merchant_goods_holding_df)
```

数据示例

```
      日期  纽约原油-多头仓位  纽约原油-空头仓位  ...   玉米-多头仓位   玉米-空头仓位    玉米-净仓位
0     1986-01-15        0.0        0.0  ...  307790.0  307815.0     -25.0
1     1986-01-31        0.0        0.0  ...  323200.0  247390.0   75810.0
2     1986-02-14        0.0        0.0  ...  303885.0  205150.0   98735.0
3     1986-02-28        0.0        0.0  ...  288625.0  204725.0   83900.0
4     1986-03-14        0.0        0.0  ...  276865.0  220480.0   56385.0
          ...        ...        ...  ...       ...       ...       ...
1802  2024-02-27   584071.0   832325.0  ...  670777.0  420149.0  250628.0
1803  2024-03-05   555705.0   827360.0  ...  646676.0  407215.0  239461.0
1804  2024-03-12   600736.0   865790.0  ...  658122.0  459072.0  199050.0
1805  2024-03-19   568958.0   877361.0  ...  683677.0  500187.0  183490.0
1806  2024-03-26   592280.0   907819.0  ...  697082.0  502483.0  194599.0
[1807 rows x 37 columns]
```
