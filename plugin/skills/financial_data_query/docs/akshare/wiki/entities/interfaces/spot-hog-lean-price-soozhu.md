---
title: "spot_hog_lean_price_soozhu - 全国瘦肉型肉猪"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, spot, parameters, returns, example]
sources: [raw/data-dictionary/spot/spot.md]
confidence: high
---
# spot_hog_lean_price_soozhu

- 分类: [[spot-spot|AKShare 现货数据]]
- 主题路径: AKShare 现货数据 > 生猪大数据 > 全国瘦肉型肉猪
- 描述: 搜猪-生猪大数据-全国瘦肉型肉猪
- 目标地址: https://www.soozhu.com/price/data/center/
- 限量: 单次返回近半个月的历史数据
- 来源页面: https://akshare.akfamily.xyz/data/spot/spot.html

## 相关

- [[spot-spot|AKShare 现货数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 全国瘦肉型肉猪

接口: spot_hog_lean_price_soozhu

目标地址: https://www.soozhu.com/price/data/center/

描述: 搜猪-生猪大数据-全国瘦肉型肉猪

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

spot_hog_lean_price_soozhu_df = ak.spot_hog_lean_price_soozhu()
print(spot_hog_lean_price_soozhu_df)
```

数据示例

```
        日期     价格
0   2024-07-21  19.15
1   2024-07-22  19.21
2   2024-07-23  19.38
3   2024-07-24  19.41
4   2024-07-25  19.38
5   2024-07-26  19.32
6   2024-07-27  19.27
7   2024-07-28  19.30
8   2024-07-29  19.38
9   2024-07-30  19.48
10  2024-07-31  19.66
11  2024-08-01  19.78
12  2024-08-02  19.85
13  2024-08-03  19.85
14  2024-08-04  19.80
```
