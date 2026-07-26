---
title: "air_city_table - 城市列表"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, others, parameters, returns, example]
sources: [raw/data-dictionary/others/others.md]
confidence: high
---
# air_city_table

- 分类: [[others-others|AKShare 另类数据]]
- 主题路径: AKShare 另类数据 > 空气质量-全国 > 城市列表
- 描述: 所有能获取空气质量数据的城市表
- 目标地址: https://www.aqistudy.cn/
- 限量: 单次返回所有可以获取的城市表数据
- 来源页面: https://akshare.akfamily.xyz/data/others/others.html

## 相关

- [[others-others|AKShare 另类数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 城市列表

接口: air_city_table

目标地址: https://www.aqistudy.cn/

描述: 所有能获取空气质量数据的城市表

限量: 单次返回所有可以获取的城市表数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称      | 类型      | 描述  |
|---------|---------|-----|
| 序号      | int64   | -   |
| 省份      | object  | -   |
| 城市      | object  | -   |
| AQI     | float64 | -   |
| 空气质量    | object  | -   |
| PM2.5浓度 | object  | -   |
| 首要污染物   | object  | -   |

接口示例

```python
import akshare as ak

air_city_table_df = ak.air_city_table()
print(air_city_table_df)
```

数据示例

```
      序号  省份  城市    AQI  空气质量    PM2.5浓度 首要污染物
0      1  北京  北京  204.0  重度污染  108 ug/m3    O3
1      2  河北  廊坊  199.0  中度污染   54 ug/m3    O3
2      3  河北  承德  198.0  中度污染   59 ug/m3    O3
3      4  河北  唐山  176.0  中度污染   74 ug/m3    O3
4      5  山西  晋城  164.0  中度污染   51 ug/m3    O3
..   ...  ..  ..    ...   ...        ...   ...
163  164  广东  中山   40.0     优   19 ug/m3   NaN
164  165  广东  东莞   39.0     优   20 ug/m3   NaN
165  166  广东  深圳   38.0     优   21 ug/m3   NaN
166  167  广东  珠海   34.0     优   17 ug/m3   NaN
167  168  海南  海口   32.0     优   14 ug/m3   NaN
```
