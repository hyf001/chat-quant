---
title: "forex_hist_em - 历史行情数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fx, parameters, returns, example]
sources: [raw/data-dictionary/fx/fx.md]
confidence: high
---
# forex_hist_em

- 分类: [[fx-fx|AKShare 外汇数据]]
- 主题路径: AKShare 外汇数据 > 历史行情数据
- 描述: 东方财富网-行情中心-外汇市场-所有汇率-历史行情数据
- 目标地址: https://quote.eastmoney.com/cnyrate/EURCNYC.html
- 限量: 单次返回指定 symbol 的历史行情数据
- 来源页面: https://akshare.akfamily.xyz/data/fx/fx.html

## 相关

- [[fx-fx|AKShare 外汇数据]]
- [[_meta/topic-map]]

## 源文摘录

### 历史行情数据

接口: forex_hist_em

目标地址: https://quote.eastmoney.com/cnyrate/EURCNYC.html

描述: 东方财富网-行情中心-外汇市场-所有汇率-历史行情数据

限量: 单次返回指定 symbol 的历史行情数据

输入参数

| 名称     | 类型  | 描述                                                                |
|--------|-----|-------------------------------------------------------------------|
| symbol | str | symbol="USDCNH"; 品种代码；可以通过 ak.forex_spot_em() 来获取所有可获取历史行情数据的品种代码 |

输出参数

| 名称  | 类型      | 描述 |
|-----|---------|----|
| 序号  | int64   | -  |
| 代码  | object  | -  |
| 名称  | object  | -  |
| 最新价 | float64 | -  |
| 涨跌额 | float64 | -  |
| 涨跌幅 | float64 | -  |
| 今开  | float64 | -  |
| 最高  | float64 | -  |
| 最低  | float64 | -  |
| 昨收  | float64 | -  |

接口示例

```python
import akshare as ak

forex_hist_em_df = ak.forex_hist_em(symbol="USDCNH")
print(forex_hist_em_df)
```

数据示例

```
         日期      代码        名称      今开     最新价      最高      最低    振幅
0     2010-08-23  USDCNH  美元兑离岸人民币  6.7200  6.7250  6.7250  6.7200  0.00
1     2010-08-24  USDCNH  美元兑离岸人民币  6.7230  6.7265  6.7265  6.7230  0.05
2     2010-08-25  USDCNH  美元兑离岸人民币  6.7325  6.7325  6.7325  6.7325  0.00
3     2010-08-26  USDCNH  美元兑离岸人民币  6.7500  6.7450  6.7500  6.7450  0.07
4     2010-08-27  USDCNH  美元兑离岸人民币  6.7530  6.7530  6.7530  6.7530  0.00
...          ...     ...       ...     ...     ...     ...     ...   ...
3776  2025-02-28  USDCNH  美元兑离岸人民币  7.3007  7.2954  7.3019  7.2844  0.24
3777  2025-03-03  USDCNH  美元兑离岸人民币  7.2915  7.3027  7.3069  7.2848  0.30
3778  2025-03-04  USDCNH  美元兑离岸人民币  7.3028  7.2543  7.3069  7.2488  0.80
3779  2025-03-05  USDCNH  美元兑离岸人民币  7.2532  7.2362  7.2769  7.2343  0.59
3780  2025-03-06  USDCNH  美元兑离岸人民币  7.2363  7.2484  7.2485  7.2354  0.18
[3781 rows x 8 columns]
```
