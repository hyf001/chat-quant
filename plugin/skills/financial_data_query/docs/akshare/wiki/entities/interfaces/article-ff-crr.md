---
title: "article_ff_crr - Current Research Returns"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, article, parameters, returns, example]
sources: [raw/data-dictionary/article/article.md]
confidence: high
---
# article_ff_crr

- 分类: [[article-article|AKShare 波动率数据]]
- 主题路径: AKShare 多因子数据 > Current Research Returns
- 描述: 获取 Current Research Returns 多因子数据; 更多信息请访问目标地址
- 目标地址: https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/article/article.html

## 相关

- [[article-article|AKShare 波动率数据]]
- [[_meta/topic-map]]

## 源文摘录

### Current Research Returns

接口: article_ff_crr

目标地址: https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html

描述: 获取 Current Research Returns 多因子数据; 更多信息请访问目标地址

限量: 单次返回所有历史数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称             | 类型     | 描述   |
|----------------|--------|------|
| item           | object | -    |
| September 2019 | object | 动态日期 |
| Last 3 Months  | object | 动态日期 |
| Last 12 Months | object | 动态日期 |

接口示例

```python
import akshare as ak

article_ff_crr_df = ak.article_ff_crr()
print(article_ff_crr_df)
```

数据示例

```
                                           item  ... Last 12  Months
0                Fama/French 3 Research Factors  ...               -
1                                         Rm-Rf  ...            8.12
2                                           SMB  ...           -9.44
3                                           HML  ...          -14.98
4          Fama/French 5 Research Factors (2x3)  ...               -
5                                         Rm-Rf  ...            8.12
6                                           SMB  ...          -12.25
7                                           HML  ...          -14.98
8                                           RMW  ...            8.46
9                                           CMA  ...          -14.63
10              Fama/French Research Portfolios  ...               -
11           Size and Book-to-Market Portfolios  ...               -
12                                  Small Value  ...           -7.16
13                                Small Neutral  ...            1.97
14                                  Big Neutral  ...           -2.47
15                                 Small Growth  ...           -2.56
16                                    Big Value  ...            0.51
17                                   Big Growth  ...           22.70
18  Size and Operating Profitability Portfolios  ...               -
19                                 Small Robust  ...            4.19
20                                Small Neutral  ...            0.17
21                                   Small Weak  ...           -4.93
22                                   Big Robust  ...           19.99
23                                  Big Neutral  ...            5.67
24                                     Big Weak  ...           12.20
25               Size and Investment Portfolios  ...               -
26                           Small Conservative  ...           -6.81
27                                Small Neutral  ...           -1.21
28                             Small Aggressive  ...            1.64
29                             Big Conservative  ...            0.77
30                                  Big Neutral  ...           14.75
31                               Big Aggressive  ...           21.59
[32 rows x 4 columns]
```
