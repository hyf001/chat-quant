---
title: "fund_report_asset_allocation_cninfo - 基金资产配置"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_report_asset_allocation_cninfo

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金报告 > 基金资产配置
- 描述: 巨潮资讯-数据中心-专题统计-基金报表-基金资产配置
- 目标地址: https://webapi.cninfo.com.cn/#/thematicStatistics
- 限量: 返回所有基金资产配置数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 基金资产配置

接口: fund_report_asset_allocation_cninfo

目标地址: https://webapi.cninfo.com.cn/#/thematicStatistics

描述: 巨潮资讯-数据中心-专题统计-基金报表-基金资产配置

限量: 返回所有基金资产配置数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称            | 类型     | 描述       |
|---------------|--------|----------|
| 报告期           | object | -        |
| 基金覆盖家数        | object | 注意单位: 只  |
| 股票权益类占净资产比例   | object | 注意单位: %  |
| 债券固定收益类占净资产比例 | object | 注意单位: %  |
| 现金货币类占净资产比例   | object | 注意单位: %  |
| 基金市场净资产规模     | object | 注意单位: 亿元 |

接口示例

```python
import akshare as ak

fund_report_asset_allocation_cninfo_df = ak.fund_report_asset_allocation_cninfo()
print(fund_report_asset_allocation_cninfo_df)
```

数据示例

```
      报告期  基金覆盖家数  股票权益类占净资产比例  债券固定收益类占净资产比例  现金货币类占净资产比例  基金市场净资产规模
0   2024-06-30   11600        18.72          58.23        19.68  303791.15
1   2024-03-31   11346        20.37          58.42        20.17  286070.29
2   2023-12-31   11012        21.36          58.07        20.63  270156.52
3   2023-09-30   10776        22.22          57.36        17.84  270492.99
4   2023-06-30   10539        22.58          56.70        19.31  272807.40
..         ...     ...          ...            ...          ...        ...
63  2008-09-30     392        57.63          30.48        10.80   18272.96
64  2008-06-30     358        62.90          19.38        10.67   20680.07
65  2008-03-31     342        68.70          14.88        13.48   25757.00
66  2007-12-31     342        74.32          10.17        10.85   32918.04
67  2007-09-30     327        77.00           9.25        12.32   29924.06
[68 rows x 6 columns]
```
