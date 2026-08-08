---
title: "air_quality_rank - 空气质量排名"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, others, parameters, returns, example]
sources: [raw/data-dictionary/others/others.md]
confidence: high
---
# air_quality_rank

- 分类: [[others-others|AKShare 另类数据]]
- 主题路径: AKShare 另类数据 > 空气质量-全国 > 空气质量排名
- 描述: 获取指定 date 时间点上所有城市(168个)的空气质量数据
- 目标地址: https://www.zq12369.com/environment.php
- 限量: 单次返回所有的数据
- 来源页面: https://akshare.akfamily.xyz/data/others/others.html

## 相关

- [[others-others|AKShare 另类数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 空气质量排名

接口: air_quality_rank

目标地址: https://www.zq12369.com/environment.php

描述: 获取指定 date 时间点上所有城市(168个)的空气质量数据

限量: 单次返回所有的数据

输入参数

| 名称   | 类型  | 描述                                                                                       |
|------|-----|------------------------------------------------------------------------------------------|
| date | str | date=""; "": 当前时刻空气质量排名, 默认; "20200312": 当日空气质量排名; "202003": 当月空气质量排名; "2019": 当年空气质量排名; |

输出参数

| 名称      | 类型    | 描述  |
|---------|-------|-----|
| 降序      | str   | 排名  |
| 省份      | str   | -   |
| 城市      | str   | -   |
| AQI     | float | -   |
| 空气质量    | str   | -   |
| PM2.5浓度 | str   | -   |
| 首要污染物   | str   | -   |

接口示例-实时

```python
import akshare as ak

air_quality_rank_df = ak.air_quality_rank(date="")
print(air_quality_rank_df)
```

数据示例-实时

```
        降序  省份  城市    AQI  空气质量   PM2.5浓度  首要污染物
1      1.0  山西  太原  123.0  轻度污染  93 ug/m3  PM2.5
2      2.0  山东  德州  116.0  轻度污染  33 ug/m3   PM10
3      3.0  河南  安阳  111.0  轻度污染  60 ug/m3   PM10
4      4.0  吉林  长春  108.0  轻度污染  81 ug/m3  PM2.5
5      5.0  广东  佛山  100.0     良  55 ug/m3     O3
..     ...  ..  ..    ...   ...       ...    ...
164  164.0  广东  珠海   34.0     优  16 ug/m3    NaN
165  165.0  江苏  南通   34.0     优  23 ug/m3    NaN
166  166.0  浙江  舟山   30.0     优  11 ug/m3    NaN
167  167.0  四川  雅安   30.0     优  13 ug/m3    NaN
168  168.0  西藏  拉萨   29.0     优   9 ug/m3    NaN
```

接口示例-具体某天

```python
import akshare as ak
air_quality_rank_df = ak.air_quality_rank(date="2020-03-20")
print(air_quality_rank_df)
```

数据示例-具体某天

```
        降序   省份    城市    AQI  空气质量   PM2.5浓度 首要污染物
1      1.0   山西    晋城  124.0  轻度污染  42 ug/m3  PM10
2      2.0   山东    德州  120.0  轻度污染  36 ug/m3  PM10
3      3.0   河南    焦作  118.0  轻度污染  42 ug/m3  PM10
4      4.0   山东    菏泽  118.0  轻度污染  33 ug/m3  PM10
5      5.0   河南    安阳  118.0  轻度污染  44 ug/m3  PM10
..     ...  ...   ...    ...   ...       ...   ...
164  164.0   广东    深圳   45.0     优  29 ug/m3   NaN
165  165.0  黑龙江   哈尔滨   43.0     优  30 ug/m3   NaN
166  166.0   广东    惠州   43.0     优  30 ug/m3   NaN
167  167.0   新疆  乌鲁木齐   32.0     优  17 ug/m3   NaN
168  168.0   海南    海口   29.0     优  13 ug/m3   NaN
```

接口示例-具体某月

```python
import akshare as ak
air_quality_rank_df = ak.air_quality_rank(date="2020-03")
print(air_quality_rank_df)
```

数据示例-具体某月

```
        降序  省份  城市  综合指数  最大指数  首要污染物
1      1.0  河南  安阳  5.29  1.60  PM2.5
2      2.0  山东  淄博  5.27  1.51  PM2.5
3      3.0  山东  枣庄  5.19  1.54  PM2.5
4      4.0  河南  焦作  5.16  1.54   PM10
5      5.0  陕西  西安  5.11  1.59   PM10
..     ...  ..  ..   ...   ...    ...
164  164.0  广东  惠州  2.52  0.69     O3
165  165.0  广东  中山  2.51  0.74     O3
166  166.0  浙江  舟山  2.27  0.70     O3
167  167.0  海南  海口  1.84  0.58     O3
168  168.0  西藏  拉萨  1.78  0.72     O3
```

接口示例-具体某年

```python
import akshare as ak
air_quality_rank_df = ak.air_quality_rank(date="2019")
print(air_quality_rank_df)
```

数据示例-具体某年

```
        降序  省份   城市  综合指数  最大指数  首要污染物
1      1.0  河南   安阳  6.91  2.03  PM2.5
2      2.0  河北   邢台  6.85  1.86  PM2.5
3      3.0  河北  石家庄  6.80  1.80  PM2.5
4      4.0  河北   邯郸  6.77  1.89  PM2.5
5      5.0  山西   临汾  6.74  1.77  PM2.5
..     ...  ..  ...   ...   ...    ...
164  164.0  福建   厦门  2.98  0.84     O3
165  165.0  安徽   黄山  2.95  0.84     O3
166  166.0  浙江   舟山  2.68  0.82     O3
167  167.0  海南   海口  2.47  0.90     O3
168  168.0  西藏   拉萨  2.39  0.81     O3
```
