---
title: "qdii_a_index_jsl - 亚洲指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qdii, parameters, returns, example]
sources: [raw/data-dictionary/qdii/qdii.md]
confidence: high
---
# qdii_a_index_jsl

- 分类: [[qdii-qdii|AKShare QDII 数据]]
- 主题路径: AKShare QDII 数据 > T+0 QDII 亚洲市场 > 亚洲指数
- 描述: 集思录-T+0 QDII-亚洲市场-亚洲指数
- 目标地址: https://www.jisilu.cn/data/qdii/#qdiia
- 限量: 单次返回所有数据
- 来源页面: https://akshare.akfamily.xyz/data/qdii/qdii.html

## 相关

- [[qdii-qdii|AKShare QDII 数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 亚洲指数

接口: qdii_a_index_jsl

目标地址: https://www.jisilu.cn/data/qdii/#qdiia

描述: 集思录-T+0 QDII-亚洲市场-亚洲指数

限量: 单次返回所有数据

输入参数

| 名称     | 类型  | 描述                |
|--------|-----|-------------------|
| cookie | str | 需要传入用户登录后的 cookie |

输出参数

| 名称   | 类型      | 描述       |
|------|---------|----------|
| 代码   | object  |          |
| 名称   | object  |          |
| 现价   | float64 |          |
| 涨幅   | object  |          |
| 成交   | float64 | 注意单位: 万元 |
| 场内份额 | int64   | 注意单位: 万份 |
| 场内新增 | int64   | 注意单位: 万份 |
| 净值   | float64 |          |
| 净值日期 | object  |          |
| 估值   | float64 |          |
| 溢价率  | object  |          |
| 相关标的 | object  |          |
| 指数涨幅 | object  |          |
| 申购费  | object  |          |
| 赎回费  | object  |          |
| 托管费  | float64 |          |
| 基金公司 | object  |          |

接口示例

```python
import akshare as ak

qdii_a_index_jsl_df = ak.qdii_a_index_jsl()
print(qdii_a_index_jsl_df)
```

数据示例

```
      代码          名称    现价   涨幅  ...    申购费    赎回费   托管费  基金公司
0    164705       恒生LOF  1.089  10.00%  ...  1.20%  1.50%  1.05   汇添富
1    513230     港股消费ETF  0.970   9.98%  ...   0.5%   0.5%  0.60  华夏基金
2    513990      港股通ETF  1.001  10.00%  ...      -      -  0.25  招商基金
3    159850     恒生国企ETF  0.791  10.01%  ...  0.50%  0.50%  0.65  华夏基金
4    159567    港股创新药ETF  1.111  10.00%  ...      -      -  0.60  银华基金
..      ...         ...    ...     ...  ...    ...    ...   ...   ...
104  520890  港股通红利低波ETF  1.128   5.32%  ...  0.50%  0.50%  0.60  华泰柏瑞
105  501307    银河高股息LOF  1.059   5.37%  ...  1.00%  1.50%  0.68  银河基金
106  501310     价值基金LOF  1.118   4.39%  ...  1.20%  1.50%  0.90  华宝基金
107  513090     香港证券ETF  1.279   9.97%  ...  0.50%  0.50%  0.20   易方达
108  513800   日本东证指数ETF  1.387  -0.07%  ...      -      -  0.25  南方基金
[109 rows x 17 columns]
```
