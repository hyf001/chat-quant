---
title: "option_sse_minute_sina - 期权行情分钟数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, option, parameters, returns, example]
sources: [raw/data-dictionary/option/option.md]
confidence: high
---
# option_sse_minute_sina

- 分类: [[option-option|AKShare 期权数据]]
- 主题路径: AKShare 期权数据 > 金融期权-新浪 > 上交所 > 期权行情分钟数据
- 描述: 期权行情分钟数据, 只能返还当天的分钟数据
- 目标地址: https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php
- 限量: 单次返回期权行情分钟数据
- 来源页面: https://akshare.akfamily.xyz/data/option/option.html

## 相关

- [[option-option|AKShare 期权数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 期权行情分钟数据

接口: option_sse_minute_sina

目标地址: https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php

描述: 期权行情分钟数据, 只能返还当天的分钟数据

限量: 单次返回期权行情分钟数据

输入参数

| 名称     | 类型  | 描述                |
|--------|-----|-------------------|
| symbol | str | symbol="10002273" |

输出参数

| 名称  | 类型      | 描述    |
|-----|---------|-------|
| 日期  | object  | 当前交易日 |
| 时间  | object  | -     |
| 价格  | float64 | -     |
| 成交  | int64   | -     |
| 持仓  | int64   | -     |
| 均价  | float64 | -     |

接口示例

```python
import akshare as ak

option_sse_minute_sina_df = ak.option_sse_minute_sina(symbol="10003720")
print(option_sse_minute_sina_df)
```

数据示例

```
      日期        时间      价格  成交     持仓      均价
0    2022-01-21  09:26:00  0.0000   0      0  0.0000
1    2022-01-21  09:27:00  0.0000   0      0  0.0000
2    2022-01-21  09:28:00  0.0000   0      0  0.0000
3    2022-01-21  09:29:00  0.0000   0      0  0.0000
4    2022-01-21  09:30:00  0.0011  14  32758  0.0011
..          ...       ...     ...  ..    ...     ...
330  2022-01-21  14:56:00  0.0009  40  31816  0.0010
331  2022-01-21  14:57:00  0.0008   0  31866  0.0010
332  2022-01-21  14:58:00  0.0008   0      0  0.0010
333  2022-01-21  14:59:00  0.0008   0      0  0.0010
334  2022-01-21  15:00:00  0.0008   0  31866  0.0010
```
