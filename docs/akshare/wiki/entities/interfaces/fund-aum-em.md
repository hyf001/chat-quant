---
title: "fund_aum_em - 基金规模详情"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_aum_em

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金公司规模 > 基金规模详情
- 描述: 天天基金网-基金数据-基金规模
- 目标地址: https://fund.eastmoney.com/Company/lsgm.html
- 限量: 单次返回所有基金规模数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 基金规模详情

接口: fund_aum_em

目标地址: https://fund.eastmoney.com/Company/lsgm.html

描述: 天天基金网-基金数据-基金规模

限量: 单次返回所有基金规模数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称     | 类型      | 描述       |
|--------|---------|----------|
| 序号     | int64   | -        |
| 基金公司   | object  | -        |
| 成立时间   | object  | -        |
| 全部管理规模 | float64 | 注意单位: 亿元 |
| 全部基金数  | int64   | -        |
| 全部经理数  | int64   | -        |
| 更新日期   | object  | -        |

接口示例

```python
import akshare as ak

fund_aum_em_df = ak.fund_aum_em()
print(fund_aum_em_df)
```

数据示例

```
      序号          基金公司        成立时间    全部管理规模  全部基金数  全部经理数   更新日期
0      1   易方达基金管理有限公司  2001-04-17  16599.27    632     81  11-08
1      2    广发基金管理有限公司  2003-08-05  12701.86    660     82  11-10
2      3    华夏基金管理有限公司  1998-04-09  12379.85    709    113  11-10
3      4  南方基金管理股份有限公司  1998-03-06  10966.40    607     84  10-24
4      5    天弘基金管理有限公司  2004-11-08  10486.77    334     46  11-01
..   ...           ...         ...       ...    ...    ...    ...
200  201    国都证券股份有限公司  2001-12-28      0.41      2      2  09-30
201  202    天风证券股份有限公司  2000-03-29       NaN      0      0  12-31
202  203    国新证券股份有限公司  2007-09-07       NaN      0      0  03-31
203  204    安信证券股份有限公司  2006-08-22       NaN      0      0  03-31
204  205    东兴证券股份有限公司  2008-05-28       NaN      0      0  03-31
[205 rows x 7 columns]
```
