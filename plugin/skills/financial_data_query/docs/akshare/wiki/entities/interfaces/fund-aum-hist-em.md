---
title: "fund_aum_hist_em - 基金公司历年管理规模"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_aum_hist_em

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金公司规模 > 基金公司历年管理规模
- 描述: 天天基金网-基金数据-基金公司历年管理规模排行列表
- 目标地址: http://fund.eastmoney.com/Company/lsgm.html
- 限量: 单次返回所有基金公司历年管理规模排行列表数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 基金公司历年管理规模

接口: fund_aum_hist_em

目标地址: http://fund.eastmoney.com/Company/lsgm.html

描述: 天天基金网-基金数据-基金公司历年管理规模排行列表

限量: 单次返回所有基金公司历年管理规模排行列表数据

输入参数

| 名称   | 类型  | 描述                      |
|------|-----|-------------------------|
| year | str | year="2023"; 从 2001 年开始 |

输出参数

| 名称   | 类型      | 描述  |
|------|---------|-----|
| 序号   | int64   | -   |
| 基金公司 | object  | -   |
| 总规模  | float64 | -   |
| 股票型  | float64 | -   |
| 混合型  | float64 | -   |
| 债券型  | float64 | -   |
| 指数型  | float64 | -   |
| QDII | float64 | -   |
| 货币型  | float64 | -   |

接口示例

```python
import akshare as ak

fund_aum_hist_em_df = ak.fund_aum_hist_em(year="2023")
print(fund_aum_hist_em_df)
```

数据示例

```
      序号       基金公司       总规模      股票型  ...    债券型    指数型    QDII      货币型
0      1   易方达基金管理有限公司  16514.20  2704.67  ...  3221.98  2343.89  763.82  6802.29
1      2    广发基金管理有限公司  12633.03  1124.83  ...  2749.18  1179.12  394.54  6046.73
2      3    华夏基金管理有限公司  12238.81  3551.49  ...  1924.34  3430.87  785.84  4458.91
3      4  南方基金管理股份有限公司  10853.73  1266.44  ...  2198.48  1453.78   83.07  5791.66
4      5    天弘基金管理有限公司  10479.03   817.96  ...  1908.11   862.39  153.29  7405.90
..   ...           ...       ...      ...  ...      ...      ...     ...      ...
194  195    瑞达基金管理有限公司      1.05      NaN  ...      NaN      NaN     NaN      NaN
195  196    华创证券有限责任公司      1.03      NaN  ...     1.03      NaN     NaN      NaN
196  197  明亚基金管理有限责任公司      1.00     0.47  ...      NaN     0.47     NaN      NaN
197  198    华鑫证券有限责任公司      0.72      NaN  ...     0.72      NaN     NaN      NaN
198  199    国都证券股份有限公司      0.41      NaN  ...      NaN      NaN     NaN      NaN
[199 rows x 9 columns]
```
