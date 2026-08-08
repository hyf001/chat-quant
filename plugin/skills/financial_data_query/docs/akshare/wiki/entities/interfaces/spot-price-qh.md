---
title: "spot_price_qh - 99 现货走势"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, spot, parameters, returns, example]
sources: [raw/data-dictionary/spot/spot.md]
confidence: high
---
# spot_price_qh

- 分类: [[spot-spot|AKShare 现货数据]]
- 主题路径: AKShare 现货数据 > 99 现货走势
- 描述: 99 期货-数据-期现-现货走势
- 目标地址: https://www.99qh.com/data/spotTrend
- 限量: 单次返回指定 symbol 的所有历史数据；由于数据源限制，只能获取个别品种
- 来源页面: https://akshare.akfamily.xyz/data/spot/spot.html

## 相关

- [[spot-spot|AKShare 现货数据]]
- [[_meta/topic-map]]

## 源文摘录

### 99 现货走势

接口: spot_price_qh

目标地址: https://www.99qh.com/data/spotTrend

描述: 99 期货-数据-期现-现货走势

限量: 单次返回指定 symbol 的所有历史数据；由于数据源限制，只能获取个别品种

输入参数

| 名称     | 类型  | 描述                                                |
|--------|-----|---------------------------------------------------|
| symbol | str | symbol="螺纹钢"; 可以通过 ak.spot_price_table_qh() 获取品种表 |

输出参数

| 名称    | 类型      | 描述 |
|-------|---------|----|
| 日期    | object  | -  |
| 期货收盘价 | float64 | -  |
| 现货价格  | float64 | -  |

接口示例

```python
import akshare as ak

spot_price_qh_df = ak.spot_price_qh(symbol='螺纹钢')
print(spot_price_qh_df)
```

数据示例

```
         日期  期货收盘价  现货价格
0     2012-10-31   3700  3811
1     2012-11-01   3776  3811
2     2012-11-08   3900  3811
3     2012-11-09   3750  3806
4     2012-11-14   3810  3761
...          ...    ...   ...
2466  2024-05-10   3662  3561
2467  2024-05-13   3686  3545
2468  2024-05-14   3630  3552
2469  2024-05-15   3621  3530
2470  2024-05-16   3703  3533
[2471 rows x 3 columns]
```
