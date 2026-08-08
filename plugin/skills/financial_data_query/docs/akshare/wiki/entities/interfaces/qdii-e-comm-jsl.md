---
title: "qdii_e_comm_jsl - 欧美商品"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qdii, parameters, returns, example]
sources: [raw/data-dictionary/qdii/qdii.md]
confidence: high
---
# qdii_e_comm_jsl

- 分类: [[qdii-qdii|AKShare QDII 数据]]
- 主题路径: AKShare QDII 数据 > T+0 QDII 欧美市场 > 欧美商品
- 描述: 集思录-T+0 QDII-欧美市场-欧美商品
- 目标地址: https://www.jisilu.cn/data/qdii/#qdiia
- 限量: 单次返回所有数据
- 来源页面: https://akshare.akfamily.xyz/data/qdii/qdii.html

## 相关

- [[qdii-qdii|AKShare QDII 数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 欧美商品

接口: qdii_e_comm_jsl

目标地址: https://www.jisilu.cn/data/qdii/#qdiia

描述: 集思录-T+0 QDII-欧美市场-欧美商品

限量: 单次返回所有数据

输入参数

| 名称     | 类型  | 描述                |
|--------|-----|-------------------|
| cookie | str | 需要传入用户登录后的 cookie |

输出参数

| 名称      | 类型      | 描述       |
|---------|---------|----------|
| 代码      | object  |          |
| 名称      | object  |          |
| 现价      | float64 |          |
| 涨幅      | object  |          |
| 成交      | float64 | 注意单位: 万元 |
| 场内份额    | int64   | 注意单位: 万份 |
| 场内新增    | int64   | 注意单位: 万份 |
| T-2净值   | float64 |          |
| 净值日期    | object  |          |
| T-1估值   | float64 |          |
| 估值日期    | object  |          |
| T-1溢价率  | object  |          |
| 相关标的    | object  |          |
| T-1指数涨幅 | object  |          |
| 申购费     | object  |          |
| 赎回费     | object  |          |
| 托管费     | float64 |          |
| 基金公司    | object  |          |

接口示例

```python
import akshare as ak

qdii_e_comm_jsl_df = ak.qdii_e_comm_jsl()
print(qdii_e_comm_jsl_df)
```

数据示例

```
    代码         名称     现价      涨幅  ...    申购费  赎回费  托管费 基金公司
0   161129   原油LOF易方达  1.341   2.60%  ...  1.20%  1.50%  1.25   易方达
1   161116    黄金主题LOF  1.082  -0.46%  ...      0  1.50%  1.40   易方达
2   501018    南方原油LOF  1.194   2.58%  ...  1.20%  1.50%  1.28  南方基金
3   160723    嘉实原油LOF  1.387   2.06%  ...  1.20%  1.50%  1.28  嘉实基金
4   161815     抗通胀LOF  0.753   0.40%  ...  1.60%  1.50%  2.15  银华基金
5   164701      黄金LOF  1.111  -0.45%  ...  0.80%  1.50%  1.26   汇添富
6   160216    国泰商品LOF  0.513   0.20%  ...  1.50%  1.50%  1.85  国泰基金
7   160416    石油基金LOF  1.615   0.56%  ...  0.00%  1.50%  1.28  华安基金
8   163208  全球油气能源LOF  0.983   2.93%  ...  1.50%  1.50%  1.85  诺安基金
9   165513  中信保诚商品LOF  0.704  -0.14%  ...  1.60%  1.50%  2.05  信诚基金
10  162719      石油LOF  2.222   2.44%  ...  1.20%  1.50%  1.30  广发基金
11  160719    嘉实黄金LOF  1.285  -0.16%  ...  0.80%  1.50%  1.26  嘉实基金
12  162411    华宝油气LOF  0.719   3.01%  ...  1.50%  1.50%  1.28  华宝基金
[13 rows x 18 columns]
```
