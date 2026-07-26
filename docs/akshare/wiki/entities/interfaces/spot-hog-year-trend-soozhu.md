---
title: "spot_hog_year_trend_soozhu - 今年以来全国出栏均价走势"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, spot, parameters, returns, example]
sources: [raw/data-dictionary/spot/spot.md]
confidence: high
---
# spot_hog_year_trend_soozhu

- 分类: [[spot-spot|AKShare 现货数据]]
- 主题路径: AKShare 现货数据 > 生猪大数据 > 今年以来全国出栏均价走势
- 描述: 搜猪-生猪大数据-今年以来全国出栏均价走势
- 目标地址: https://www.soozhu.com/price/data/center/
- 限量: 单次返回近一年所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/spot/spot.html

## 相关

- [[spot-spot|AKShare 现货数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 今年以来全国出栏均价走势

接口: spot_hog_year_trend_soozhu

目标地址: https://www.soozhu.com/price/data/center/

描述: 搜猪-生猪大数据-今年以来全国出栏均价走势

限量: 单次返回近一年所有历史数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称  | 类型      | 描述 |
|-----|---------|----|
| 日期  | object  | -  |
| 价格  | float64 | -  |

接口示例

```python
import akshare as ak

spot_hog_year_trend_soozhu_df = ak.spot_hog_year_trend_soozhu()
print(spot_hog_year_trend_soozhu_df)
```

数据示例

```
         日期     价格
0    2024-01-16  13.81
1    2024-01-17  14.10
2    2024-01-18  14.04
3    2024-01-19  13.79
4    2024-01-20  13.67
..          ...    ...
195  2024-07-29  19.38
196  2024-07-30  19.48
197  2024-07-31  19.66
198  2024-08-01  19.78
199  2024-08-02  19.85
[200 rows x 2 columns]
```
