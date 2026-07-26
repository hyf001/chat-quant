---
title: "spot_hog_crossbred_soozhu - 全国后备二元母猪"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, spot, parameters, returns, example]
sources: [raw/data-dictionary/spot/spot.md]
confidence: high
---
# spot_hog_crossbred_soozhu

- 分类: [[spot-spot|AKShare 现货数据]]
- 主题路径: AKShare 现货数据 > 生猪大数据 > 全国后备二元母猪
- 描述: 搜猪-生猪大数据-全国后备二元母猪
- 目标地址: https://www.soozhu.com/price/data/center/
- 限量: 单次返回近半个月的历史数据
- 来源页面: https://akshare.akfamily.xyz/data/spot/spot.html

## 相关

- [[spot-spot|AKShare 现货数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 全国后备二元母猪

接口: spot_hog_crossbred_soozhu

目标地址: https://www.soozhu.com/price/data/center/

描述: 搜猪-生猪大数据-全国后备二元母猪

限量: 单次返回近半个月的历史数据

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

spot_hog_crossbred_soozhu_df = ak.spot_hog_crossbred_soozhu()
print(spot_hog_crossbred_soozhu_df)
```

数据示例

```
       日期       价格
0   2024-07-26  1945.83
1   2024-07-27  2678.44
2   2024-07-28  2704.33
3   2024-07-29  1852.07
4   2024-07-30  1833.00
5   2024-07-31  1837.78
6   2024-08-01  1966.08
7   2024-08-02  1943.75
8   2024-08-03  2872.67
9   2024-08-04  2695.44
10  2024-08-05  1905.15
11  2024-08-06  1914.64
12  2024-08-07  1830.65
13  2024-08-08  1991.06
14  2024-08-09  1960.00
```
