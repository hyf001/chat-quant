---
title: "index_zh_a_hist_min_em - 分时行情数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# index_zh_a_hist_min_em

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > A股股票指数 > 分时行情数据
- 描述: 东方财富网-指数数据-分时行情
- 目标地址: https://quote.eastmoney.com/center/hszs.html
- 限量: 单次返回具体指数指定 period 从 start_date 到 end_date 的之间的近期数据，该接口不能返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 分时行情数据

接口: index_zh_a_hist_min_em

目标地址: https://quote.eastmoney.com/center/hszs.html

描述: 东方财富网-指数数据-分时行情

限量: 单次返回具体指数指定 period 从 start_date 到 end_date 的之间的近期数据，该接口不能返回所有历史数据

输入参数

| 名称         | 类型  | 描述                                                                                |
|------------|-----|-----------------------------------------------------------------------------------|
| symbol     | str | symbol="399006"; 指数代码，此处不用市场标识                                                    |
| period     | str | period="1"; choice of {'1', '5', '15', '30', '60'}, 其中 1 分钟数据只能返回当前的, 其余只能返回近期的数据 |
| start_date | str | start_date="1979-09-01 09:32:00"; 开始日期时间                                          |
| end_date   | str | end_date="2222-01-01 09:32:00"; 结束时间时间                                            |

输出参数

| 名称  | 类型      | 描述      |
|-----|---------|---------|
| 时间  | object  | 交易日     |
| 开盘  | float64 | 开盘价     |
| 收盘  | float64 | 收盘价     |
| 最高  | float64 | 最高价     |
| 最低  | float64 | 最低价     |
| 成交量 | int64   | 注意单位: 手 |
| 成交额 | float64 | 注意单位: 元 |
| 均价  | float64 | -       |

接口示例

```python
import akshare as ak

index_zh_a_hist_min_em_df = ak.index_zh_a_hist_min_em(symbol="000001", period="1", start_date="2023-12-11 09:30:00", end_date="2023-12-11 19:00:00")
print(index_zh_a_hist_min_em_df)
```

数据示例

```
           时间       开盘       收盘  ...       成交量           成交额       均价
0    2023-12-11 09:30:00  2956.29  2956.29  ...   3198631  3.394971e+09  2957.681
1    2023-12-11 09:31:00  2955.35  2937.70  ...  12531907  1.227149e+10  2945.626
2    2023-12-11 09:32:00  2938.36  2935.57  ...   8823405  8.810568e+09  2940.907
3    2023-12-11 09:33:00  2935.72  2932.00  ...   7235184  7.282885e+09  2940.683
4    2023-12-11 09:34:00  2932.48  2933.37  ...   5309002  5.608316e+09  2945.141
..                   ...      ...      ...  ...       ...           ...       ...
236  2023-12-11 14:56:00  2990.23  2989.94  ...   2032283  2.301672e+09  2999.493
237  2023-12-11 14:57:00  2989.94  2990.58  ...   2234140  2.480918e+09  3000.265
238  2023-12-11 14:58:00  2990.73  2990.63  ...    128204  1.482932e+08  3000.532
239  2023-12-11 14:59:00  2990.63  2990.63  ...         0  0.000000e+00  3000.532
240  2023-12-11 15:00:00  2990.63  2991.44  ...   3969436  4.319616e+09  3001.557
[241 rows x 8 columns]
```
