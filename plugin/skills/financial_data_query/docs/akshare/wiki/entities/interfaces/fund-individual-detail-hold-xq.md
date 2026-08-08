---
title: "fund_individual_detail_hold_xq - 基金持仓资产比例"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_individual_detail_hold_xq

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金持仓资产比例
- 描述: 雪球基金-基金详情-基金持仓-详情
- 目标地址: https://danjuanfunds.com/rn/fund-detail/archive?id=103&code=000001
- 限量: 单次返回单只基金指定日期的持仓大类资产比例
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

### 基金持仓资产比例

接口: fund_individual_detail_hold_xq

目标地址: https://danjuanfunds.com/rn/fund-detail/archive?id=103&code=000001

描述: 雪球基金-基金详情-基金持仓-详情

限量: 单次返回单只基金指定日期的持仓大类资产比例

输入参数

| 名称      | 类型    | 描述                      |
|---------|-------|-------------------------|
| symbol  | str   | symbol="000001"; 基金代码   |
| date    | str   | date="20231231"; 季度日期   |
| timeout | float | timeout=None; 默认不设置超时参数 |

输出参数

| 名称   | 类型      | 描述     |
|------|---------|--------|
| 资产类型 | object  | -      |
| 仓位占比 | float64 | 注意单位：% |

接口示例

```python
import akshare as ak

fund_individual_detail_hold_xq_df = ak.fund_individual_detail_hold_xq(symbol="002804", date="20231231")
print(fund_individual_detail_hold_xq_df)
```

数据示例

```
  资产类型   仓位占比
0   股票  51.95
1   现金  19.51
2   其他  29.09
```
