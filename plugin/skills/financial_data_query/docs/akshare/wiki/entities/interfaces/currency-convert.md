---
title: "currency_convert - 货币对价格转换"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, currency, parameters, returns, example]
sources: [raw/data-dictionary/currency/currency.md]
confidence: high
---
# currency_convert

- 分类: [[currency-currency|AKShare 货币数据]]
- 主题路径: AKShare 货币数据 > 货币对价格转换
- 描述: 指定货币对指定货币数量的转换后价格
- 目标地址: https://currencyscoop.com/
- 限量: 单次返回指定货币对的转换后价格
- 来源页面: https://akshare.akfamily.xyz/data/currency/currency.html

## 相关

- [[currency-currency|AKShare 货币数据]]
- [[_meta/topic-map]]

## 源文摘录

### 货币对价格转换

接口: currency_convert

注意：此接口使用外部 API, 免费账号每月限量访问 5000 次, 可以在 [currencyscoop](https://currencyscoop.com/) 注册

目标地址: https://currencyscoop.com/

描述: 指定货币对指定货币数量的转换后价格

限量: 单次返回指定货币对的转换后价格

输入参数

| 名称      | 类型  | 描述                  |
|---------|-----|---------------------|
| base    | str | base="USD"; 基础货币    |
| to      | str | to="CNY"; 需要转换到的货币  |
| amount  | str | amount="10000"; 转换量 |
| api_key | str | api_key="此处输入 API"; |

输出参数

| 名称    | 类型     | 描述 |
|-------|--------|----|
| item  | object | -  |
| value | object | -  |

接口示例

```python
import akshare as ak

currency_convert_df = ak.currency_convert(base="USD", to="CNY", amount="10000", api_key="此处输入 API")
print(currency_convert_df)
```

数据示例

```
        item                value
0  timestamp  2023-07-24 11:31:20
1       date           2023-07-24
2       from                  USD
3         to                  CNY
4     amount                10000
5      value            71898.995
```
