---
title: "spot_mixed_feed_soozhu - 全国育肥猪合料（含自配料）半月走势"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, spot, parameters, returns, example]
sources: [raw/data-dictionary/spot/spot.md]
confidence: high
---
# spot_mixed_feed_soozhu

- 分类: [[spot-spot|AKShare 现货数据]]
- 主题路径: AKShare 现货数据 > 生猪大数据 > 全国育肥猪合料（含自配料）半月走势
- 描述: 搜猪-生猪大数据-全国育肥猪合料（含自配料）半月走势
- 目标地址: https://www.soozhu.com/price/data/center/
- 限量: 单次返回近半个月的历史数据
- 来源页面: https://akshare.akfamily.xyz/data/spot/spot.html

## 相关

- [[spot-spot|AKShare 现货数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 全国育肥猪合料（含自配料）半月走势

接口: spot_mixed_feed_soozhu

目标地址: https://www.soozhu.com/price/data/center/

描述: 搜猪-生猪大数据-全国育肥猪合料（含自配料）半月走势

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

spot_mixed_feed_soozhu_df = ak.spot_mixed_feed_soozhu()
print(spot_mixed_feed_soozhu_df)
```

数据示例

```
         日期    价格
0   2024-07-29  3.24
1   2024-07-30  3.11
2   2024-07-31  3.24
3   2024-08-01  3.18
4   2024-08-02  3.26
5   2024-08-03  3.35
6   2024-08-04  3.46
7   2024-08-05  3.27
8   2024-08-06  3.19
9   2024-08-07  3.25
10  2024-08-08  3.07
11  2024-08-09  3.30
12  2024-08-10  3.55
13  2024-08-11  3.42
14  2024-08-12  3.22
```
