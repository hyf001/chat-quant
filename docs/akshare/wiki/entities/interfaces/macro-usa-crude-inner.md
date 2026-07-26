---
title: "macro_usa_crude_inner - 美国原油产量报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_usa_crude_inner

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 美国宏观 > 其他 > 美国原油产量报告
- 描述: 美国原油产量报告, 数据区间从 19830107-至今, 每周三公布(美国节假日除外), 美国能源信息署(EIA)
- 目标地址: https://datacenter.jin10.com/reportType/dc_eia_crude_oil_produce
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 美国原油产量报告

接口: macro_usa_crude_inner

目标地址: https://datacenter.jin10.com/reportType/dc_eia_crude_oil_produce

描述: 美国原油产量报告, 数据区间从 19830107-至今, 每周三公布(美国节假日除外), 美国能源信息署(EIA)

限量: 单次返回所有历史数据

1. 报告内容: 美国能源信息署（EIA）在北京时间每周三晚公布EIA报告，除了公布美国原油库存、汽油库存等数据外，报告还包含美国上周国内原油产量的数据。
2. 报告组成：美国国内原油产量、美国本土48州原油产量和美国阿拉斯加州原油产量。
3. 数据关系：美国国内原油产量=美国本土48州原油产量+美国阿拉斯加州原油产量 单位均为万桶/日。
4. 数据解读: 该数据反映了美国原油供应侧的情况，理论而言，当美国国内原油产量录得增加，通常导致油价下跌；当产量减少，则通常导致油价上扬。

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称             | 类型      | 描述 |
|----------------|---------|----|
| 日期             | object  | -  |
| 美国国内原油总量-产量    | float64 | -  |
| 美国国内原油总量-变化    | float64 | -  |
| 美国本土48州原油产量-产量 | float64 | -  |
| 美国本土48州原油产量-变化 | float64 | -  |
| 美国阿拉斯加州原油产量-产量 | float64 | -  |
| 美国阿拉斯加州原油产量-变化 | float64 | -  |

接口示例

```python
import akshare as ak

macro_usa_crude_inner_df = ak.macro_usa_crude_inner()
print(macro_usa_crude_inner_df)
```

数据示例

```
       日期  美国国内原油总量-产量  ...  美国阿拉斯加州原油产量-产量  美国阿拉斯加州原油产量-变化
0     1983-01-07        863.4  ...             0.0             NaN
1     1983-01-14        863.4  ...             0.0             0.0
2     1983-01-21        863.4  ...             0.0             0.0
3     1983-01-28        863.4  ...             0.0             0.0
4     1983-02-04        866.0  ...             0.0             0.0
          ...          ...  ...             ...             ...
2144  2024-03-01       1320.0  ...            43.6             0.4
2145  2024-03-08       1310.0  ...            43.2            -0.4
2146  2024-03-15       1310.0  ...            44.1             0.9
2147  2024-03-22       1310.0  ...            43.2            -0.9
2148  2024-03-29       1310.0  ...            43.2             0.0
[2149 rows x 7 columns]
```
