---
title: "macro_china_swap_rate - FR007利率互换曲线历史数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_swap_rate

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > FR007利率互换曲线历史数据
- 描述: 国家统计局-FR007利率互换曲线历史数据
- 目标地址: https://www.chinamoney.com.cn/chinese/bkcurvfxhis/?cfgItemType=72&curveType=FR007
- 限量: 单次返回所有历史数据, 该接口只能获取近一年的数据的数据，其中每次只能获取一个月的数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### FR007利率互换曲线历史数据

接口: macro_china_swap_rate

目标地址: https://www.chinamoney.com.cn/chinese/bkcurvfxhis/?cfgItemType=72&curveType=FR007

描述: 国家统计局-FR007利率互换曲线历史数据

限量: 单次返回所有历史数据, 该接口只能获取近一年的数据的数据，其中每次只能获取一个月的数据

输入参数

| 名称         | 类型  | 描述                           |
|------------|-----|------------------------------|
| start_date | str | start_date="20231128"；注意时间间隔 |
| end_date   | str | end_date="20231130"          |

输出参数

| 名称   | 类型      | 描述  |
|------|---------|-----|
| 日期   | object  | -   |
| 曲线名称 | object  | -   |
| 时刻   | object  | -   |
| 价格类型 | object  | -   |
| 1M   | float64 | -   |
| 3M   | float64 | -   |
| 6M   | float64 | -   |
| 9M   | float64 | -   |
| 1Y   | float64 | -   |
| 2Y   | float64 | -   |
| 3Y   | float64 | -   |
| 4Y   | float64 | -   |
| 5Y   | float64 | -   |
| 7Y   | float64 | -   |
| 10Y  | float64 | -   |

接口示例

```python
import akshare as ak

macro_china_swap_rate_df = ak.macro_china_swap_rate(start_date="20240501", end_date="20240531")
print(macro_china_swap_rate_df)
```

数据示例

```
             日期           曲线名称    时刻 价格类型  ...      4Y      5Y      7Y     10Y
0    2024-05-06  FR007利率互换行情曲线   9:30   报卖  ...  2.1375  2.1652  2.5000  2.5000
1    2024-05-06  FR007利率互换行情曲线  13:30   报买  ...  2.0750  2.1350  2.1650  2.2650
2    2024-05-06  FR007利率互换行情曲线  14:00   报卖  ...  2.0944  2.1543  2.2512  2.3263
3    2024-05-06  FR007利率互换行情曲线  14:00   均值  ...  2.0864  2.1530  2.2369  2.3106
4    2024-05-06  FR007利率互换行情曲线  14:00   报买  ...  2.0784  2.1518  2.2225  2.2950
..          ...            ...    ...  ...  ...     ...     ...     ...     ...
940  2024-05-31  FR007利率互换行情曲线  12:30   报卖  ...  2.0000  2.0650  2.2450  2.3350
941  2024-05-31  FR007利率互换行情曲线  12:30   均值  ...  1.9800  2.0450  2.1450  2.2350
942  2024-05-31  FR007利率互换行情曲线  12:30   报买  ...  1.9600  2.0250  2.0450  2.1350
943  2024-05-31  FR007利率互换行情曲线  11:00   均值  ...  1.9775  2.0476  2.1721  2.2687
944  2024-05-31  FR007利率互换收盘曲线  16:30   报买  ...  1.9853  2.0569  2.1525  2.2425
[945 rows x 15 columns]
```
