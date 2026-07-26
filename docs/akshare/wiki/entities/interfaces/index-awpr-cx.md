---
title: "index_awpr_cx - 新经济入职工资溢价水平"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# index_awpr_cx

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 财新指数 > 新经济入职工资溢价水平
- 描述: 财新指数-新经济入职工资溢价水平
- 目标地址: https://yun.ccxe.com.cn/indices/nei
- 限量: 该接口返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 新经济入职工资溢价水平

接口: index_awpr_cx

目标地址: https://yun.ccxe.com.cn/indices/nei

描述: 财新指数-新经济入职工资溢价水平

限量: 该接口返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称          | 类型      | 描述  |
|-------------|---------|-----|
| 日期          | object  | -   |
| 新经济入职工资溢价水平 | float64 | -   |
| 变化值         | float64 | -   |

接口示例

```python
import akshare as ak

index_awpr_cx_df = ak.index_awpr_cx()
print(index_awpr_cx_df)
```

数据示例

```
      日期  新经济入职工资溢价水平  变化值
0   2015-07-31   106.858500  0.000000
1   2015-08-31   109.196100  2.337600
2   2015-09-30   108.008300 -1.187800
3   2015-10-31   106.994600 -1.013700
4   2015-11-30   104.243100 -2.751500
..         ...          ...       ...
73  2021-08-31   102.576555 -0.202858
74  2021-09-30   102.680842  0.104288
75  2021-10-31   103.914771  1.233928
76  2021-11-30   102.056202 -1.858569
77  2021-12-31   104.185324  2.129122
```
