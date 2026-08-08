---
title: "fund_open_fund_rank_em - 开放式基金排行"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_open_fund_rank_em

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金排行 > 开放式基金排行
- 描述: 东方财富网-数据中心-开放式基金排行
- 目标地址: https://fund.eastmoney.com/data/fundranking.html
- 限量: 单次返回当前时刻所有数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 开放式基金排行

接口: fund_open_fund_rank_em

目标地址: https://fund.eastmoney.com/data/fundranking.html

描述: 东方财富网-数据中心-开放式基金排行

限量: 单次返回当前时刻所有数据

输入参数

| 名称     | 类型  | 描述                                                                       |
|--------|-----|--------------------------------------------------------------------------|
| symbol | str | symbol="全部"; choice of {"全部", "股票型", "混合型", "债券型", "指数型", "QDII", "FOF"} |

输出参数

| 名称   | 类型      | 描述      |
|------|---------|---------|
| 序号   | int64   | -       |
| 基金代码 | object  | -       |
| 基金简称 | object  | -       |
| 日期   | object  | -       |
| 单位净值 | float64 | -       |
| 累计净值 | float64 | -       |
| 日增长率 | float64 | 注意单位: % |
| 近1周  | float64 | 注意单位: % |
| 近1月  | float64 | 注意单位: % |
| 近3月  | float64 | 注意单位: % |
| 近6月  | float64 | 注意单位: % |
| 近1年  | float64 | 注意单位: % |
| 近2年  | float64 | 注意单位: % |
| 近3年  | float64 | 注意单位: % |
| 今年来  | float64 | 注意单位: % |
| 成立来  | float64 | 注意单位: % |
| 自定义  | float64 | 注意单位: % |
| 手续费  | object  | -       |

接口示例

```python
import akshare as ak

fund_open_fund_rank_em_df = ak.fund_open_fund_rank_em(symbol="全部")
print(fund_open_fund_rank_em_df)
```

数据示例

```
      序号    基金代码                    基金简称  ...       成立来      自定义    手续费
0          1  003384                  金鹰添盈纯债债券A  ...  146.67  138.619600  0.08%
1          2  012623                  金鹰添盈纯债债券C  ...  106.92  133.400700  0.00%
2          3  008729                    同泰恒利纯债C  ...  141.60  125.063500  0.00%
3          4  008728                    同泰恒利纯债A  ...  139.84  122.035400  0.08%
4          5  017091  景顺长城纳斯达克科技ETF联接(QDII)A人民币  ...   62.36         NaN  0.12%
      ...     ...                        ...  ...     ...         ...    ...
15005  15006  019983                  泓德智选启元混合C  ...  -14.00  -14.000000  0.00%
15006  15007  020693                  长城健康消费混合C  ...    5.15    5.148741  0.00%
15007  15008  019936  华安恒生互联网科技业ETF发起式联接(QDII)A  ...    1.39    1.390000  0.05%
15008  15009  020880                  天弘齐享债券发起D  ...    0.21    0.207645  0.06%
15009  15010  020738               安信宝利债券(LOF)C  ...    0.72    0.716648  0.00%
[15010 rows x 18 columns]
```
