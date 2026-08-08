---
title: "index_ti_cx - 科技投入指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# index_ti_cx

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 财新指数 > 科技投入指数
- 描述: 财新指数-科技投入指数
- 目标地址: https://yun.ccxe.com.cn/indices/nei
- 限量: 该接口返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 科技投入指数

接口: index_ti_cx

目标地址: https://yun.ccxe.com.cn/indices/nei

描述: 财新指数-科技投入指数

限量: 该接口返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称     | 类型      | 描述  |
|--------|---------|-----|
| 日期     | object  | -   |
| 科技投入指数 | float64 | -   |
| 变化值    | float64 | -   |

接口示例

```python
import akshare as ak

index_ti_cx_df = ak.index_ti_cx()
print(index_ti_cx_df)
```

数据示例

```
        日期     科技投入指数   变化值
0   2015-07-31  27.562400  0.000000
1   2015-08-31  23.012985 -4.549415
2   2015-09-30  25.229635  2.216650
3   2015-10-31  25.949450  0.719815
4   2015-11-30  24.258245 -1.691205
..         ...        ...       ...
73  2021-08-31  27.384085 -0.104765
74  2021-09-30  27.670710  0.286625
75  2021-10-31  29.044460  1.373750
76  2021-11-30  26.347445 -2.697015
77  2021-12-31  26.504550  0.157105
```
