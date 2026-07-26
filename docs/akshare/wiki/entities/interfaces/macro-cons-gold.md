---
title: "macro_cons_gold - 全球最大黄金 ETF—SPDR Gold Trust 持仓报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_cons_gold

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 重要机构 > 全球最大黄金 ETF—SPDR Gold Trust 持仓报告
- 描述: 全球最大黄金 ETF—SPDR Gold Trust 持仓报告, 数据区间从 20041119-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_etf_gold
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 全球最大黄金 ETF—SPDR Gold Trust 持仓报告

接口: macro_cons_gold

目标地址: https://datacenter.jin10.com/reportType/dc_etf_gold

描述: 全球最大黄金 ETF—SPDR Gold Trust 持仓报告, 数据区间从 20041119-至今

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称    | 类型      | 描述       |
|-------|---------|----------|
| 商品    | object  | -        |
| 日期    | object  | -        |
| 总库存   | float64 | 注意单位: 吨  |
| 增持/减持 | float64 | 注意单位: 吨  |
| 总价值   | float64 | 注意单位: 美元 |

接口示例

```python
import akshare as ak

macro_cons_gold_df = ak.macro_cons_gold()
print(macro_cons_gold_df)
```

数据示例

```
      商品      日期     总库存  增持/减持  总价值
0     黄金  2004-11-19   57.85  49.76  8.288069e+08
1     黄金  2004-11-22   87.09  29.24  1.253785e+09
2     黄金  2004-11-24   96.42   9.33  1.390569e+09
3     黄金  2004-11-26  100.46   4.04  1.456603e+09
4     黄金  2004-11-29  103.57   3.11  1.502482e+09
   ..         ...     ...    ...           ...
2401  黄金  2024-03-22  835.33  -3.17  5.830850e+10
2402  黄金  2024-03-26  830.15  -5.18  5.816290e+10
2403  黄金  2024-04-01  826.98  -3.17  5.885568e+10
2404  黄金  2024-04-02  829.00   2.02  6.033517e+10
2405  黄金  2024-04-03  830.73   1.73  6.087828e+10
[2406 rows x 5 columns]
```
