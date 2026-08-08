---
title: "macro_china_society_traffic_volume - 全社会客货运输量"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_society_traffic_volume

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 全社会客货运输量
- 描述: 国家统计局-全社会客货运输量-非累计
- 目标地址: http://finance.sina.com.cn/mac/#industry-10-0-31-1
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 全社会客货运输量

接口: macro_china_society_traffic_volume

目标地址: http://finance.sina.com.cn/mac/#industry-10-0-31-1

描述: 国家统计局-全社会客货运输量-非累计

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称              | 类型      | 描述       |
|-----------------|---------|----------|
| 统计时间            | object  | 年月       |
| 统计对象            | object  | -        |
| 货运量             | float64 | 注意单位: 亿吨 |
| 货运量同比增长         | float64 | 注意单位: %  |
| 货物周转量           | float64 | 注意单位: 亿  |
| 公里货物周转量同比增长     | float64 | 注意单位: %  |
| 客运量             | float64 | 注意单位: 亿人 |
| 客运量同比增长         | float64 | 注意单位: %  |
| 旅客周转量           | float64 | 注意单位: 亿  |
| 公里旅客周转量同比增长     | float64 | 注意单位: %  |
| 沿海主要港口货物吞吐量     | float64 | 注意单位: 亿吨 |
| 沿海主要港口货物吞吐量同比增长 | float64 | 注意单位: %  |
| 其中:外贸货物吞吐量      | float64 | 注意单位: 亿吨 |
| 其中:外贸货物吞吐量同比增长  | float64 | 注意单位: %  |
| 民航总周转量          | float64 | 注意单位: 亿  |
| 公里民航总周转         | float64 | 注意单位: %  |

接口示例

```python
import akshare as ak

macro_china_society_traffic_volume_df = ak.macro_china_society_traffic_volume()
print(macro_china_society_traffic_volume_df)
```

数据示例

```
         统计时间    统计对象    货运量  ...  其中:外贸货物吞吐量同比增长  民航总周转量  公里民航总周转
0      2023.7    国际航线  23.60  ...             NaN    29.9     74.9
1      2023.7  港澳地区航线   1.40  ...             NaN     1.0    488.6
2      2023.7    国内航线  36.50  ...             NaN    83.8     64.6
3      2023.7      民航  60.11  ...             NaN   113.7     67.1
4      2023.7      水运   7.90  ...             NaN     NaN      NaN
       ...     ...    ...  ...             ...     ...      ...
2403  1952.12      水运    NaN  ...             NaN     NaN      NaN
2404  1952.12      公路    NaN  ...             NaN     NaN      NaN
2405  1952.12      铁路    NaN  ...             NaN     NaN      NaN
2406  1952.12      合计    NaN  ...             NaN     NaN      NaN
2407  1952.12      民航    NaN  ...             NaN     NaN      NaN
[2408 rows x 16 columns]
```
