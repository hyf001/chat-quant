---
title: "stock_gpzy_pledge_ratio_detail_em - 重要股东股权质押明细"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_gpzy_pledge_ratio_detail_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 股票质押 > 重要股东股权质押明细
- 描述: 东方财富网-数据中心-特色数据-股权质押-重要股东股权质押明细
- 目标地址: https://data.eastmoney.com/gpzy/pledgeDetail.aspx
- 限量: 单次所有历史数据, 由于数据量比较大需要等待一定时间
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 重要股东股权质押明细

接口: stock_gpzy_pledge_ratio_detail_em

目标地址: https://data.eastmoney.com/gpzy/pledgeDetail.aspx

描述: 东方财富网-数据中心-特色数据-股权质押-重要股东股权质押明细

限量: 单次所有历史数据, 由于数据量比较大需要等待一定时间

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称      | 类型      | 描述      |
|---------|---------|---------|
| 序号      | int64   | -       |
| 股票代码    | object  | -       |
| 股票简称    | object  | -       |
| 股东名称    | object  | -       |
| 质押股份数量  | float64 | 注意单位: 股 |
| 占所持股份比例 | float64 | 注意单位: % |
| 占总股本比例  | float64 | 注意单位: % |
| 质押机构    | object  | -       |
| 最新价     | float64 | 注意单位: 元 |
| 质押日收盘价  | float64 | 注意单位: 元 |
| 预估平仓线   | float64 | 注意单位: 元 |
| 公告日期    | object  | -       |
| 质押开始日期  | object  | -       |
| 质押结束日期  | object  | -       |
| 状态      | object  | -       |

接口示例

```python
import akshare as ak

stock_gpzy_pledge_ratio_detail_em_df = ak.stock_gpzy_pledge_ratio_detail_em()
print(stock_gpzy_pledge_ratio_detail_em_df)
```

数据示例

```
        序号    股票代码  股票简称 ... 预估平仓线  质押开始日期    质押结束日期   状态  公告日期
0            1  002501  利源股份 ... 1.036000  2026-03-27         NaT  未解押  2026-03-31
1            2  603081  大丰实业 ... 6.591200  2026-03-27         NaT  未解押  2026-03-31
2            3  603335   迪生力 ... 3.304000  2026-03-27         NaT  未解押  2026-03-31
3            4  688153  唯捷创芯 ... 18.967200  2026-03-27         NaT  未解押  2026-03-31
4            5  603515  欧普照明 ... 10.628800  2026-03-27         NaT  未解押  2026-03-31
        ...     ...   ...  ...       ...         ...         ...         ...
124783  124784  000683  博源化工 ... 1.090851  2002-09-27         NaT  未解押  2002-10-10
124784  124785  000415  渤海租赁 ... 1.897415  2001-09-03  2002-09-03  已解押  2002-09-25
124785  124786  000028  国药一致 ... 8.302703  2000-12-20  2001-12-23  已解押  2002-03-29
124786  124787  200028   一致B ... 8.302703  2000-12-20  2001-12-23  已解押  2002-03-29
124787  124788  600745  闻泰科技 ... 7.840701  2001-11-20         NaT  未解押  2001-11-24

[124788 rows x 15 columns]
```
