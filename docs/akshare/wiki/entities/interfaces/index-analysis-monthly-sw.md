---
title: "index_analysis_monthly_sw - 申万指数分析-月报表"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# index_analysis_monthly_sw

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 申万宏源研究 > 申万指数分析-月报表
- 描述: 申万宏源研究-指数分析-月报表
- 目标地址: https://www.swsresearch.com/institute_sw/allIndex/analysisIndex
- 限量: 该接口返回指定参数的数据
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 申万指数分析-月报表

接口: index_analysis_monthly_sw

目标地址: https://www.swsresearch.com/institute_sw/allIndex/analysisIndex

描述: 申万宏源研究-指数分析-月报表

限量: 该接口返回指定参数的数据

输入参数

| 名称     | 类型  | 描述                                                                             |
|--------|-----|--------------------------------------------------------------------------------|
| symbol | str | symbol="市场表征"; choice of {"市场表征", "一级行业", "二级行业", "风格指数"}                      |
| date   | str | start_date="20221031"; 通过调用 ak.index_analysis_week_month_sw(date="month") 接口获取 |

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

index_analysis_monthly_sw_df = ak.index_analysis_monthly_sw(symbol="市场表征", date="20240930")
print(index_analysis_monthly_sw_df)
```

数据示例

```
   指数代码    指数名称   发布日期    收盘指数  ...  成交额占比  流通市值 平均流通市值 股息率
0  801001     申万50   2024-09-30  3152.14  ...   16.29   82379.30  1647.59  2.72
1  801002     申万中小  2024-09-30  5988.52  ...   21.36   57060.17    61.75  1.47
2  801003     申万Ａ指  2024-09-30  3636.02  ...  100.00  343958.32    73.31  1.84
3  801005     申万创业  2024-09-30  2636.53  ...   30.85   53963.62    57.04  0.84
4  801250     申万制造  2024-09-30  4218.84  ...   44.72  113449.40    59.06  1.04
5  801260     申万消费  2024-09-30  6665.38  ...   20.02   74580.85    75.18  2.07
6  801270     申万投资  2024-09-30  3193.45  ...   16.36   50974.14    62.16  2.22
7  801280     申万服务  2024-09-30  2489.15  ...   39.48  110978.29    82.63  2.33
8  801300  申万300指数  2024-09-30  2889.29  ...   35.97  170126.42   567.09  2.39
[9 rows x 14 columns]
```
