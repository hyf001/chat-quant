---
title: "macro_china_ppi - 工业品出厂价格指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_ppi

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 工业品出厂价格指数
- 描述: 工业品出厂价格指数, 数据区间从 200601 至今, 月度数据
- 目标地址: http://data.eastmoney.com/cjsj/ppi.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 工业品出厂价格指数

接口: macro_china_ppi

目标地址: http://data.eastmoney.com/cjsj/ppi.html

描述: 工业品出厂价格指数, 数据区间从 200601 至今, 月度数据

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称     | 类型      | 描述      |
|--------|---------|---------|
| 月份     | object  | -       |
| 当月     | float64 | -       |
| 当月同比增长 | float64 | 注意单位: % |
| 累计     | float64 | -       |

接口示例

```python
import akshare as ak

macro_china_ppi_df = ak.macro_china_ppi()
print(macro_china_ppi_df)
```

数据示例

```
            月份       当月  当月同比增长        累计
0    2022年10月份   98.700   -1.30  105.2000
1    2022年09月份  100.948    0.90  105.9397
2    2022年08月份  102.300    2.30  106.6000
3    2022年07月份  104.200    4.20  107.2000
4    2022年06月份  106.100    6.10  107.7000
..         ...      ...     ...       ...
197  2006年05月份  102.430    2.43  102.5700
198  2006年04月份  101.870    1.87  102.6000
199  2006年03月份  102.490    2.49  102.9000
200  2006年02月份  103.010    3.01  103.0000
201  2006年01月份  103.050    3.05  103.0500
```
