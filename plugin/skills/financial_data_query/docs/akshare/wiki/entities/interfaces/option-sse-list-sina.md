---
title: "option_sse_list_sina - 合约到期月份列表"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, option, parameters, returns, example]
sources: [raw/data-dictionary/option/option.md]
confidence: high
---
# option_sse_list_sina

- 分类: [[option-option|AKShare 期权数据]]
- 主题路径: AKShare 期权数据 > 金融期权-新浪 > 上交所 > 合约到期月份列表
- 描述: 获取期权-上交所-50ETF-合约到期月份列表
- 目标地址: https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php
- 限量: 单次返回指定品种的到期月份列表
- 来源页面: https://akshare.akfamily.xyz/data/option/option.html

## 相关

- [[option-option|AKShare 期权数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 合约到期月份列表

接口: option_sse_list_sina

目标地址: https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php

描述: 获取期权-上交所-50ETF-合约到期月份列表

限量: 单次返回指定品种的到期月份列表

输入参数

| 名称       | 类型  | 描述                                  |
|----------|-----|-------------------------------------|
| symbol   | str | symbol="50ETF"; "50ETF" or "300ETF" |
| exchange | str | exchange="null"                     |

输出参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

接口示例

```python
import akshare as ak

option_sse_list_sina_df = ak.option_sse_list_sina(symbol="50ETF", exchange="null")
print(option_sse_list_sina_df)
```

数据示例

```
['202002', '202003', '202006', '202009']
```
