---
title: "fund_lof_spot_em - LOF基金实时行情-东财"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_lof_spot_em

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金行情 > LOF基金实时行情-东财
- 描述: 东方财富-LOF 实时行情
- 目标地址: https://quote.eastmoney.com/center/gridlist.html#fund_lof
- 限量: 单次返回所有数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

#### LOF基金实时行情-东财

接口: fund_lof_spot_em

目标地址: https://quote.eastmoney.com/center/gridlist.html#fund_lof

描述: 东方财富-LOF 实时行情

限量: 单次返回所有数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称   | 类型      | 描述      |
|------|---------|---------|
| 代码   | object  | -       |
| 名称   | object  | -       |
| 最新价  | float64 | -       |
| 涨跌额  | float64 | -       |
| 涨跌幅  | float64 | 注意单位: % |
| 成交量  | float64 | -       |
| 成交额  | float64 | -       |
| 开盘价  | float64 | -       |
| 最高价  | float64 | -       |
| 最低价  | float64 | -       |
| 昨收   | float64 | -       |
| 换手率  | float64 | -       |
| 流通市值 | int64   | -       |
| 总市值  | int64   | -       |

接口示例

```python
import akshare as ak

fund_lof_spot_em_df = ak.fund_lof_spot_em()
print(fund_lof_spot_em_df)
```

数据示例

```
      代码       名称    最新价    涨跌额  ...     昨收  换手率  流通市值        总市值
0    166009     中欧动力LOF  3.123  0.114  ...  3.009  0.64    6716805    6716805
1    161811  沪深300LOF银华  0.859  0.029  ...  0.830  0.04    7986026    7986026
2    160807  长盛沪深300LOF  1.454  0.033  ...  1.421  0.56    3979752    3979752
3    165520       有色LOF  1.515  0.034  ...  1.481  0.30   17217774   17217774
4    161217     国投资源LOF  1.238  0.027  ...  1.211  0.07    5947481    5947481
..      ...         ...    ...    ...  ...    ...   ...        ...        ...
146  501083     科创银华LOF  1.336 -0.024  ...  1.360  0.32  124253745  124253745
147  160512     博时卓越LOF  2.465 -0.045  ...  2.510  0.00   35852612   35852612
148  160621     鹏华丰和LOF  1.421 -0.029  ...  1.450  0.41    2367956    2367956
149  160215     国泰价值LOF  2.341 -0.053  ...  2.394  0.07    7602067    7602067
150  165515    信诚300LOF  1.048 -0.054  ...  1.102  0.07   37943012   37943012
[151 rows x 14 columns]
```
