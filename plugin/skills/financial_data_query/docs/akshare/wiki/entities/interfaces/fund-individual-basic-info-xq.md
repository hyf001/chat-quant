---
title: "fund_individual_basic_info_xq - 基金基本信息-雪球"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_individual_basic_info_xq

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金基本信息-雪球
- 描述: 雪球基金-基金详情
- 目标地址: https://danjuanfunds.com/funding/000001
- 限量: 单次返回单只基金基本信息
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

### 基金基本信息-雪球

接口: fund_individual_basic_info_xq

目标地址: https://danjuanfunds.com/funding/000001

描述: 雪球基金-基金详情

限量: 单次返回单只基金基本信息

输入参数

| 名称      | 类型    | 描述                      |
|---------|-------|-------------------------|
| symbol  | str   | symbol="000001"; 基金代码   |
| timeout | float | timeout=None; 默认不设置超时参数 |

输出参数

| 名称    | 类型     | 描述 |
|-------|--------|----|
| item  | object | -  |
| value | object | -  |

接口示例

```python
import akshare as ak

fund_individual_basic_info_xq_df = ak.fund_individual_basic_info_xq(symbol="000001")
print(fund_individual_basic_info_xq_df)
```

数据示例

```
      item                                              value
0     基金代码                                             000001
1     基金名称                                             华夏成长混合
2     基金全称                                            华夏成长前收费
3     成立时间                                         2001-12-18
4     最新规模                                             27.30亿
5     基金公司                                         华夏基金管理有限公司
6     基金经理                                            王泽实 万方方
7     托管银行                                       中国建设银行股份有限公司
8     基金类型                                             混合型-偏股
9     评级机构                                               晨星评级
10    基金评级                                               一星基金
11    投资策略  在股票投资方面，本基金重点投资于预期利润或收入具有良好增长潜力的成长型上市公司发行的股票，从...
12    投资目标  本基金属成长型基金，主要通过投资于具有良好成长性的上市公司的股票，在保持基金资产安全性和流动...
13  业绩比较基准                                       本基金暂不设业绩比较基准
```
