---
title: "sw_index_third_info - 申万三级行业信息"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# sw_index_third_info

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 申万三级行业信息
- 描述: 申万三级行业信息
- 目标地址: https://legulegu.com/stockdata/sw-industry-overview#level1
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

### 申万三级行业信息

接口: sw_index_third_info

目标地址: https://legulegu.com/stockdata/sw-industry-overview#level1

描述: 申万三级行业信息

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称         | 类型      | 描述  |
|------------|---------|-----|
| 行业代码       | object  |     |
| 行业名称       | object  |     |
| 成份个数       | int64   |     |
| 静态市盈率      | float64 |     |
| TTM(滚动)市盈率 | float64 |     |
| 市净率        | float64 |     |
| 静态股息率      | float64 |     |

接口示例

```python
import akshare as ak

sw_index_third_info_df = ak.sw_index_third_info()
print(sw_index_third_info_df)
```

数据示例

```
     行业代码      行业名称   上级行业  成份个数  静态市盈率  TTM(滚动)市盈率 市净率 静态股息率
0    850111.SI        种子    种植业     8  49.00       53.27  3.63   0.78
1    850113.SI     其他种植业    种植业     5  71.56       67.46  2.31   0.27
2    850122.SI      水产养殖     渔业     4  70.32       82.58  1.03   0.55
3    850142.SI      畜禽饲料     饲料     9  28.63       64.62  1.84   2.05
4    850151.SI      果蔬加工  农产品加工     5  19.19       30.98  2.97   1.16
..         ...       ...    ...   ...    ...         ...   ...    ...
253  859714.SI    综合环境治理   环境治理    14  11.03       10.15  2.33   1.67
254  859721.SI     环保设备Ⅲ  环保设备Ⅱ    28  24.18       25.12  1.67   2.27
255  859811.SI      生活用纸   个护用品     9  29.10       30.32  2.23   2.72
256  859821.SI  化妆品制造及其他    化妆品     7  23.92       28.49  2.17   1.33
257  859822.SI     品牌化妆品    化妆品     8  26.90       28.81  3.14   1.18
[258 rows x 8 columns]
```
