---
title: "macro_euro_unemployment_rate_mom - 欧元区失业率报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_euro_unemployment_rate_mom

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 欧元区宏观 > 国民经济运行状况 > 劳动力市场 > 欧元区失业率报告
- 描述: 欧元区失业率报告, 数据区间从 19980501-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_eurozone_unemployment_rate_mom
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 欧元区失业率报告

接口: macro_euro_unemployment_rate_mom

目标地址: https://datacenter.jin10.com/reportType/dc_eurozone_unemployment_rate_mom

描述: 欧元区失业率报告, 数据区间从 19980501-至今

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称  | 类型      | 描述      |
|-----|---------|---------|
| 商品  | object  | -       |
| 日期  | object  | -       |
| 今值  | float64 | 注意单位: % |
| 预测值 | float64 | 注意单位: % |
| 前值  | float64 | 注意单位: % |

接口示例

```python
import akshare as ak

macro_euro_unemployment_rate_mom_df = ak.macro_euro_unemployment_rate_mom()
print(macro_euro_unemployment_rate_mom_df)
```

数据示例

```
         商品          日期    今值  预测值    前值
0    欧元区失业率  1998-05-01  10.6  NaN   NaN
1    欧元区失业率  1998-06-01  10.5  NaN  10.6
2    欧元区失业率  1998-07-01  10.5  NaN  10.5
3    欧元区失业率  1998-08-01  10.4  NaN  10.5
4    欧元区失业率  1998-09-01  10.4  NaN  10.4
..      ...         ...   ...  ...   ...
290  欧元区失业率  2022-06-30   6.6  6.8   6.7
291  欧元区失业率  2022-08-01   6.6  6.6   6.6
292  欧元区失业率  2022-09-01   6.6  6.6   6.7
293  欧元区失业率  2022-09-30   6.6  6.6   6.6
294  欧元区失业率  2022-11-03   6.6  6.6   6.7
```
