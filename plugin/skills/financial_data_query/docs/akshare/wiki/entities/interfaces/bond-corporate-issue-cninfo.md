---
title: "bond_corporate_issue_cninfo - 企业债发行"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, bond, parameters, returns, example]
sources: [raw/data-dictionary/bond/bond.md]
confidence: high
---
# bond_corporate_issue_cninfo

- 分类: [[bond-bond|AKShare 债券数据]]
- 主题路径: AKShare 债券数据 > 债券发行 > 企业债发行
- 描述: 巨潮资讯-数据中心-专题统计-债券报表-债券发行-企业债发行
- 目标地址: https://webapi.cninfo.com.cn/#/thematicStatistics
- 来源页面: https://akshare.akfamily.xyz/data/bond/bond.html

## 相关

- [[bond-bond|AKShare 债券数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 企业债发行

接口: bond_corporate_issue_cninfo

目标地址: https://webapi.cninfo.com.cn/#/thematicStatistics

描述: 巨潮资讯-数据中心-专题统计-债券报表-债券发行-企业债发行

输入参数

| 名称         | 类型  | 描述                    |
|------------|-----|-----------------------|
| start_date | str | start_date="20210911" |
| end_date   | str | end_date="20211110"   |

输出参数

| 名称         | 类型      | 描述       |
|------------|---------|----------|
| 债券代码       | object  | -        |
| 债券简称       | object  | -        |
| 公告日期       | object  | -        |
| 交易所网上发行起始日 | object  | -        |
| 交易所网上发行终止日 | object  | -        |
| 计划发行总量     | float64 | 注意单位: 万元 |
| 实际发行总量     | float64 | 注意单位: 万元 |
| 发行面值       | float64 | -        |
| 发行价格       | int64   | 注意单位: 元  |
| 发行方式       | object  | -        |
| 发行对象       | object  | -        |
| 发行范围       | object  | -        |
| 承销方式       | object  | -        |
| 最小认购单位     | float64 | 注意单位: 万元 |
| 募资用途说明     | object  | -        |
| 最低认购额      | float64 | 注意单位: 万元 |
| 债券名称       | object  | -        |

接口示例

```python
import akshare as ak

bond_corporate_issue_cninfo_df = ak.bond_corporate_issue_cninfo(start_date="20210911", end_date="20211110")
print(bond_corporate_issue_cninfo_df)
```

数据示例

```
        债券代码       债券简称  ...       最低认购额                                      债券名称
0     184109     21开泰01  ...  10000000.0        2021年如东县开泰城建投资有限公司城市停车场建设专项债券(品种一)
1    2180441  21开泰专项债01  ...  10000000.0        2021年如东县开泰城建投资有限公司城市停车场建设专项债券(品种一)
2     184114     21云发01  ...   1000000.0             2021年第一期株洲市云龙发展投资控股集团有限公司公司债券
3    2180450    21株云发01  ...   1000000.0             2021年第一期株洲市云龙发展投资控股集团有限公司公司债券
4     188968     21电力Y3  ...  10000000.0  2021年国投电力控股股份有限公司面向专业投资者公开发行可续期公司债券(第三期)
..       ...        ...  ...         ...                                       ...
429   188725     21通用01  ...  10000000.0   2021年中国通用技术(集团)控股有限责任公司公开发行公司债券(第一期)品种一
430   188702     21正奇01  ...  10000000.0       2021年正奇控股股份有限公司面向专业投资者公开发行公司债券(第一期)
431   188738     21舟城02  ...  10000000.0   2021年舟山海城建设投资集团有限公司面向专业投资者公开发行公司债券(第二期)
432   188758     21一航Y2  ...   1000000.0        2021年中交第一航务工程局有限公司公开发行可续期公司债券(第二期)
433   149632     H1碧地03  ...   1000000.0      2021年碧桂园地产集团有限公司面向专业投资者公开发行公司债券(第三期)
[434 rows x 17 columns]
```
