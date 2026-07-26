---
title: "reits_realtime_em - REITs-实时行情"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# reits_realtime_em

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > REITs > REITs-实时行情
- 描述: 东方财富网-行情中心-REITs-沪深 REITs-实时行情
- 目标地址: http://quote.eastmoney.com/center/gridlist.html#fund_reits_all
- 限量: 单次返回所有 REITs 的实时行情数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

#### REITs-实时行情

接口: reits_realtime_em

目标地址: http://quote.eastmoney.com/center/gridlist.html#fund_reits_all

描述: 东方财富网-行情中心-REITs-沪深 REITs-实时行情

限量: 单次返回所有 REITs 的实时行情数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称  | 类型      | 描述      |
|-----|---------|---------|
| 序号  | int64   | -       |
| 代码  | object  | -       |
| 名称  | object  | -       |
| 最新价 | float64 | -       |
| 涨跌额 | float64 | -       |
| 涨跌幅 | float64 | 注意单位: % |
| 成交量 | int64   | -       |
| 成交额 | float64 | -       |
| 开盘价 | float64 | -       |
| 最高价 | float64 | -       |
| 最低价 | float64 | -       |
| 昨收  | float64 | -       |

接口示例

```python
import akshare as ak

reits_realtime_em_df = ak.reits_realtime_em()
print(reits_realtime_em_df)
```

数据示例

```
    序号  代码               名称    最新价  ...    开盘价    最高价  最低价     昨收
0    1  508026   嘉实中国电建清洁能源REIT  4.180  ...  4.110  4.199  4.110  4.150
1    2  508009       中金安徽交控REIT  7.749  ...  7.722  7.781  7.687  7.722
2    3  180106    广发成都高投产业园REIT  4.064  ...  4.053  4.100  4.000  4.050
3    4  180401       鹏华深圳能源REIT  6.361  ...  6.348  6.379  6.344  6.344
4    5  508008       国金中国铁建REIT  9.460  ...  9.434  9.486  9.425  9.435
..  ..     ...              ...    ...  ...    ...    ...    ...    ...
58  59  180102       华夏合肥高新REIT  2.196  ...  2.218  2.245  2.172  2.245
59  60  508021  国泰君安临港创新产业园REIT  4.415  ...  4.515  4.526  4.388  4.515
60  61  508066       华泰江苏交控REIT  6.524  ...  6.650  6.730  6.521  6.679
61  62  180302        华夏深国际REIT  2.829  ...  2.888  2.988  2.822  2.928
62  63  508007       中金山东高速REIT  8.184  ...  8.432  8.432  8.180  8.472
[63 rows x 12 columns]
```
