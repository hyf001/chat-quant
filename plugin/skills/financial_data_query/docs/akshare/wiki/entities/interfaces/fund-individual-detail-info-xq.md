---
title: "fund_individual_detail_info_xq - 基金交易规则"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_individual_detail_info_xq

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金交易规则
- 描述: 雪球基金-基金详情-基金交易规则
- 目标地址: https://danjuanfunds.com/djapi/fund/detail/675091
- 限量: 单次返回单只基金基金交易规则
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

### 基金交易规则

接口: fund_individual_detail_info_xq

目标地址: https://danjuanfunds.com/djapi/fund/detail/675091

描述: 雪球基金-基金详情-基金交易规则

限量: 单次返回单只基金基金交易规则

输入参数

| 名称      | 类型    | 描述                      |
|---------|-------|-------------------------|
| symbol  | str   | symbol="000001"; 基金代码   |
| timeout | float | timeout=None; 默认不设置超时参数 |

输出参数

| 名称    | 类型      | 描述 |
|-------|---------|----|
| 费用类型  | object  | -  |
| 条件或名称 | object  | -  |
| 费用    | float64 | -  |

接口示例

```python
import akshare as ak

fund_individual_detail_info_xq_df = ak.fund_individual_detail_info_xq(symbol="000001")
print(fund_individual_detail_info_xq_df)
```

数据示例

```
   费用类型                 条件或名称      费用
0  买入规则      0.0万<买入金额<100.0万     1.5
1  买入规则   100.0万<=买入金额<500.0万     1.2
2  买入规则  500.0万<=买入金额<1000.0万     0.8
3  买入规则         1000.0万<=买入金额  1000.0
4  卖出规则        0.0天<持有期限<7.0天     1.5
5  卖出规则            7.0天<=持有期限     0.5
6  其他费用                 基金管理费     1.2
7  其他费用                 基金托管费     0.2
```
