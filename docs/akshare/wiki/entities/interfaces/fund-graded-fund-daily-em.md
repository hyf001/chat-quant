---
title: "fund_graded_fund_daily_em - 分级基金-实时数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_graded_fund_daily_em

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金净值 > 分级基金-实时数据
- 描述: 东方财富网-天天基金网-基金数据-分级基金-实时数据, 此接口数据每个交易日 **16:00～23:00**
- 目标地址: http://fund.eastmoney.com/fjjj.html#1_1__0__zdf,desc_1
- 限量: 单次返回当前时刻所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 分级基金-实时数据

接口: fund_graded_fund_daily_em

目标地址: http://fund.eastmoney.com/fjjj.html#1_1__0__zdf,desc_1

描述: 东方财富网-天天基金网-基金数据-分级基金-实时数据, 此接口数据每个交易日 **16:00～23:00**

限量: 单次返回当前时刻所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称        | 类型    | 描述      |
|-----------|-------|---------|
| 基金代码      | str   | -       |
| 基金简称      | str   | -       |
| 单位净值      | float | -       |
| 累计净值      | float | -       |
| 前交易日-单位净值 | float | -       |
| 前交易日-累计净值 | float | -       |
| 日增长值      | float | -       |
| 日增长率      | float | 注意单位: % |
| 市价        | str   | -       |
| 折价率       | str   | -       |
| 手续费       | str   | -       |

接口示例

```python
import akshare as ak

fund_graded_fund_daily_em_df = ak.fund_graded_fund_daily_em()
print(fund_graded_fund_daily_em_df)
```

数据示例

```
       基金代码            基金简称    单位净值    累计净值  ...   日增长率      市价     折价率    手续费
0    150232     申万菱信申万电子分级B  0.5598          ...  15.85  0.9080  -62.20
1    150174  信诚中证TMT产业主题分级B  0.6580  2.0740  ...  10.77    0.76  -15.50
2    150312   信诚中证智能家居指数分级B  0.7430  0.0960  ...  10.73  0.7570   -1.88
3    150310   信诚中证信息安全指数分级B  0.9090  0.1040  ...   9.92  1.0790  -18.70
4    150151  信诚中证800有色指数分级B    0.63  1.1180  ...   6.42  0.7110  -12.86
..      ...             ...     ...     ...  ...    ...     ...     ...    ...
341  150252   招商中证煤炭等权指数分级B                  ...         0.5120
342  150324   工银中证环保产业指数分级B                  ...           0.74
343  150197   国泰国证有色金属行业分级B                  ...           0.44
344  150294   南方中证高铁产业指数分级B                  ...         0.4350
345  161825       银华中证800分级                  ...                         1.20%
```
