---
title: "migration_scale_baidu - 迁徙规模"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, event, parameters, returns, example]
sources: [raw/data-dictionary/event/event.md]
confidence: high
---
# migration_scale_baidu

- 分类: [[event-event|AKShare 迁徙数据]]
- 主题路径: AKShare 迁徙数据 > 迁徙数据-百度 > 迁徙规模
- 描述: 百度-百度地图慧眼-百度迁徙-迁徙规模
- 目标地址: https://qianxi.baidu.com/?from=shoubai#city=0
- 限量: 单次返回所有迁徙规模数据
- 来源页面: https://akshare.akfamily.xyz/data/event/event.html

## 相关

- [[event-event|AKShare 迁徙数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 迁徙规模

接口: migration_scale_baidu

目标地址: https://qianxi.baidu.com/?from=shoubai#city=0

描述: 百度-百度地图慧眼-百度迁徙-迁徙规模

- 迁徙规模指数：反映迁入或迁出人口规模，城市间可横向对比
- 城市迁徙边界采用该城市行政区划，包含该城市管辖的区、县、乡、村

限量: 单次返回所有迁徙规模数据

输入参数

| 名称        | 类型  | 描述                                                          |
|-----------|-----|-------------------------------------------------------------|
| area      | str | area="广州市", 输入需要查询的省份或者城市, 都需要用全称, 比如: "浙江省", "乌鲁木齐市"       |
| indicator | str | indicator="move_in", 返回迁入地详情, indicator="move_out", 返回迁出地详情 |

输出参数

| 名称     | 类型      | 描述     |
|--------|---------|--------|
| 日期     | object  | -      |
| 迁徙规模指数 | float64 | 定义参见百度 |

接口示例

```python
import akshare as ak

migration_scale_baidu_df = ak.migration_scale_baidu(area="广州市", indicator="move_in")
print(migration_scale_baidu_df)
```

数据示例

```
         日期     迁徙规模指数
0     2019-01-12   8.413535
1     2019-01-13   7.877218
2     2019-01-14   8.920660
3     2019-01-15   7.426858
4     2019-01-16   7.339183
          ...        ...
1100  2023-09-18  13.620539
1101  2023-09-19   9.761666
1102  2023-09-20   9.755867
1103  2023-09-21  10.397938
1104  2023-09-22  10.492319
[1105 rows x 2 columns]
```
