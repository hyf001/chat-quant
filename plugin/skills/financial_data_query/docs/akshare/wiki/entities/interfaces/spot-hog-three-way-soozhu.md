---
title: "spot_hog_three_way_soozhu - 全国三元仔猪"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, spot, parameters, returns, example]
sources: [raw/data-dictionary/spot/spot.md]
confidence: high
---
# spot_hog_three_way_soozhu

- 分类: [[spot-spot|AKShare 现货数据]]
- 主题路径: AKShare 现货数据 > 生猪大数据 > 全国三元仔猪
- 描述: 搜猪-生猪大数据-全国三元仔猪
- 目标地址: https://www.soozhu.com/price/data/center/
- 限量: 单次返回近半个月的历史数据
- 来源页面: https://akshare.akfamily.xyz/data/spot/spot.html

## 相关

- [[spot-spot|AKShare 现货数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 全国三元仔猪

接口: spot_hog_three_way_soozhu

目标地址: https://www.soozhu.com/price/data/center/

描述: 搜猪-生猪大数据-全国三元仔猪

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

spot_hog_three_way_soozhu_df = ak.spot_hog_three_way_soozhu()
print(spot_hog_three_way_soozhu_df)
```

数据示例

```
         日期      价格
0   2024-07-23  707.29
1   2024-07-24  696.21
2   2024-07-25  674.69
3   2024-07-26  702.08
4   2024-07-27  715.67
5   2024-07-28  722.33
6   2024-07-29  692.26
7   2024-07-30  673.71
8   2024-07-31  684.41
9   2024-08-01  687.30
10  2024-08-02  709.69
11  2024-08-03  679.75
12  2024-08-04  694.00
13  2024-08-05  706.33
14  2024-08-06  718.02
```
