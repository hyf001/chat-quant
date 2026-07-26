---
title: "spot_corn_price_soozhu - 全国玉米价格走势"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, spot, parameters, returns, example]
sources: [raw/data-dictionary/spot/spot.md]
confidence: high
---
# spot_corn_price_soozhu

- 分类: [[spot-spot|AKShare 现货数据]]
- 主题路径: AKShare 现货数据 > 生猪大数据 > 全国玉米价格走势
- 描述: 搜猪-生猪大数据-全国玉米价格走势
- 目标地址: https://www.soozhu.com/price/data/center/
- 限量: 单次返回近半个月的历史数据
- 来源页面: https://akshare.akfamily.xyz/data/spot/spot.html

## 相关

- [[spot-spot|AKShare 现货数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 全国玉米价格走势

接口: spot_corn_price_soozhu

目标地址: https://www.soozhu.com/price/data/center/

描述: 搜猪-生猪大数据-全国玉米价格走势

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

spot_corn_price_soozhu_df = ak.spot_corn_price_soozhu()
print(spot_corn_price_soozhu_df)
```

数据示例

```
         日期    价格
0   2024-07-27  2.50
1   2024-07-28  2.47
2   2024-07-29  2.51
3   2024-07-30  2.45
4   2024-07-31  2.43
5   2024-08-01  2.41
6   2024-08-02  2.45
7   2024-08-03  2.52
8   2024-08-04  2.36
9   2024-08-05  2.45
10  2024-08-06  2.45
11  2024-08-07  2.46
12  2024-08-08  2.40
13  2024-08-09  2.45
14  2024-08-10  2.57
```
