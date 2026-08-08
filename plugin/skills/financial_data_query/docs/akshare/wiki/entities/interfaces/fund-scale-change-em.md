---
title: "fund_scale_change_em - 规模变动"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_scale_change_em

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 规模份额 > 规模变动
- 描述: 天天基金网-基金数据-规模份额-规模变动
- 目标地址: https://fund.eastmoney.com/data/gmbdlist.html
- 限量: 返回所有规模变动数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 规模变动

接口: fund_scale_change_em

目标地址: https://fund.eastmoney.com/data/gmbdlist.html

描述: 天天基金网-基金数据-规模份额-规模变动

限量: 返回所有规模变动数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称    | 类型      | 描述       |
|-------|---------|----------|
| 序号    | int64   | -        |
| 截止日期  | object  | -        |
| 基金家数  | int64   | -        |
| 期间申购  | float64 | 注意单位: 亿份 |
| 期间赎回  | float64 | 注意单位: 亿份 |
| 期末总份额 | float64 | 注意单位: 亿份 |
| 期末净资产 | float64 | 注意单位: 亿份 |

接口示例

```python
import akshare as ak

fund_scale_change_em_df = ak.fund_scale_change_em()
print(fund_scale_change_em_df)
```

数据示例

```
      序号  截止日期   基金家数  期间申购  期间赎回      期末总份额   期末净资产
0      1  2023-09-30  18788  358045.47  360752.19  264069.33  273412.57
1      2  2023-06-30  18132  340624.75  330338.84  264410.61  275641.99
2      3  2023-03-31  17531  325891.23  324651.27  251161.43  264545.81
3      4  2022-12-31  16880  307176.62  317969.28  246613.07  258026.93
4      5  2022-09-30  16180  313441.70  310953.24  253704.92  264088.21
..   ...         ...    ...        ...        ...        ...        ...
97    98  1999-06-30     12        NaN        NaN     260.00     360.04
98    99  1999-03-31      6        NaN        NaN     120.00     128.21
99   100  1998-12-31      5        NaN        NaN     100.00     107.42
100  101  1998-09-30      5        NaN        NaN     100.00     101.79
101  102  1998-06-30      4        NaN        NaN      80.00      82.72
[102 rows x 7 columns]
```
