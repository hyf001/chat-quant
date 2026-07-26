---
title: "fund_individual_profit_probability_xq - 基金盈利概率"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_individual_profit_probability_xq

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金盈利概率
- 描述: 雪球基金-基金详情-盈利概率；历史任意时点买入，持有满X时间，盈利概率，以及平均收益
- 目标地址: https://danjuanfunds.com/funding/000001
- 限量: 单次返回单只基金历史任意时点买入，持有满 X 时间，盈利概率，以及平均收益
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

### 基金盈利概率

接口: fund_individual_profit_probability_xq

目标地址: https://danjuanfunds.com/funding/000001

描述: 雪球基金-基金详情-盈利概率；历史任意时点买入，持有满X时间，盈利概率，以及平均收益

限量: 单次返回单只基金历史任意时点买入，持有满 X 时间，盈利概率，以及平均收益

输入参数

| 名称      | 类型    | 描述                      |
|---------|-------|-------------------------|
| symbol  | str   | symbol="000001"; 基金代码   |
| timeout | float | timeout=None; 默认不设置超时参数 |

输出参数

| 名称   | 类型     | 描述     |
|------|--------|--------|
| 持有时长 | object | -      |
| 盈利概率 | object | 注意单位：% |
| 平均收益 | object | 注意单位：% |

接口示例

```python
import akshare as ak

fund_individual_profit_probability_xq_df = ak.fund_individual_profit_probability_xq(symbol="000001")
print(fund_individual_profit_probability_xq_df)
```

数据示例

```
  持有时长  盈利概率 平均收益
0  满6个月    53   5.97
1   满1年    59  14.23
2   满2年    66  32.34
3   满3年    76  51.16
```
