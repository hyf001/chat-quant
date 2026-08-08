---
title: "spot_soybean_price_soozhu - 全国豆粕价格走势"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, spot, parameters, returns, example]
sources: [raw/data-dictionary/spot/spot.md]
confidence: high
---
# spot_soybean_price_soozhu

- 分类: [[spot-spot|AKShare 现货数据]]
- 主题路径: AKShare 现货数据 > 生猪大数据 > 全国豆粕价格走势
- 描述: 搜猪-生猪大数据-全国豆粕价格走势
- 目标地址: https://www.soozhu.com/price/data/center/
- 限量: 单次返回近半个月的历史数据
- 来源页面: https://akshare.akfamily.xyz/data/spot/spot.html

## 相关

- [[spot-spot|AKShare 现货数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 全国豆粕价格走势

接口: spot_soybean_price_soozhu

目标地址: https://www.soozhu.com/price/data/center/

描述: 搜猪-生猪大数据-全国豆粕价格走势

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

spot_soybean_price_soozhu_df = ak.spot_soybean_price_soozhu()
print(spot_soybean_price_soozhu_df)
```

数据示例

```
         日期    价格
0   2024-07-28  3.53
1   2024-07-29  3.32
2   2024-07-30  3.35
3   2024-07-31  3.36
4   2024-08-01  3.35
5   2024-08-02  3.38
6   2024-08-03  3.55
7   2024-08-04  3.52
8   2024-08-05  3.32
9   2024-08-06  3.40
10  2024-08-07  3.33
11  2024-08-08  3.22
12  2024-08-09  3.25
13  2024-08-10  3.41
14  2024-08-11  3.18
```
