---
title: "fund_etf_scale_szse - ETF 基金份额-深交所"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_etf_scale_szse

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金规模 > ETF 基金份额-深交所
- 描述: 深圳证券交易所-基金产品-基金列表-ETF基金份额
- 目标地址: https://fund.szse.cn/marketdata/fundslist/index.html
- 限量: 单次返回最近交易日的 ETF 基金份额数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

#### ETF 基金份额-深交所

接口: fund_etf_scale_szse

目标地址: https://fund.szse.cn/marketdata/fundslist/index.html

描述: 深圳证券交易所-基金产品-基金列表-ETF基金份额

限量: 单次返回最近交易日的 ETF 基金份额数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称    | 类型      | 描述 |
|-------|---------|----|
| 基金代码  | object  | -  |
| 基金简称  | object  | -  |
| 基金类别  | object  | -  |
| 投资类别  | object  | -  |
| 上市日期  | object  | -  |
| 基金份额  | float64 | -  |
| 基金管理人 | object  | -  |
| 基金发起人 | float64 | -  |
| 基金托管人 | float64 | -  |
| 净值    | float64 | -  |

接口示例

```python
import akshare as ak

fund_etf_scale_szse_df = ak.fund_etf_scale_szse()
print(fund_etf_scale_szse_df)
```

数据示例

```
     基金代码        基金简称   基金类别  ... 基金发起人 基金托管人  净值
0    159001        货币ETF易方达    ETF  ...   NaN   NaN  100.0000
1    159003         招商快线ETF    ETF  ...   NaN   NaN  100.0000
2    159005        汇添富快钱ETF    ETF  ...   NaN   NaN  100.0000
3    159100           巴西ETF    ETF  ...   NaN   NaN    1.0223
4    159101      港股通科技ETF基金    ETF  ...   NaN   NaN    0.9906
..      ...             ...    ...  ...   ...   ...       ...
898  180606    中金中国绿发商业REIT  不动产基金  ...   NaN   NaN       NaN
899  180607      华夏中海商业REIT  不动产基金  ...   NaN   NaN       NaN
900  180701    银华绍兴原水水利REIT  不动产基金  ...   NaN   NaN       NaN
901  180801      中航首钢绿能REIT  不动产基金  ...   NaN   NaN       NaN
902  180901  南方润泽科技数据中心REIT  不动产基金  ...   NaN   NaN       NaN
[903 rows x 10 columns]
```
