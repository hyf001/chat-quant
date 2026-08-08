---
title: "currency_currencies - 货币基础信息查询"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, currency, parameters, returns, example]
sources: [raw/data-dictionary/currency/currency.md]
confidence: high
---
# currency_currencies

- 分类: [[currency-currency|AKShare 货币数据]]
- 主题路径: AKShare 货币数据 > 货币基础信息查询
- 描述: 所有货币的基础信息
- 目标地址: https://currencyscoop.com/
- 限量: 单次返回指定所有货币基础信息
- 来源页面: https://akshare.akfamily.xyz/data/currency/currency.html

## 相关

- [[currency-currency|AKShare 货币数据]]
- [[_meta/topic-map]]

## 源文摘录

### 货币基础信息查询

接口: currency_currencies

注意：此接口使用外部 API, 免费账号每月限量访问 5000 次, 可以在 [currencyscoop](https://currencyscoop.com/) 注册

目标地址: https://currencyscoop.com/

描述: 所有货币的基础信息

限量: 单次返回指定所有货币基础信息

输入参数

| 名称      | 类型  | 描述                  |
|---------|-----|---------------------|
| c_type  | str | c_type="fiat"       |
| api_key | str | api_key="此处输入 API"; |

输出参数

| 名称                  | 类型     | 描述 |
|---------------------|--------|----|
| id                  | int64  | -  |
| name                | object | -  |
| short_code          | object | -  |
| code                | object | -  |
| precision           | int64  | -  |
| subunit             | int64  | -  |
| symbol              | object | -  |
| symbol_first        | bool   | -  |
| decimal_mark        | object | -  |
| thousands_separator | object | -  |

接口示例

```python
import akshare as ak

currency_currencies_df = ak.currency_currencies(c_type="fiat", api_key="此处输入 API")
print(currency_currencies_df)
```

数据示例

```
      id                           name  ... decimal_mark thousands_separator
0      1                     UAE Dirham  ...            .                   ,
1      2                        Afghani  ...            .                   ,
2      3                            Lek  ...            .                   ,
3      4                  Armenian Dram  ...            .                   ,
4      5  Netherlands Antillean Guilder  ...            ,                   .
..   ...                            ...  ...          ...                 ...
156  157                      CFP Franc  ...            .                   ,
157  158                    Yemeni Rial  ...            .                   ,
158  159                           Rand  ...            .                   ,
159  160                 Zambian Kwacha  ...            .                   ,
160  161                Zimbabwe Dollar  ...            .                   ,
[161 rows x 10 columns]
```
