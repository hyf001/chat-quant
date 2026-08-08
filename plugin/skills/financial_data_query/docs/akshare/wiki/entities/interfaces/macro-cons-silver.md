---
title: "macro_cons_silver - 全球最大白银ETF--iShares Silver Trust持仓报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_cons_silver

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 重要机构 > 全球最大白银ETF--iShares Silver Trust持仓报告
- 描述: 全球最大白银 ETF--iShares Silver Trust 持仓报告, 数据区间从 20041202-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_etf_sliver
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 全球最大白银ETF--iShares Silver Trust持仓报告

接口: macro_cons_silver

目标地址: https://datacenter.jin10.com/reportType/dc_etf_sliver

描述: 全球最大白银 ETF--iShares Silver Trust 持仓报告, 数据区间从 20041202-至今

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

macro_cons_silver_df = ak.macro_cons_silver()
print(macro_cons_silver_df)
```

数据示例

```
      商品      日期      总库存   增持/减持   总价值
0     白银  2014-12-02  10891.14   68.54   5505643206
1     白银  2014-12-03  10806.20  -84.94   5614273871
2     白银  2014-12-05  10737.66  -68.54   5626921446
3     白银  2014-12-11  10648.28  -89.38   5839725280
4     白银  2014-12-13  10606.57  -41.71   5820097631
   ..         ...       ...     ...          ...
1183  白银  2024-03-26  13159.26   52.62  10392678118
1184  白银  2024-03-27  13190.55   31.29  10392678118
1185  白银  2024-04-01  13399.59  209.04  10567503086
1186  白银  2024-04-02  13487.76   88.17  11118260677
1187  白银  2024-04-03  13601.92  114.16  11476815280
[1188 rows x 5 columns]
```
