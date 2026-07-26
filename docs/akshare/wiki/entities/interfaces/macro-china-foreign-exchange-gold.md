---
title: "macro_china_foreign_exchange_gold - 央行黄金和外汇储备"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_foreign_exchange_gold

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 央行黄金和外汇储备
- 描述: 国家统计局-央行黄金和外汇储备, 比东财接口数据时间长
- 目标地址: http://finance.sina.com.cn/mac/#fininfo-5-0-31-2
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 央行黄金和外汇储备

接口: macro_china_foreign_exchange_gold

目标地址: http://finance.sina.com.cn/mac/#fininfo-5-0-31-2

描述: 国家统计局-央行黄金和外汇储备, 比东财接口数据时间长

限量: 单次返回所有历史数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称     | 类型      | 描述        |
|--------|---------|-----------|
| 统计时间   | object  | 年月        |
| 黄金储备   | float64 | 注意单位: 万盎司 |
| 国家外汇储备 | float64 | 注意单位: 亿美元 |

接口示例

```python
import akshare as ak

macro_china_foreign_exchange_gold_df = ak.macro_china_foreign_exchange_gold()
print(macro_china_foreign_exchange_gold_df)
```

数据示例

```
        统计时间     黄金储备    国家外汇储备
0    1978.12  1280.00      1.67
1    1979.12  1280.00      8.40
2    1980.12  1280.00    -12.96
3    1981.12  1267.00     27.08
4    1982.12  1267.00     69.86
..       ...      ...       ...
384   2023.7  6869.00  32042.70
385   2023.8  6962.00  31600.98
386   2023.9  7046.00  31150.70
387   2024.1  7219.00  32193.20
388   2024.2  7258.00  32258.17
[389 rows x 3 columns]
```
