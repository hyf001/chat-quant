---
title: "stock_zh_index_daily_tx - 历史行情数据-腾讯"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# stock_zh_index_daily_tx

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > A股股票指数 > 历史行情数据 > 历史行情数据-腾讯
- 描述: 股票指数(或者股票)历史行情数据, 支持自定义时间范围
- 目标地址: https://gu.qq.com/sh000919/zs
- 限量: 单次返回具体某个股票指数(或者股票)指定时间范围内的历史行情数据
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 历史行情数据-腾讯

接口: stock_zh_index_daily_tx

目标地址: https://gu.qq.com/sh000919/zs

描述: 股票指数(或者股票)历史行情数据, 支持自定义时间范围

限量: 单次返回具体某个股票指数(或者股票)指定时间范围内的历史行情数据

输入参数-历史行情数据

| 名称         | 类型  | 描述                                             |
|------------|-----|------------------------------------------------|
| symbol     | str | symbol="sh000001"                              |
| start_date | str | start_date=""; 开始日期, 格式 "YYYYMMDD", 为空则从最早日期开始 |
| end_date   | str | end_date=""; 结束日期, 格式 "YYYYMMDD", 为空则到当前（最新）日期 |

输出参数-历史行情数据

| 名称     | 类型      | 描述                  |
|--------|---------|---------------------|
| date   | object  | 腾讯的数据开始时间, 不是证券上市时间 |
| open   | float64 | -                   |
| close  | float64 | -                   |
| high   | float64 | -                   |
| low    | float64 | -                   |
| amount | float64 | 注意单位: 手             |

接口示例

```python
import akshare as ak

stock_zh_index_daily_tx_df = ak.stock_zh_index_daily_tx(symbol="sh000001", start_date="20260101", end_date="20260429")
print(stock_zh_index_daily_tx_df)
```

数据示例

```
          date     open    close     high      low       amount
0   2026-01-05  3986.97  4023.42  4025.26  3983.58  596950455.0
1   2026-01-06  4026.02  4083.67  4083.67  4025.09  702472270.0
2   2026-01-07  4083.84  4085.77  4098.78  4069.44  683384352.0
3   2026-01-08  4077.72  4082.98  4093.87  4067.12  666131337.0
4   2026-01-09  4086.76  4120.43  4121.72  4083.62  729837985.0
..         ...      ...      ...      ...      ...          ...
71  2026-04-23  4110.79  4093.25  4114.84  4070.46  671166092.0
72  2026-04-24  4081.03  4079.90  4092.61  4061.15  605031798.0
73  2026-04-27  4074.81  4086.34  4092.83  4071.08  589950867.0
74  2026-04-28  4076.14  4078.64  4090.20  4062.87  600507498.0
75  2026-04-29  4061.82  4107.51  4112.15  4061.82  614221451.0
[76 rows x 6 columns]
```
