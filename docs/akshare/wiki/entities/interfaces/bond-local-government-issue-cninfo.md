---
title: "bond_local_government_issue_cninfo - 地方债发行"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, bond, parameters, returns, example]
sources: [raw/data-dictionary/bond/bond.md]
confidence: high
---
# bond_local_government_issue_cninfo

- 分类: [[bond-bond|AKShare 债券数据]]
- 主题路径: AKShare 债券数据 > 债券发行 > 地方债发行
- 描述: 巨潮资讯-数据中心-专题统计-债券报表-债券发行-地方债发行
- 目标地址: https://webapi.cninfo.com.cn/#/thematicStatistics
- 来源页面: https://akshare.akfamily.xyz/data/bond/bond.html

## 相关

- [[bond-bond|AKShare 债券数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 地方债发行

接口: bond_local_government_issue_cninfo

目标地址: https://webapi.cninfo.com.cn/#/thematicStatistics

描述: 巨潮资讯-数据中心-专题统计-债券报表-债券发行-地方债发行

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

bond_local_government_issue_cninfo_df = ak.bond_local_government_issue_cninfo(start_date="20210911", end_date="20211110")
print(bond_local_government_issue_cninfo_df)
```

数据示例

```
         债券代码  ...                                             债券名称
0      186882  ...               2021年新疆维吾尔自治区(新疆生产建设兵团)再融资一般债券(二期)
1      192633  ...               2021年新疆维吾尔自治区(新疆生产建设兵团)再融资一般债券(二期)
2     2171216  ...               2021年新疆维吾尔自治区(新疆生产建设兵团)再融资一般债券(二期)
3      186883  ...               2021年新疆维吾尔自治区(新疆生产建设兵团)再融资专项债券(二期)
4      192634  ...               2021年新疆维吾尔自治区(新疆生产建设兵团)再融资专项债券(二期)
...       ...  ...                                              ...
1444   192226  ...         2021年山东省政府棚改专项债券(八期)-2021年山东省政府专项债券(四十期)
1445  2105885  ...         2021年山东省政府棚改专项债券(八期)-2021年山东省政府专项债券(四十期)
1446   186469  ...  2021年山东省政府支持中小银行发展专项债券(一期)-2021年山东省政府专项债券(四十一期)
1447   192227  ...  2021年山东省政府支持中小银行发展专项债券(一期)-2021年山东省政府专项债券(四十一期)
1448  2105886  ...  2021年山东省政府支持中小银行发展专项债券(一期)-2021年山东省政府专项债券(四十一期)
[1449 rows x 15 columns]
```
