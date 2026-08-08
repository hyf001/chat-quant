---
title: "air_quality_hebei - 近期空气质量"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, others, parameters, returns, example]
sources: [raw/data-dictionary/others/others.md]
confidence: high
---
# air_quality_hebei

- 分类: [[others-others|AKShare 另类数据]]
- 主题路径: AKShare 另类数据 > 空气质量-河北 > 近期空气质量
- 描述: 河北省实时空气质量数据
- 目标地址: http://218.11.10.130:8080/#/application/home
- 限量: 单次返回所有城市数据
- 来源页面: https://akshare.akfamily.xyz/data/others/others.html

## 相关

- [[others-others|AKShare 另类数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 近期空气质量

接口: air_quality_hebei

目标地址: http://218.11.10.130:8080/#/application/home

描述: 河北省实时空气质量数据

限量: 单次返回所有城市数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称         | 类型      | 描述            |
|------------|---------|---------------|
| 城市         | object  | 城市名称          |
| 区域         | object  | 城市下属行政区域      |
| 监测点        | object  | 监测站点名称        |
| 时间         | object  | 监测时间          |
| AQI        | float64 | 空气质量指数        |
| 空气质量等级     | object  | 空气质量级别(优、良等)  |
| 首要污染物      | object  | 主要污染物         |
| 经度         | float64 | 监测站点经度        |
| 纬度         | float64 | 监测站点纬度        |
| PM10_IAQI  | float64 | PM10空气质量分指数   |
| PM10_浓度    | float64 | PM10浓度值       |
| PM2.5_IAQI | float64 | PM2.5空气质量分指数  |
| PM2.5_浓度   | float64 | PM2.5浓度值      |
| 一氧化碳_IAQI  | float64 | CO空气质量分指数     |
| 一氧化碳_浓度    | float64 | CO浓度值         |
| 二氧化氮_IAQI  | float64 | NO2空气质量分指数    |
| 二氧化氮_浓度    | float64 | NO2浓度值        |
| 二氧化硫_IAQI  | float64 | SO2空气质量分指数    |
| 二氧化硫_浓度    | float64 | SO2浓度值        |
| 臭氧1小时_IAQI | float64 | O3 1小时空气质量分指数 |
| 臭氧1小时_浓度   | float64 | O3 1小时浓度值     |
| 臭氧8小时_IAQI | float64 | O3 8小时空气质量分指数 |
| 臭氧8小时_浓度   | float64 | O3 8小时浓度值     |

接口示例

```python
import akshare as ak

air_quality_hebei_df = ak.air_quality_hebei()
print(air_quality_hebei_df)
```

数据示例

```
       城市   区域         监测点  ... 臭氧1小时_浓度  臭氧8小时_IAQI 臭氧8小时_浓度
0    石家庄市  长安区    市区22中南校区  ...     15.0         0.0     40.0
1    石家庄市  栾城区      栾城区星河路  ...      8.0         0.0     40.0
2    石家庄市  鹿泉区    鹿泉住建局(*)  ...     29.0         0.0     41.0
3    石家庄市  藁城区     藁城九中(*)  ...     16.0         0.0     43.0
4    石家庄市  桥西区      市区西南高教  ...      7.0         0.0     41.0
..    ...  ...         ...  ...      ...         ...      ...
359   衡水市  武强县   武强实验学校(*)  ...     11.0         0.0     38.0
360   衡水市   景县    景县交通局(*)  ...     28.0         0.0     48.0
361   衡水市  武邑县   武邑县委党校(*)  ...     16.0         0.0     36.0
362   衡水市   景县  景县市场监管局(*)  ...     33.0         0.0     58.0
363   衡水市  阜城县    阜城交通局(*)  ...     30.0         0.0     48.0
[364 rows x 23 columns]
```
