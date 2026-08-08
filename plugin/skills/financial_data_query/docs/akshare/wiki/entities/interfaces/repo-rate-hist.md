---
title: "repo_rate_hist - 回购定盘利率-历史"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, interest-rate, parameters, returns, example]
sources: [raw/data-dictionary/interest_rate/interest_rate.md]
confidence: high
---
# repo_rate_hist

- 分类: [[interest-rate-interest-rate|AKShare 利率数据]]
- 主题路径: AKShare 利率数据 > 回购定盘利率-历史
- 描述: 回购定盘利率数据
- 目标地址: https://www.chinamoney.com.cn/chinese/bkfrr/
- 限量: 单次返回指定日期间(一年)的所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/interest_rate/interest_rate.html

## 相关

- [[interest-rate-interest-rate|AKShare 利率数据]]
- [[_meta/topic-map]]

## 源文摘录

### 回购定盘利率-历史

接口: repo_rate_hist

目标地址: https://www.chinamoney.com.cn/chinese/bkfrr/

描述: 回购定盘利率数据

限量: 单次返回指定日期间(一年)的所有历史数据

输入参数

| 名称         | 类型  | 描述                                     |
|------------|-----|----------------------------------------|
| start_date | str | start_date="20200930"; 开始时间与结束时间需要在一年内 |
| end_date   | str | end_date="20201029"; 开始时间与结束时间需要在一年内   |

输出参数

| 名称     | 类型      | 描述      |
|--------|---------|---------|
| date   | object  | -       |
| FR001  | float64 | 注意单位: % |
| FR007  | float64 | 注意单位: % |
| FR014  | float64 | 注意单位: % |
| FDR001 | float64 | 注意单位: % |
| FDR007 | float64 | 注意单位: % |
| FDR014 | float64 | 注意单位: % |

接口示例

```python
import akshare as ak

repo_rate_hist_df = ak.repo_rate_hist(start_date="20231001", end_date="20240101")
print(repo_rate_hist_df)
```

数据示例

```
          date   FR001   FR007  FR014  FDR001  FDR007  FDR014
0   2023-10-07  1.7000  1.8500   1.82  1.7000  1.8224    1.82
1   2023-10-08  1.5600  1.8000   1.78  1.5300  1.7500    1.75
2   2023-10-09  1.8100  2.0100   1.85  1.7400  1.8000    1.80
3   2023-10-10  1.9300  2.0500   2.22  1.8400  1.8600    1.90
4   2023-10-11  1.9600  2.1400   2.20  1.8700  1.9200    2.00
..         ...     ...     ...    ...     ...     ...     ...
57  2023-12-25  1.6210  1.8117   3.90  1.5900  1.8000    3.15
58  2023-12-26  1.5500  4.3500   3.80  1.4969  1.8305    3.10
59  2023-12-27  1.5100  4.0000   3.10  1.4400  1.8728    3.05
60  2023-12-28  1.5000  3.2000   3.00  1.3900  1.9572    2.95
61  2023-12-29  1.9149  2.4000   2.45  1.7400  2.3000    2.40
[62 rows x 7 columns]
```
