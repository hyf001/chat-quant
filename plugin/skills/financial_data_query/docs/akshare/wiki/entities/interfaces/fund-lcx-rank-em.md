---
title: "fund_lcx_rank_em - 理财基金排行"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_lcx_rank_em

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金排行 > 理财基金排行
- 描述: 东方财富网-数据中心-理财基金排行, 每个交易日17点后更新, 货币基金的单位净值均为 1.0000 元，最新一年期定存利率: 1.50%
- 目标地址: https://fund.eastmoney.com/data/lcxfundranking.html#t;c0;r;sSYL_Z;ddesc;pn50;f;os1;
- 限量: 由于目标网站没有数据，该接口暂时未能返回数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 理财基金排行

接口: fund_lcx_rank_em

目标地址: https://fund.eastmoney.com/data/lcxfundranking.html#t;c0;r;sSYL_Z;ddesc;pn50;f;os1;

描述: 东方财富网-数据中心-理财基金排行, 每个交易日17点后更新, 货币基金的单位净值均为 1.0000 元，最新一年期定存利率: 1.50%

限量: 由于目标网站没有数据，该接口暂时未能返回数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称       | 类型      | 描述      |
|----------|---------|---------|
| 序号       | int64   | -       |
| 基金代码     | object  | -       |
| 基金简称     | object  | -       |
| 日期       | object  | -       |
| 万份收益     | float64 | -       |
| 年化收益率7日  | float64 | 注意单位: % |
| 年化收益率14日 | float64 | 注意单位: % |
| 年化收益率28日 | float64 | 注意单位: % |
| 近1周      | float64 | 注意单位: % |
| 近1月      | float64 | 注意单位: % |
| 近3月      | float64 | 注意单位: % |
| 近6月      | float64 | 注意单位: % |
| 今年来      | float64 | 注意单位: % |
| 成立来      | float64 | 注意单位: % |
| 可购买      | float64 | 可购买     |
| 手续费      | object  | -       |

接口示例

```python
import akshare as ak

fund_lcx_rank_em_df = ak.fund_lcx_rank_em()
print(fund_lcx_rank_em_df)
```

数据示例

```
   序号    基金代码     基金简称          日期    万份收益  ...   近6月   今年来      成立来 可购买    手续费
0   1  531014  建信双周理财B  2021-01-17   0.783  ...  1.12  0.14  36.6531   1  0.00%
1   2  530014  建信双周理财A  2021-01-17  0.7035  ...  0.98  0.12   33.374   1  0.00%
```
