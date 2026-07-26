---
title: "option_cffex_zz1000_list_sina - 中证1000指数列表"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, option, parameters, returns, example]
sources: [raw/data-dictionary/option/option.md]
confidence: high
---
# option_cffex_zz1000_list_sina

- 分类: [[option-option|AKShare 期权数据]]
- 主题路径: AKShare 期权数据 > 金融期权-新浪 > 中金所 > 中证1000指数列表
- 描述: 中金所-中证1000指数-所有合约, 返回的第一个合约为主力合约
- 目标地址: https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php
- 限量: 单次返回所有合约
- 来源页面: https://akshare.akfamily.xyz/data/option/option.html

## 相关

- [[option-option|AKShare 期权数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 中证1000指数列表

接口: option_cffex_zz1000_list_sina

目标地址: https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php

描述: 中金所-中证1000指数-所有合约, 返回的第一个合约为主力合约

限量: 单次返回所有合约

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

接口示例

```python
import akshare as ak

option_cffex_zz1000_list_sina_df = ak.option_cffex_zz1000_list_sina()
print(option_cffex_zz1000_list_sina_df)
```

数据示例

```
{'中证1000指数': ['mo2208', 'mo2209', 'mo2212', 'mo2210', 'mo2306', 'mo2303']}
```
