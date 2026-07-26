---
title: "index_hist_cni - 指数行情"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# index_hist_cni

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 国证指数 > 指数行情
- 描述: 国证指数-具体指数的日频率行情数据
- 目标地址: http://www.cnindex.com.cn/module/index-detail.html?act_menu=1&indexCode=399001
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 指数行情

接口: index_hist_cni

目标地址: http://www.cnindex.com.cn/module/index-detail.html?act_menu=1&indexCode=399001

描述: 国证指数-具体指数的日频率行情数据

输入参数

| 名称         | 类型  | 描述                                             |
|------------|-----|------------------------------------------------|
| symbol     | str | symbol="399005"; 从 ak.index_all_cni() 接口获取指数代码 |
| start_date | str | start_date="20230114"                          |
| end_date   | str | end_date="20240114"                            |

输出参数

| 名称  | 类型      | 描述       |
|-----|---------|----------|
| 日期  | object  | -        |
| 开盘价 | float64 | -        |
| 最高价 | float64 | -        |
| 最低价 | float64 | -        |
| 收盘价 | float64 | -        |
| 涨跌幅 | float64 | -        |
| 成交量 | float64 | 注意单位: 万手 |
| 成交额 | float64 | 注意单位: 亿元 |

接口示例

```python
import akshare as ak

index_hist_cni_df = ak.index_hist_cni(symbol="399005", start_date="20230114", end_date="20240114")
print(index_hist_cni_df)
```

数据示例

```
       日期      开盘价     最高价   最低价    收盘价   涨跌幅    成交量     成交额
0    2023-01-16  7646.53  7791.17  7622.78  7726.87  0.0111  3333.08  764.47
1    2023-01-17  7739.01  7763.82  7708.61  7747.54  0.0027  2451.54  553.48
2    2023-01-18  7754.17  7788.91  7742.23  7752.89  0.0007  2135.29  491.04
3    2023-01-19  7752.13  7821.15  7720.00  7821.15  0.0088  2316.82  551.81
4    2023-01-20  7831.02  7872.72  7812.26  7858.43  0.0048  2388.04  591.12
..          ...      ...      ...      ...      ...     ...      ...     ...
237  2024-01-08  5724.03  5740.62  5618.65  5618.65 -0.0209  2380.41  393.86
238  2024-01-09  5629.52  5683.72  5599.87  5641.58  0.0041  2480.49  427.98
239  2024-01-10  5619.17  5670.40  5562.28  5594.86 -0.0083  2180.10  402.80
240  2024-01-11  5588.35  5720.80  5575.51  5691.66  0.0173  2619.25  512.84
241  2024-01-12  5675.48  5709.83  5646.72  5646.90 -0.0079  2454.19  433.13
[242 rows x 8 columns]
```
