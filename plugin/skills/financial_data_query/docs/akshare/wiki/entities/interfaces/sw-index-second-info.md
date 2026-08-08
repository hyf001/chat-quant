---
title: "sw_index_second_info - 申万二级行业信息"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# sw_index_second_info

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 申万二级行业信息
- 描述: 申万二级行业信息
- 目标地址: https://legulegu.com/stockdata/sw-industry-overview#level1
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

### 申万二级行业信息

接口: sw_index_second_info

目标地址: https://legulegu.com/stockdata/sw-industry-overview#level1

描述: 申万二级行业信息

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称         | 类型      | 描述  |
|------------|---------|-----|
| 行业代码       | object  |     |
| 行业名称       | object  |     |
| 上级行业       | object  |     |
| 成份个数       | int64   |     |
| 静态市盈率      | float64 |     |
| TTM(滚动)市盈率 | float64 |     |
| 市净率        | float64 |     |
| 静态股息率      | float64 |     |

接口示例

```python
import akshare as ak

sw_index_second_info_df = ak.sw_index_second_info()
print(sw_index_second_info_df)
```

数据示例

```
     行业代码   行业名称  上级行业  成份个数 静态市盈率 TTM(滚动)市盈率 市净率 静态股息率
0    801016.SI    种植业  农林牧渔    19  35.38       37.23  2.69   2.05
1    801015.SI     渔业  农林牧渔     6  29.29       30.42  1.04   0.88
2    801014.SI     饲料  农林牧渔    16  33.07       22.95  3.80   1.22
3    801012.SI  农产品加工  农林牧渔    22  35.96       46.34  2.03   1.26
4    801017.SI    养殖业  农林牧渔    21  10.64        6.61  2.08   1.44
..         ...    ...   ...   ...    ...         ...   ...    ...
119  801963.SI  炼化及贸易  石油石化    31  11.03       11.54  1.04   5.05
120  801971.SI   环境治理    环保   105  18.89       17.79  1.47   1.89
121  801972.SI  环保设备Ⅱ    环保    28  24.18       25.12  1.67   2.27
122  801981.SI   个护用品  美容护理    13  32.54       31.44  2.46   2.59
123  801982.SI    化妆品  美容护理    15  26.26       28.75  2.89   1.21
[124 rows x 8 columns]
```
