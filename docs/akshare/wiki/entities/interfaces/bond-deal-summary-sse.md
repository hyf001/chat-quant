---
title: "bond_deal_summary_sse - 债券成交概览"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, bond, parameters, returns, example]
sources: [raw/data-dictionary/bond/bond.md]
confidence: high
---
# bond_deal_summary_sse

- 分类: [[bond-bond|AKShare 债券数据]]
- 主题路径: AKShare 债券数据 > 上交所债券 > 债券成交概览
- 描述: 上登债券信息网-市场数据-市场统计-市场概览-债券成交概览
- 目标地址: http://bond.sse.com.cn/data/statistics/overview/turnover/
- 限量: 单次返回指定交易日的债券成交概览数据
- 来源页面: https://akshare.akfamily.xyz/data/bond/bond.html

## 相关

- [[bond-bond|AKShare 债券数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 债券成交概览

接口: bond_deal_summary_sse

目标地址: http://bond.sse.com.cn/data/statistics/overview/turnover/

描述: 上登债券信息网-市场数据-市场统计-市场概览-债券成交概览

限量: 单次返回指定交易日的债券成交概览数据

输入参数

| 名称   | 类型  | 描述              |
|------|-----|-----------------|
| date | str | date='20200104' |

输出参数

| 名称     | 类型      | 描述       |
|--------|---------|----------|
| 债券类型   | object  | -        |
| 当日成交笔数 | int64   | -        |
| 当日成交金额 | float64 | 注意单位: 万元 |
| 当年成交笔数 | int64   | -        |
| 当年成交金额 | float64 | 注意单位: 万元 |
| 数据日期   | object  | -        |

接口示例

```python
import akshare as ak

bond_summary_sse_df = ak.bond_deal_summary_sse(date='20210104')
print(bond_summary_sse_df)
```

数据示例

```
        债券类型  当日成交笔数 当日成交金额  当年成交笔数  当年成交金额  数据日期
0      记账式国债    3685   363349.44    3685   363349.44  2021-01-04
1      地方政府债      11    81284.62      11    81284.62  2021-01-04
2        金融债     568    11075.26     568    11075.26  2021-01-04
3        企业债     234   124537.76     234   124537.76  2021-01-04
4    中小企业私募债     298   802906.69     298   802906.69  2021-01-04
5    公开发行公司债    1570  1442430.80    1570  1442430.80  2021-01-04
6   非公开发行公司债      26    66038.67      26    66038.67  2021-01-04
7        可转债  923863  1566929.29  923863  1566929.29  2021-01-04
8       可交换债    3962    26873.67    3962    26873.67  2021-01-04
9        分离债       0        0.00       0        0.00  2021-01-04
10  企业资产支持证券      44   215197.41      44   215197.41  2021-01-04
11  信贷资产支持证券       0        0.00       0        0.00  2021-01-04
12      其他债券       0        0.00       0        0.00  2021-01-04
13        合计  934261  4700623.60  934261  4700623.60  2021-01-04
```
