---
title: "index_analysis_weekly_sw - 申万指数分析-周报表"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# index_analysis_weekly_sw

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 申万宏源研究 > 申万指数分析-周报表
- 描述: 申万宏源研究-指数分析-周报表
- 目标地址: https://www.swsresearch.com//institute_sw/allIndex/analysisIndex
- 限量: 该接口返回指定参数的数据
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 申万指数分析-周报表

接口: index_analysis_weekly_sw

目标地址: https://www.swsresearch.com//institute_sw/allIndex/analysisIndex

描述: 申万宏源研究-指数分析-周报表

限量: 该接口返回指定参数的数据

输入参数

| 名称     | 类型  | 描述                                                                            |
|--------|-----|-------------------------------------------------------------------------------|
| symbol | str | symbol="市场表征"; choice of {"市场表征", "一级行业", "二级行业", "风格指数"}                     |
| date   | str | start_date="20221104"; 通过调用 ak.index_analysis_week_month_sw(date="week") 接口获取 |

输出参数

| 名称     | 类型      | 描述       |
|--------|---------|----------|
| 指数代码   | object  | -        |
| 指数名称   | object  | -        |
| 发布日期   | object  | -        |
| 收盘指数   | float64 | -        |
| 成交量    | float64 | 注意单位: 亿股 |
| 涨跌幅    | float64 | 注意单位: %  |
| 换手率    | float64 | 注意单位: %  |
| 市盈率    | float64 | 注意单位: 倍  |
| 市净率    | float64 | 注意单位: 倍  |
| 均价     | float64 | 注意单位: 元  |
| 成交额占比  | float64 | 注意单位: %  |
| 流通市值   | float64 | 注意单位: 亿元 |
| 平均流通市值 | float64 | 注意单位: 亿元 |
| 股息率    | float64 | 注意单位: %  |

接口示例

```python
import akshare as ak

index_analysis_weekly_sw_df = ak.index_analysis_weekly_sw(symbol="市场表征", date="20241025")
print(index_analysis_weekly_sw_df)
```

数据示例

```
   指数代码     指数名称 发布日期     收盘指数  ...   成交额占比 流通市值  平均流通市值 股息率
0  801001     申万50   2024-10-25  3073.15  ...   12.21   80271.53  1605.43  2.85
1  801002     申万中小  2024-10-25  6137.80  ...   20.65   58574.66    63.39  1.47
2  801003     申万Ａ指  2024-10-25  3694.53  ...  100.00  349595.86    74.51  1.86
3  801005     申万创业  2024-10-25  2830.78  ...   42.01   58026.76    61.34  0.78
4  801250     申万制造  2024-10-25  4513.51  ...   56.09  121638.16    63.35  1.01
5  801260     申万消费  2024-10-25  6427.74  ...   15.56   72040.49    72.62  2.18
6  801270     申万投资  2024-10-25  3117.80  ...   12.77   49872.16    60.67  2.32
7  801280     申万服务  2024-10-25  2524.14  ...   38.88  112674.97    83.71  2.37
8  801300  申万300指数  2024-10-25  2877.66  ...   33.49  169457.12   564.86  2.46
[9 rows x 14 columns]
```
