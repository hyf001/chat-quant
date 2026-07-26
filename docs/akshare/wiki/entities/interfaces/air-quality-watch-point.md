---
title: "air_quality_watch_point - 监测点空气质量"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, others, parameters, returns, example]
sources: [raw/data-dictionary/others/others.md]
confidence: high
---
# air_quality_watch_point

- 分类: [[others-others|AKShare 另类数据]]
- 主题路径: AKShare 另类数据 > 空气质量-全国 > 监测点空气质量
- 描述: 获取每个城市的所有空气质量监测点的数据
- 目标地址: https://www.zq12369.com/environment.php
- 限量: 单次返回指定城市指定日期区间的所有监测点的空气质量数据
- 来源页面: https://akshare.akfamily.xyz/data/others/others.html

## 相关

- [[others-others|AKShare 另类数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 监测点空气质量

接口: air_quality_watch_point

目标地址: https://www.zq12369.com/environment.php

描述: 获取每个城市的所有空气质量监测点的数据

限量: 单次返回指定城市指定日期区间的所有监测点的空气质量数据

输入参数

| 名称         | 类型     | 描述                                           |
|------------|--------|----------------------------------------------|
| city       | object | city="杭州"; 调用 ak.air_city_table() 接口获取所有城市列表 | |
| start_date | object | start_date="2018-01-01"                      |
| end_date   | object | end_date="2020-04-27"                        |

输出参数

| 名称        | 类型      | 描述    |
|-----------|---------|-------|
| pointname | object  | 监测点名称 |
| aqi       | float64 | AQI   |
| pm2_5     | float64 | PM2.5 |
| pm10      | float64 | PM10  |
| no2       | float64 | NO2   |
| so2       | float64 | SO2   |
| o3        | float64 | O3    |
| co        | float64 | CO    |

接口示例

```python
import akshare as ak

air_quality_watch_point_df = ak.air_quality_watch_point(city="杭州", start_date="2018-01-01", end_date="2020-04-27")
print(air_quality_watch_point_df)
```

数据示例

```
   pointname      aqi  ...                  o3                  co
0       朝晖五区  83.9315  ...               162.4  1.3581999999999999
1       浙江农大  82.7099  ...                 183                 1.3
2        城厢镇  82.2618  ...                 175              1.2643
3         下沙  81.5554  ...                 175                 1.2
4        临平镇  80.2429  ...               174.6              1.2182
5       和睦小学  79.7488  ...                 170              1.2209
6         西溪  78.5832  ...                 173                 1.1
7         滨江  77.9729  ...                 172                 1.3
8        卧龙桥  71.1863  ...                 161             1.13265
9         云栖  70.4404  ...                 168                 1.2
10       千岛湖  55.8762  ...  143.00000000000003                   1
```
