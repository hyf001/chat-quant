---
title: "option_commodity_contract_sina - 当前合约"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, option, parameters, returns, example]
sources: [raw/data-dictionary/option/option.md]
confidence: high
---
# option_commodity_contract_sina

- 分类: [[option-option|AKShare 期权数据]]
- 主题路径: AKShare 期权数据 > 商品期权-新浪 > 当前合约
- 描述: 新浪财经-商品期权当前在交易的合约
- 目标地址: https://stock.finance.sina.com.cn/futures/view/optionsDP.php
- 限量: 单次返回指定 symbol 的所有合约数据
- 来源页面: https://akshare.akfamily.xyz/data/option/option.html

## 相关

- [[option-option|AKShare 期权数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 当前合约

接口: option_commodity_contract_sina

目标地址: https://stock.finance.sina.com.cn/futures/view/optionsDP.php

描述: 新浪财经-商品期权当前在交易的合约

限量: 单次返回指定 symbol 的所有合约数据

输入参数

| 名称     | 类型  | 描述            |
|--------|-----|---------------|
| symbol | str | symbol="玉米期权" |

输出参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| 序号  | str | -   |
| 合约  | str | -   |

接口示例

```python
import akshare as ak

option_commodity_contract_sina_df = ak.option_commodity_contract_sina(symbol="黄金期权")
print(option_commodity_contract_sina_df)
```

数据示例

```
   序号   合约
0   1  au2204
1   2  au2202
2   3  au2206
3   4  au2203
```
