---
title: "fund_report_industry_allocation_cninfo - 基金行业配置"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_report_industry_allocation_cninfo

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金报告 > 基金行业配置
- 描述: 巨潮资讯-数据中心-专题统计-基金报表-基金行业配置
- 目标地址: https://webapi.cninfo.com.cn/#/thematicStatistics
- 限量: 返回指定 date 的所有数据; date 从 2017 年开始
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 基金行业配置

接口: fund_report_industry_allocation_cninfo

目标地址: https://webapi.cninfo.com.cn/#/thematicStatistics

描述: 巨潮资讯-数据中心-专题统计-基金报表-基金行业配置

限量: 返回指定 date 的所有数据; date 从 2017 年开始

输入参数

| 名称   | 类型  | 描述                                                                                       |
|------|-----|------------------------------------------------------------------------------------------|
| date | str | date="20210630"; choice of {"XXXX0331", "XXXX0630", "XXXX0930", "XXXX1231"}, 其中 XXXX 为年份 |

输出参数

| 名称      | 类型      | 描述       |
|---------|---------|----------|
| 行业编码    | object  | -        |
| 证监会行业名称 | object  | -        |
| 报告期     | object  | -        |
| 基金覆盖家数  | int64   | 注意单位: 只  |
| 行业规模    | float64 | 注意单位: 亿元 |
| 占净资产比例  | float64 | 注意单位: %  |

接口示例

```python
import akshare as ak

fund_report_industry_allocation_cninfo_df = ak.fund_report_industry_allocation_cninfo(date="20210630")
print(fund_report_industry_allocation_cninfo_df)
```

数据示例

```
   行业编码           证监会行业名称         报告期  基金覆盖家数      行业规模  占净资产比例
0     A          农、林、牧、渔业  2021-06-30    3117    225.63    0.10
1     B               采矿业  2021-06-30    2182    807.04    0.35
2     C               制造业  2021-06-30    4897  37945.44   16.66
3     D  电力、热力、燃气及水生产和供应业  2021-06-30    4044    350.24    0.15
4     E               建筑业  2021-06-30    3931    236.84    0.10
5     F            批发和零售业  2021-06-30    3802    352.99    0.15
6     G       交通运输、仓储和邮政业  2021-06-30    2150    739.33    0.32
7     H            住宿和餐饮业  2021-06-30     513    145.43    0.06
8     I   信息传输、软件和信息技术服务业  2021-06-30    4472   2501.85    1.10
9     J               金融业  2021-06-30    4348   4539.41    1.99
10    K              房地产业  2021-06-30    2062    669.58    0.29
11    L          租赁和商务服务业  2021-06-30    2410   1035.95    0.45
12    M        科学研究和技术服务业  2021-06-30    3052   1595.45    0.70
13    N     水利、环境和公共设施管理业  2021-06-30    3486    124.66    0.05
14    O     居民服务、修理和其他服务业  2021-06-30       1      0.00    0.00
15    P                教育  2021-06-30     737     77.00    0.03
16    Q           卫生和社会工作  2021-06-30    1877   1487.55    0.65
17    R         文化、体育和娱乐业  2021-06-30    1386    375.28    0.16
18    S                综合  2021-06-30     278     60.31    0.03
```
