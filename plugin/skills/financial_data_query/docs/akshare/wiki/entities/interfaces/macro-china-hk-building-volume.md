---
title: "macro_china_hk_building_volume - 香港楼宇买卖合约数量"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_hk_building_volume

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国香港宏观 > 香港楼宇买卖合约数量
- 描述: 东方财富-经济数据一览-中国香港-香港楼宇买卖合约数量
- 目标地址: https://data.eastmoney.com/cjsj/foreign_8_5.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 香港楼宇买卖合约数量

接口: macro_china_hk_building_volume

目标地址: https://data.eastmoney.com/cjsj/foreign_8_5.html

描述: 东方财富-经济数据一览-中国香港-香港楼宇买卖合约数量

限量: 单次返回所有历史数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称   | 类型      | 描述  |
|------|---------|-----|
| 时间   | object  | -   |
| 前值   | float64 | -   |
| 现值   | float64 | -   |
| 发布日期 | object  | -   |

接口示例

```python
import akshare as ak

macro_china_hk_building_volume_df = ak.macro_china_hk_building_volume()
print(macro_china_hk_building_volume_df)
```

数据示例

```
          时间    前值     现值      发布日期
0    2008年01月  15592  16984.0  2008-02-04
1    2008年02月  16984  14384.0  2008-03-06
2    2008年03月  14384  10993.0  2008-04-04
3    2008年04月  10993  10945.0  2008-05-05
4    2008年05月  10945  10138.0  2008-06-04
..        ...    ...      ...         ...
190  2023年11月   2938   3532.0  2023-12-04
191  2023年12月   3532   3764.0  2024-01-04
192  2024年01月   3764   4401.0  2024-02-02
193  2024年02月   4401   3189.0  2024-03-04
194  2024年03月   3189      NaN  2024-04-04
[195 rows x 4 columns]
```
