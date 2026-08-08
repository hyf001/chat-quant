---
title: "futures_global_hist_em - 外盘-历史行情数据-东财"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, futures, parameters, returns, example]
sources: [raw/data-dictionary/futures/futures.md]
confidence: high
---
# futures_global_hist_em

- 分类: [[futures-futures|AKShare 期货数据]]
- 主题路径: 此处的合约需要是近期的合约, 否则会报错 > 外盘-历史行情数据-东财
- 描述: 东方财富网-行情中心-期货市场-国际期货-历史行情数据
- 目标地址: https://quote.eastmoney.com/globalfuture/HG25J.html
- 限量: 单次返回指定品种的历史数据
- 来源页面: https://akshare.akfamily.xyz/data/futures/futures.html

## 相关

- [[futures-futures|AKShare 期货数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 外盘-历史行情数据-东财

接口: futures_global_hist_em

目标地址: https://quote.eastmoney.com/globalfuture/HG25J.html

描述: 东方财富网-行情中心-期货市场-国际期货-历史行情数据

限量: 单次返回指定品种的历史数据

输入参数

| 名称     | 类型  | 描述                                                                        |
|--------|-----|---------------------------------------------------------------------------|
| symbol | str | symbol="HG00Y"; 品种代码；可以通过 ak.futures_global_spot_em() 来获取所有可获取历史行情数据的品种代码 |

输出参数

| 名称  | 类型      | 描述      |
|-----|---------|---------|
| 日期  | object  | -       |
| 代码  | object  | -       |
| 名称  | object  | -       |
| 开盘  | float64 | -       |
| 最新价 | float64 | -       |
| 最高  | float64 | -       |
| 最低  | float64 | -       |
| 总量  | int64   | -       |
| 涨幅  | float64 | 注意单位: % |
| 持仓  | object  | -       |
| 日增  | int64   | -       |

接口示例

```python
import akshare as ak

futures_global_hist_em_df = ak.futures_global_hist_em(symbol="HG00Y")
print(futures_global_hist_em_df)
```

数据示例

```
         日期     代码      名称     开盘  ...     总量    涨幅      持仓      日增
0     2011-07-15  HG00Y  COMEX铜  4.3740  ...      1  0.00       0           0
1     2011-07-21  HG00Y  COMEX铜  4.4330  ...      2  1.35       0           0
2     2011-07-29  HG00Y  COMEX铜  4.4580  ...    114  1.04       0           0
3     2011-08-03  HG00Y  COMEX铜  4.3600  ...    167 -3.42       0           0
4     2011-08-12  HG00Y  COMEX铜  4.0240  ...      6 -7.49       0           0
...          ...    ...     ...     ...  ...    ...   ...     ...         ...
3480  2025-02-27  HG00Y  COMEX铜  4.5835  ...  50367  0.17  122084        1306
3481  2025-02-28  HG00Y  COMEX铜  4.5955  ...  42115 -1.19  123553        1469
3482  2025-03-03  HG00Y  COMEX铜  4.5765  ...  48192  0.93  122627  4294966370
3483  2025-03-04  HG00Y  COMEX铜  4.5880  ...  47016 -0.56  122610  4294967279
3484  2025-03-05  HG00Y  COMEX铜  4.5800  ...  57782  5.25  123815        1205
[3485 rows x 11 columns]
```
