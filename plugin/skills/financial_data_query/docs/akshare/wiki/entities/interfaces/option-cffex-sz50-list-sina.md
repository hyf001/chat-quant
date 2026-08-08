---
title: "option_cffex_sz50_list_sina - 上证50指数列表"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, option, parameters, returns, example]
sources: [raw/data-dictionary/option/option.md]
confidence: high
---
# option_cffex_sz50_list_sina

- 分类: [[option-option|AKShare 期权数据]]
- 主题路径: AKShare 期权数据 > 金融期权-新浪 > 中金所 > 上证50指数列表
- 描述: 中金所-上证50指数-所有合约, 返回的第一个合约为主力合约
- 目标地址: https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php/ho/cffex
- 限量: 单次返回所有合约
- 来源页面: https://akshare.akfamily.xyz/data/option/option.html

## 相关

- [[option-option|AKShare 期权数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 上证50指数列表

接口: option_cffex_sz50_list_sina

目标地址: https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php/ho/cffex

描述: 中金所-上证50指数-所有合约, 返回的第一个合约为主力合约

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

option_cffex_sz50_list_sina_df = ak.option_cffex_sz50_list_sina()
print(option_cffex_sz50_list_sina_df)
```

数据示例

```
{'上证50指数': ['ho2301', 'ho2303', 'ho2302', 'ho2306', 'ho2312', 'ho2309']}
```
