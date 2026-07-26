---
title: "fund_rating_sh - 上海证券评级"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_rating_sh

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金评级 > 上海证券评级
- 描述: 天天基金网-基金评级-上海证券评级
- 目标地址: https://fund.eastmoney.com/data/fundrating_3.html
- 限量: 单次返回指定交易日的所有基金评级数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 上海证券评级

接口: fund_rating_sh

目标地址: https://fund.eastmoney.com/data/fundrating_3.html

描述: 天天基金网-基金评级-上海证券评级

限量: 单次返回指定交易日的所有基金评级数据

输入参数

| 名称   | 类型  | 描述                                                                        |
|------|-----|---------------------------------------------------------------------------|
| date | str | date='20230630'; https://fund.eastmoney.com/data/fundrating_3.html 获取查询日期 |

输出参数

| 名称         | 类型      | 描述      |
|------------|---------|---------|
| 代码         | object  | -       |
| 简称         | object  | -       |
| 基金经理       | object  | -       |
| 基金公司       | object  | -       |
| 3年期评级-3年评级 | int64   | -       |
| 3年期评级-较上期  | float64 | -       |
| 5年期评级-5年评级 | float64 | -       |
| 5年期评级-较上期  | float64 | -       |
| 单位净值       | float64 | -       |
| 日期         | object  | -       |
| 日增长率       | float64 | 注意单位: % |
| 近1年涨幅      | float64 | 注意单位: % |
| 近3年涨幅      | float64 | 注意单位: % |
| 近5年涨幅      | float64 | 注意单位: % |
| 手续费        | object  | -       |
| 类型         | object  | -       |

接口示例

```python
import akshare as ak

fund_rating_sh_df = ak.fund_rating_sh(date='20230630')
print(fund_rating_sh_df)
```

数据示例

```
      代码           简称     基金经理    基金公司  ...  近3年涨幅  近5年涨幅    手续费  类型
0     000004     中海可转债债券C       章俊    中海基金  ...  -8.00  24.14  0.00%
1     000003     中海可转债债券A       章俊    中海基金  ...  -6.77  25.94  0.08%
2     000014      华夏聚利债券A      何家琪    华夏基金  ...  27.31  61.22  0.06%
3     000015      华夏纯债债券A      柳万军    华夏基金  ...  10.16  22.21  0.08%
4     000046     工银产业债债券B      何秀红  工银瑞信基金  ...   8.79  26.21  0.00%
      ...          ...      ...     ...  ...    ...    ...    ...  ..
4632  540009   汇丰晋信消费红利股票  范坤祥,费馨涵  汇丰晋信基金  ...  -5.45  39.22  0.15%
4633  540010   汇丰晋信科技先锋股票       陈平  汇丰晋信基金  ... -30.95  31.16  0.15%
4634  960000    汇丰晋信大盘股票H      闵良超  汇丰晋信基金  ...    NaN    NaN
4635  671030   西部利得事件驱动股票      张昌平  西部利得基金  ...  35.24    NaN  0.15%
4636  673090  西部利得个股精选股票A      童国林  西部利得基金  ...   3.18  50.24  0.12%
[4637 rows x 16 columns]
```
