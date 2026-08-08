---
title: "fund_hk_fund_hist_em - 香港基金-历史数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_hk_fund_hist_em

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金净值 > 香港基金-历史数据
- 描述: 东方财富网站-天天基金网-基金数据-香港基金-历史净值明细
- 目标地址: http://overseas.1234567.com.cn/f10/FundJz/968092#FHPS
- 限量: 单次返回指定 code 和 symbol 所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 香港基金-历史数据

接口: fund_hk_fund_hist_em

目标地址: http://overseas.1234567.com.cn/f10/FundJz/968092#FHPS

描述: 东方财富网站-天天基金网-基金数据-香港基金-历史净值明细

限量: 单次返回指定 code 和 symbol 所有历史数据

输入参数

| 名称     | 类型  | 描述                                                            |
|--------|-----|---------------------------------------------------------------|
| code   | str | code="1002200683"; 香港基金代码, 可以通过调用 **ak.fund_em_hk_rank()** 获取 |
| symbol | str | symbol="历史净值明细"; choice of {"历史净值明细", "分红送配详情"}               |

输出参数-历史净值明细

| 名称   | 类型      | 描述      |
|------|---------|---------|
| 净值日期 | object  | -       |
| 单位净值 | float64 | -       |
| 日增长值 | float64 | -       |
| 日增长率 | float64 | 注意单位: % |
| 单位   | object  | -       |

接口示例-历史净值明细

```python
import akshare as ak

fund_hk_fund_hist_em_df = ak.fund_hk_fund_hist_em(code='1002200683', symbol="历史净值明细")
print(fund_hk_fund_hist_em_df)
```

数据示例-历史净值明细

```
     净值日期     单位净值    日增长值    日增长率 单位
0    2021-01-19  10.0056 -0.0583 -0.5793  元
1    2021-01-18  10.0639  0.0620  0.6199  元
2    2021-01-15  10.0019 -0.0074 -0.0739  元
3    2021-01-14  10.0093  0.0444  0.4456  元
4    2021-01-13   9.9649 -0.0026 -0.0261  元
..          ...      ...     ...     ... ..
165  2020-05-14  10.0774  0.0214  0.2128  元
166  2020-05-13  10.0560  0.0210  0.2093  元
167  2020-05-12  10.0350  0.0350  0.3500  元
168  2020-05-11  10.0000  0.0000  0.0000  元
169  2020-05-08  10.0000                  元
```

输出参数-分红送配详情

| 名称    | 类型      | 描述  |
|-------|---------|-----|
| 年份    | object  | -   |
| 权益登记日 | object  | -   |
| 除息日   | object  | -   |
| 分红发放日 | object  | -   |
| 分红金额  | float64 | -   |
| 单位    | object  | -   |

接口示例-分红送配详情

```python
import akshare as ak

fund_hk_fund_hist_em_df = ak.fund_hk_fund_hist_em(code='1002200683', symbol="分红送配详情")
print(fund_hk_fund_hist_em_df)
```

数据示例-分红送配详情

```
     年份权益登记日         除息日    分红发放日    分红金额 单位
0  2020              2020-12-31              0.0522  元
1  2020  2020-11-30  2020-11-30  2020-12-14  0.0552  元
2  2020  2020-10-30  2020-10-30  2020-11-13  0.0573  元
3  2020  2020-09-30  2020-09-30  2020-10-16  0.0527  元
4  2020  2020-08-31  2020-08-31  2020-09-14  0.0545  元
5  2020  2020-07-31  2020-07-31  2020-08-14  0.0593  元
6  2020  2020-06-30  2020-06-30  2020-07-15  0.0669  元
```
