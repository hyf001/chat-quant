---
title: "macro_stock_finance - 股票筹资"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_stock_finance

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融市场 > 股票筹资
- 描述: 同花顺-数据中心-宏观数据-股票筹资
- 目标地址: https://data.10jqka.com.cn/macro/finance/
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 股票筹资

接口: macro_stock_finance

目标地址: https://data.10jqka.com.cn/macro/finance/

描述: 同花顺-数据中心-宏观数据-股票筹资

限量: 单次返回所有历史数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称     | 类型      | 描述 |
|--------|---------|----|
| 月份     | object  | -  |
| 募集资金   | float64 | -  |
| 首发募集资金 | float64 | -  |
| 增发募集资金 | float64 | -  |
| 配股募集资金 | float64 | -  |

接口示例

```python
import akshare as ak

macro_stock_finance_df = ak.macro_stock_finance()
print(macro_stock_finance_df)
```

数据示例

```
    月份     募集资金  首发募集资金 增发募集资金  配股募集资金
0   2023-05   567.67  368.03   199.64     NaN
1   2023-06   600.62  313.84   189.56   97.22
2   2023-07  1145.38  602.19   543.19     NaN
3   2023-08   890.07  244.96   632.60   12.51
4   2023-09   310.89  142.20   168.69     NaN
5   2023-10   318.26   57.45   260.81     NaN
6   2023-11   416.35   81.24   317.13   17.98
7   2023-12   439.66  110.33   329.33     NaN
8   2024-01   497.90  116.16   381.74     NaN
9   2024-02    44.83   18.00    26.83     NaN
10  2024-03   306.71   53.24   253.47     NaN
11  2024-04   182.98    9.31   173.67     NaN
12  2024-05    84.48   21.49    62.99     NaN
13  2024-06   109.70   38.76    70.93     NaN
14  2024-07   185.47   42.12   143.35     NaN
15  2024-08   104.06   45.85    58.21     NaN
16  2024-09    53.19   39.66    13.53     NaN
17  2024-10   107.17   37.35    69.83     NaN
18  2024-11   190.44   52.66   137.79     NaN
19  2024-12   402.63   79.51   323.12     NaN
20  2025-01   847.32   41.09   806.23     NaN
21  2025-02    78.43   34.50    43.93     NaN
22  2025-03  1360.01   58.11  1301.91     NaN
23  2025-04   219.92   56.44   163.48     NaN
24  2025-05   221.00   88.37   132.63     NaN
25  2025-06  5392.38   44.93  5347.45     NaN
26  2025-07   510.08  219.44   290.63     NaN
27  2025-08   193.42   13.56   179.86     NaN
28  2025-09  1543.38   98.45  1444.93     NaN
29  2025-10   313.78  112.92   200.86     NaN
```
