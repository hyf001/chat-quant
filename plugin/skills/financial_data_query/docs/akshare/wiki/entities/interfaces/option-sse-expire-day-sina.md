---
title: "option_sse_expire_day_sina - 合约到期月份列表"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, option, parameters, returns, example]
sources: [raw/data-dictionary/option/option.md]
confidence: high
---
# option_sse_expire_day_sina

- 分类: [[option-option|AKShare 期权数据]]
- 主题路径: AKShare 期权数据 > 金融期权-新浪 > 上交所 > 合约到期月份列表
- 描述: 获取指定到期月份指定品种的剩余到期时间
- 目标地址: https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php
- 限量: 单次返回指定品种的品种的剩余到期时间
- 来源页面: https://akshare.akfamily.xyz/data/option/option.html

## 相关

- [[option-option|AKShare 期权数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 合约到期月份列表

接口: option_sse_expire_day_sina

目标地址: https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php

描述: 获取指定到期月份指定品种的剩余到期时间

限量: 单次返回指定品种的品种的剩余到期时间

输入参数

| 名称         | 类型  | 描述                                  |
|------------|-----|-------------------------------------|
| trade_date | str | trade_date="202002";                |
| symbol     | str | symbol="50ETF"; "50ETF" or "300ETF" |
| exchange   | str | exchange="null"                     |

输出参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

接口示例

```python
import akshare as ak

option_sse_expire_day_sina_df = ak.option_sse_expire_day_sina(trade_date="202002", symbol="50ETF", exchange="null")
print(option_sse_expire_day_sina_df)
```

数据示例

```
('2020-02-26', 3)
```
