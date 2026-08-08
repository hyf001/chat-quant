---
title: "fund_individual_analysis_xq - 基金数据分析"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_individual_analysis_xq

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金数据分析
- 描述: 雪球基金-基金详情-数据分析
- 目标地址: https://danjuanfunds.com/funding/000001
- 限量: 返回单只基金历史表现分析数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

### 基金数据分析

接口: fund_individual_analysis_xq

目标地址: https://danjuanfunds.com/funding/000001

描述: 雪球基金-基金详情-数据分析

限量: 返回单只基金历史表现分析数据

输入参数

| 名称      | 类型    | 描述                      |
|---------|-------|-------------------------|
| symbol  | str   | symbol="000001"; 基金代码   |
| timeout | float | timeout=None; 默认不设置超时参数 |

输出参数

| 名称       | 类型      | 描述     |
|----------|---------|--------|
| 周期       | object  | -      |
| 较同类风险收益比 | int64   | 注意单位：% |
| 较同类抗风险波动 | int64   | 注意单位：% |
| 年化波动率    | float64 | 注意单位：% |
| 年化夏普比率   | float64 | -      |
| 最大回撤     | float64 | 注意单位：% |

接口示例

```python
import akshare as ak

fund_individual_analysis_xq_df = ak.fund_individual_analysis_xq(symbol="000001")
print(fund_individual_analysis_xq_df)
```

数据示例

```
   周期  较同类风险收益比 较同类抗风险波动  年化波动率  年化夏普比率   最大回撤
0  近1年         3        61  12.72   -1.89  26.58
1  近3年         9        56  18.66   -0.93  48.55
2  近5年         2        57  19.04   -0.11  48.55
```
