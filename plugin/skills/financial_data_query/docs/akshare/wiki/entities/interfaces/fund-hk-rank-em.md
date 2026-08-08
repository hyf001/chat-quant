---
title: "fund_hk_rank_em - 香港基金排行"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_hk_rank_em

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金排行 > 香港基金排行
- 描述: 东方财富网-数据中心-基金排行-香港基金排行
- 目标地址: https://overseas.1234567.com.cn/FundList
- 限量: 单次返回当前时刻所有数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 香港基金排行

接口: fund_hk_rank_em

目标地址: https://overseas.1234567.com.cn/FundList

描述: 东方财富网-数据中心-基金排行-香港基金排行

限量: 单次返回当前时刻所有数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称     | 类型      | 描述                       |
|--------|---------|--------------------------|
| 序号     | int64   | -                        |
| 基金代码   | object  | -                        |
| 基金简称   | object  | -                        |
| 币种     | object  | -                        |
| 日期     | object  | -                        |
| 单位净值   | float64 | -                        |
| 日增长率   | float64 | 注意单位: %                  |
| 近1周    | float64 | 注意单位: %                  |
| 近1月    | float64 | 注意单位: %                  |
| 近3月    | float64 | 注意单位: %                  |
| 近6月    | float64 | 注意单位: %                  |
| 近1年    | float64 | 注意单位: %                  |
| 近2年    | float64 | 注意单位: %                  |
| 近3年    | float64 | 注意单位: %                  |
| 今年来    | float64 | 注意单位: %                  |
| 成立来    | float64 | 注意单位: %                  |
| 可购买    | object  | -                        |
| 香港基金代码 | object  | 用于查询历史净值数据, 通过该字段查询相关的数据 |

接口示例

```python
import akshare as ak

fund_hk_rank_em_df = ak.fund_hk_rank_em()
print(fund_hk_rank_em_df)
```

数据示例

```
      序号    基金代码                       基金简称  ...      成立来   可购买      香港基金代码
0      1  968077             东方汇理创新动力股票基金分派  ...   2.5000  不可购买  1002185388
1      2  968062                 摩根太平洋科技人民币  ...  20.7000   可购买  1002075743
2      3  968063                  摩根太平洋科技美元  ...  16.9000  不可购买  1002075744
3      4  968075                百达策略收益累积CNY  ...  19.6950   可购买  1002185380
4      5  968061               摩根太平洋科技人民币对冲  ...  16.9000   可购买  1002075741
..   ...     ...                        ...  ...      ...   ...         ...
107  108  968031              中银香港全天候香港股票基金  ... -46.5613  不可购买  1001402919
108  109  968006                     行健宏扬中国  ... -17.9400   可购买  1000595430
109  110  968058  博时-安本标准精选新兴市场债券基金PRC类别A美元  ...      NaN  不可购买  1002059492
110  111  968060  博时-安本标准精选新兴市场债券基金PRC类别I美元  ...      NaN  不可购买  1002059495
111  112  968153                 南方东英精选美元债券  ...   1.6000  不可购买  1003656354
[112 rows x 18 columns]
```
