---
title: "bond_treasure_issue_cninfo - 国债发行"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, bond, parameters, returns, example]
sources: [raw/data-dictionary/bond/bond.md]
confidence: high
---
# bond_treasure_issue_cninfo

- 分类: [[bond-bond|AKShare 债券数据]]
- 主题路径: AKShare 债券数据 > 债券发行 > 国债发行
- 描述: 巨潮资讯-数据中心-专题统计-债券报表-债券发行-国债发行
- 目标地址: https://webapi.cninfo.com.cn/#/thematicStatistics
- 来源页面: https://akshare.akfamily.xyz/data/bond/bond.html

## 相关

- [[bond-bond|AKShare 债券数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 国债发行

接口: bond_treasure_issue_cninfo

目标地址: https://webapi.cninfo.com.cn/#/thematicStatistics

描述: 巨潮资讯-数据中心-专题统计-债券报表-债券发行-国债发行

输入参数

| 名称         | 类型  | 描述                    |
|------------|-----|-----------------------|
| start_date | str | start_date="20210911" |
| end_date   | str | end_date="20211110"   |

输出参数

| 名称     | 类型      | 描述       |
|--------|---------|----------|
| 债券代码   | object  | -        |
| 债券简称   | object  | -        |
| 发行起始日  | object  | -        |
| 发行终止日  | object  | -        |
| 计划发行总量 | float64 | 注意单位: 亿元 |
| 实际发行总量 | float64 | 注意单位: 亿元 |
| 发行价格   | float64 | 注意单位: 元  |
| 单位面值   | int64   | 注意单位: 元  |
| 缴款日    | object  | -        |
| 增发次数   | int64   | -        |
| 交易市场   | object  | -        |
| 发行方式   | object  | -        |
| 发行对象   | object  | -        |
| 公告日期   | object  | -        |
| 债券名称   | object  | -        |

接口示例

```python
import akshare as ak

bond_treasure_issue_cninfo_df = ak.bond_treasure_issue_cninfo(start_date="20210910", end_date="20211109")
print(bond_treasure_issue_cninfo_df)
```

数据示例

```
       债券代码      债券简称  ...        公告日期                债券名称
0    020450    21贴债53  ...  2021-10-29  2021年记账式贴现(五十三期)国债
1    108450    贴债2153  ...  2021-10-29  2021年记账式贴现(五十三期)国债
2    219953  21贴现国债53  ...  2021-10-29  2021年记账式贴现(五十三期)国债
3    020451    21贴债54  ...  2021-11-04  2021年记账式贴现(五十四期)国债
4    108451    贴债2154  ...  2021-11-04  2021年记账式贴现(五十四期)国债
..      ...       ...  ...         ...                 ...
99   102103    国债2103  ...  2021-09-03    2021年记账式附息(三期)国债
100  210003  21附息国债03  ...  2021-09-03    2021年记账式附息(三期)国债
101  020441    21贴债44  ...  2021-09-09  2021年记账式贴现(四十四期)国债
102  108441    贴债2144  ...  2021-09-09  2021年记账式贴现(四十四期)国债
103  219944  21贴现国债44  ...  2021-09-09  2021年记账式贴现(四十四期)国债
[104 rows x 15 columns]
```
