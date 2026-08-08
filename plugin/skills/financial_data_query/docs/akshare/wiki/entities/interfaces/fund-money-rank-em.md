---
title: "fund_money_rank_em - 货币型基金排行"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_money_rank_em

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金排行 > 货币型基金排行
- 描述: 东方财富网-数据中心-货币型基金排行
- 目标地址: https://fund.eastmoney.com/data/hbxfundranking.html
- 限量: 单次返回当前时刻所有数据, 每个交易日 17 点后更新, 货币基金的单位净值均为 1.0000 元，最新一年期定存利率: 1.50%
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 货币型基金排行

接口: fund_money_rank_em

目标地址: https://fund.eastmoney.com/data/hbxfundranking.html

描述: 东方财富网-数据中心-货币型基金排行

限量: 单次返回当前时刻所有数据, 每个交易日 17 点后更新, 货币基金的单位净值均为 1.0000 元，最新一年期定存利率: 1.50%

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
| 万份收益     | float64 | 注意单位: % |
| 年化收益率7日  | float64 | 注意单位: % |
| 年化收益率14日 | float64 | 注意单位: % |
| 年化收益率28日 | float64 | 注意单位: % |
| 近1月      | float64 | 注意单位: % |
| 近3月      | float64 | 注意单位: % |
| 近6月      | float64 | 注意单位: % |
| 近1年      | float64 | 注意单位: % |
| 近2年      | float64 | 注意单位: % |
| 近3年      | float64 | 注意单位: % |
| 近5年      | float64 | 注意单位: % |
| 今年来      | float64 | 注意单位: % |
| 成立来      | float64 | 注意单位: % |
| 手续费      | object  | -       |

接口示例

```python
import akshare as ak

fund_money_rank_em_df = ak.fund_money_rank_em()
print(fund_money_rank_em_df)
```

数据示例

```
      序号  基金代码   基金简称          日期  ...    近5年   今年来    成立来    手续费
0      1  004121    兴银现金添利A  2024-02-28  ...   9.83  0.39  18.94  0.00%
1      2  002234  泰信天天收益货币B  2024-02-28  ...  11.96  0.39  22.74  0.00%
2      3  740602      长安货币B  2024-02-28  ...  11.56  0.37  40.86  0.00%
3      4  015972   中航航行宝货币B  2024-02-28  ...    NaN  0.39   3.78  0.00%
4      5  001821   兴全天添益货币B  2024-02-28  ...  13.18  0.39  27.46  0.00%
..   ...     ...        ...         ...  ...    ...   ...    ...    ...
539  540  019040      国联日盈C  2024-02-28  ...    NaN  0.44   1.29  0.00%
540  541  019145      长盛货币E  2024-02-28  ...    NaN  0.37   1.14  0.00%
541  542  019769  华商现金增利货币E  2024-02-28  ...    NaN  0.34   0.74  0.00%
542  543  019967    工银如意货币C  2024-02-28  ...    NaN  0.38   0.72  0.00%
543  544  020097      中加货币E  2024-02-28  ...    NaN  0.35   0.52  0.00%
[544 rows x 18 columns]
```
