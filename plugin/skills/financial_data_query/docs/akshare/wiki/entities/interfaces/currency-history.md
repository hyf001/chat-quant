---
title: "currency_history - 货币报价历史数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, currency, parameters, returns, example]
sources: [raw/data-dictionary/currency/currency.md]
confidence: high
---
# currency_history

- 分类: [[currency-currency|AKShare 货币数据]]
- 主题路径: AKShare 货币数据 > 货币报价历史数据
- 描述: 货币报价历史数据
- 目标地址: https://currencyscoop.com/
- 限量: 单次返回指定货币在指定交易日的报价历史数据-免费账号每月限量访问 5000 次
- 来源页面: https://akshare.akfamily.xyz/data/currency/currency.html

## 相关

- [[currency-currency|AKShare 货币数据]]
- [[_meta/topic-map]]

## 源文摘录

### 货币报价历史数据

接口: currency_history

注意：此接口使用外部 API, 免费账号每月限量访问 5000 次, 可以在 [currencyscoop](https://currencyscoop.com/) 注册

目标地址: https://currencyscoop.com/

描述: 货币报价历史数据

限量: 单次返回指定货币在指定交易日的报价历史数据-免费账号每月限量访问 5000 次

输入参数

| 名称      | 类型  | 描述                                                                                                          |
|---------|-----|-------------------------------------------------------------------------------------------------------------|
| base    | str | base="USD"                                                                                                  |
| date    | str | date="2023-02-03"                                                                                           |
| symbols | str | symbols=""; 默认返回全部, 可以在此处设置 symbols="AUD", 则返回 AUD 的数据; 可以在此处设置 symbols: str = "AUD,CNY", 则返回 AUD 和 CNY 的数据 |
| api_key | str | api_key="此处输入 API";                                                                                         |

输出参数

| 名称       | 类型      | 描述   |
|----------|---------|------|
| currency | object  | 货币代码 |
| date     | object  | 日期   |
| base     | float64 | 货币   |
| rates    | float64 | 比率   |

接口示例

```python
import akshare as ak

currency_history_df = ak.currency_history(base="USD", date="2023-02-03", symbols="", api_key="此处输入 API")
print(currency_history_df)
```

数据示例

```
    currency       date base         rates
0        ADA 2023-02-03  USD      2.501764
1        AED 2023-02-03  USD      3.672500
2        AFN 2023-02-03  USD     89.667343
3        ALL 2023-02-03  USD    107.092799
4        AMD 2023-02-03  USD    395.155660
..       ...        ...  ...           ...
215      ZAR 2023-02-03  USD     17.470971
216      ZMK 2023-02-03  USD  19217.069221
217      ZMW 2023-02-03  USD     19.217069
218      ZWD 2023-02-03  USD    361.900000
219      ZWL 2023-02-03  USD    804.930876
[220 rows x 4 columns]
```
