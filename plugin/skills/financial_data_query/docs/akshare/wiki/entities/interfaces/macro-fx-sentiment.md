---
title: "macro_fx_sentiment - 货币对-投机情绪报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fx, parameters, returns, example]
sources: [raw/data-dictionary/fx/fx.md]
confidence: high
---
# macro_fx_sentiment

- 分类: [[fx-fx|AKShare 外汇数据]]
- 主题路径: AKShare 外汇数据 > 货币对-投机情绪报告
- 描述: 货币对-投机情绪报告
- 目标地址: https://datacenter.jin10.com/reportType/dc_ssi_trends
- 限量: 单次返回指定日期所有品种的数据(所指定的日期必须在当前交易日之前的30个交易日内)
- 来源页面: https://akshare.akfamily.xyz/data/fx/fx.html

## 相关

- [[fx-fx|AKShare 外汇数据]]
- [[_meta/topic-map]]

## 源文摘录

### 货币对-投机情绪报告

接口: macro_fx_sentiment

目标地址: https://datacenter.jin10.com/reportType/dc_ssi_trends

描述: 货币对-投机情绪报告

限量: 单次返回指定日期所有品种的数据(所指定的日期必须在当前交易日之前的30个交易日内)

输入参数

| 名称         | 类型  | 描述                                                |
|------------|-----|---------------------------------------------------|
| start_date | str | start_date="2020-04-07"; 所指定的日期必须在当前交易日之前的30个交易日内 |
| end_date   | str | end_date="2020-04-07"; 与 start_date 一致            |

输出参数

| 名称     | 类型      | 描述     |
|--------|---------|--------|
| date   | object  | 间隔10分钟 |
| AUDJPY | float64 | -      |
| AUDUSD | float64 | -      |
| EURAUD | float64 | -      |
| EURJPY | float64 | -      |
| EURUSD | float64 | -      |
| GBPJPY | float64 | -      |
| GBPUSD | float64 | -      |
| NZDUSD | float64 | -      |
| USDCAD | float64 | -      |
| USDCHF | float64 | -      |
| USDJPY | float64 | -      |
| USDX   | float64 | -      |
| XAUUSD | float64 | -      |

接口示例

```python
import akshare as ak
from datetime import datetime

test_date = datetime.now().date().isoformat().replace("-", "")
macro_fx_sentiment_df = ak.macro_fx_sentiment(start_date=test_date, end_date=test_date)
print(macro_fx_sentiment_df)
```

数据示例

```
                 date  AUDJPY  AUDUSD  EURAUD  ...  USDCHF  USDJPY   USDX  XAUUSD
0    2022-10-11 00:00   52.45   72.53   44.73  ...   39.59   33.90  37.00   72.38
1    2022-10-11 00:10   52.46   72.47   44.85  ...   39.10   33.78  36.49   72.43
2    2022-10-11 00:20   52.48   72.23   45.37  ...   39.10   33.88  36.48   72.75
3    2022-10-11 00:30   52.38   72.34   44.71  ...   38.90   33.73  36.34   72.83
4    2022-10-11 00:40   52.31   72.48   44.44  ...   38.80   33.61  36.23   72.82
..                ...     ...     ...     ...  ...     ...     ...    ...     ...
962  2022-10-17 19:30   54.86   68.14   36.53  ...   42.80   30.48  39.77   60.45
963  2022-10-17 19:40   54.43   67.81   37.01  ...   43.54   30.83  39.82   60.73
964  2022-10-17 19:50   54.39   68.46   36.92  ...   43.38   30.75  39.72   60.77
965  2022-10-17 20:00   54.10   68.05   38.01  ...   44.05   30.88  39.49   61.36
966  2022-10-17 20:10   55.51   67.39   36.80  ...   42.82   30.95  39.78   59.70
```
