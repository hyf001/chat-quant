---
title: "fund_aum_trend_em - 基金规模走势"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_aum_trend_em

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金公司规模 > 基金规模走势
- 描述: 天天基金网-基金数据-市场全部基金规模走势
- 目标地址: http://fund.eastmoney.com/Company/default.html
- 限量: 单次返回所有市场全部基金规模走势数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 基金规模走势

接口: fund_aum_trend_em

目标地址: http://fund.eastmoney.com/Company/default.html

描述: 天天基金网-基金数据-市场全部基金规模走势

限量: 单次返回所有市场全部基金规模走势数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称    | 类型      | 描述  |
|-------|---------|-----|
| date  | object  | -   |
| value | float64 | -   |

接口示例

```python
import akshare as ak

fund_aum_trend_em_df = ak.fund_aum_trend_em()
print(fund_aum_trend_em_df)
```

数据示例

```
          date         value
0   2016-06-30  7.795280e+12
1   2016-09-30  8.572922e+12
2   2016-12-31  8.966215e+12
3   2017-03-31  8.964740e+12
4   2017-06-30  9.887788e+12
5   2017-09-30  1.085338e+13
6   2017-12-31  1.141607e+13
7   2018-03-31  1.205598e+13
8   2018-06-30  1.256286e+13
9   2018-09-30  1.307637e+13
10  2018-12-31  1.285114e+13
11  2019-03-31  1.349216e+13
12  2019-06-30  1.321250e+13
13  2019-09-30  1.332581e+13
14  2019-12-31  1.463123e+13
15  2020-03-31  1.624671e+13
16  2020-06-30  1.649092e+13
17  2020-09-30  1.717224e+13
18  2020-12-31  1.953767e+13
19  2021-03-31  2.116346e+13
20  2021-06-28  2.233053e+13
```
