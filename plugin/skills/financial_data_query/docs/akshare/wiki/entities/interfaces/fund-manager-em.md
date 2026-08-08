---
title: "fund_manager_em - 基金经理"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_manager_em

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金经理
- 描述: 天天基金网-基金数据-基金经理大全
- 目标地址: https://fund.eastmoney.com/manager/default.html
- 限量: 单次返回所有基金经理数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

### 基金经理

接口: fund_manager_em

目标地址: https://fund.eastmoney.com/manager/default.html

描述: 天天基金网-基金数据-基金经理大全

限量: 单次返回所有基金经理数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称        | 类型      | 描述       |
|-----------|---------|----------|
| 序号        | int64   | -        |
| 姓名        | object  | -        |
| 所属公司      | object  | -        |
| 现任基金代码    | object  | -        |
| 现任基金      | object  | -        |
| 累计从业时间    | int64   | 注意单位: 天  |
| 现任基金资产总规模 | float64 | 注意单位: 亿元 |
| 现任基金最佳回报  | float64 | 注意单位: %  |

接口示例

```python
import akshare as ak

fund_manager_em_df = ak.fund_manager_em()
print(fund_manager_em_df)
```

数据示例

```
       序号   姓名    所属公司  ...累计从业时间 现任基金资产总规模 现任基金最佳回报
0         1  艾邦妮    华夏基金  ...   1110      3.13     24.96
1         1  艾邦妮    华夏基金  ...   1110      3.13     24.96
2         1  艾邦妮    华夏基金  ...   1110      3.13     24.96
3         2   艾翀  中信建投基金  ...    983      3.87     91.87
4         2   艾翀  中信建投基金  ...    983      3.87     91.87
...     ...  ...     ...  ...    ...       ...       ...
32078  4080  祝祯哲    富国基金  ...    895     23.77     12.14
32079  4081  周宗舟  汇丰晋信基金  ...    855      3.40     49.61
32080  4081  周宗舟  汇丰晋信基金  ...    855      3.40     49.61
32081  4081  周宗舟  汇丰晋信基金  ...    855      3.40     49.61
32082  4081  周宗舟  汇丰晋信基金  ...    855      3.40     49.61
[32083 rows x 8 columns]
```
