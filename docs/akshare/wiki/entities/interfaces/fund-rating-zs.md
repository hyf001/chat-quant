---
title: "fund_rating_zs - 招商证券评级"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_rating_zs

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金评级 > 招商证券评级
- 描述: 天天基金网-基金评级-招商证券评级
- 目标地址: http://fund.eastmoney.com/data/fundrating_2.html
- 限量: 单次返回指定交易日的所有基金评级数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 招商证券评级

接口: fund_rating_zs

目标地址: http://fund.eastmoney.com/data/fundrating_2.html

描述: 天天基金网-基金评级-招商证券评级

限量: 单次返回指定交易日的所有基金评级数据

输入参数

| 名称   | 类型  | 描述                                                                        |
|------|-----|---------------------------------------------------------------------------|
| date | str | date='20230331'; https://fund.eastmoney.com/data/fundrating_2.html 获取查询日期 |

输出参数

| 名称         | 类型      | 描述      |
|------------|---------|---------|
| 代码         | object  | -       |
| 简称         | object  | -       |
| 基金经理       | object  | -       |
| 基金公司       | object  | -       |
| 3年期评级-3年评级 | int64   | -       |
| 3年期评级-较上期  | float64 | -       |
| 单位净值       | float64 | -       |
| 日期         | object  | -       |
| 日增长率       | float64 | 注意单位: % |
| 近1年涨幅      | float64 | 注意单位: % |
| 近3年涨幅      | float64 | 注意单位: % |
| 近5年涨幅      | float64 | 注意单位: % |
| 手续费        | object  | -       |

接口示例

```python
import akshare as ak

fund_rating_zs_df = ak.fund_rating_zs(date='20230331')
print(fund_rating_zs_df)
```

数据示例

```
      代码               简称     基金经理  基金公司  ...  近1年涨幅  近3年涨幅   近5年涨幅    手续费
0     005161        华商上游产业股票A       童立  华商基金  ...  -1.82  84.44  153.39  0.15%
1     005660        嘉实资源精选股票A      苏文杰  嘉实基金  ...  -3.08  76.04     NaN  0.15%
2     007130         中庚小盘价值股票      丘栋荣  中庚基金  ...   4.65  94.52     NaN  1.50%
3     320020         诺安策略精选股票       李迪  诺安基金  ...   1.63  44.76  102.39  0.15%
4     007538         永赢沪深300A       万纯  永赢基金  ...  -9.77   4.63     NaN  0.10%
      ...              ...      ...   ...  ...    ...    ...     ...    ...
3319  162714  广发深证100指数(LOF)A      陆志明  广发基金  ... -17.19 -10.96   30.65  0.12%
3320  070009         嘉实超短债债券C      李金灿  嘉实基金  ...   2.12   6.91   13.97  0.00%
3321  000227         华安年年红债券A      石雨欣  华安基金  ...   1.45   6.83   27.18  0.06%
3322  002864        广发安泽短债债券A      刘志辉  广发基金  ...   2.70   8.07   16.11  0.04%
3323  000239        华安年年盈定开债A  朱才敏,魏媛媛  华安基金  ...   0.50   8.18   32.63  0.06%
[3324 rows x 13 columns]
```
