---
title: "currency_latest - 货币报价最新数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, currency, parameters, returns, example]
sources: [raw/data-dictionary/currency/currency.md]
confidence: high
---
# currency_latest

- 分类: [[currency-currency|AKShare 货币数据]]
- 主题路径: AKShare 货币数据 > 货币报价最新数据
- 描述: 货币报价最新数据
- 目标地址: https://currencyscoop.com/
- 限量: 单次返回指定货币的最新报价数据
- 来源页面: https://akshare.akfamily.xyz/data/currency/currency.html

## 相关

- [[currency-currency|AKShare 货币数据]]
- [[_meta/topic-map]]

## 源文摘录

### 货币报价最新数据

接口: currency_latest

注意：此接口使用外部 API, 免费账号每月限量访问 5000 次, 可以在 [currencyscoop](https://currencyscoop.com/) 注册

目标地址: https://currencyscoop.com/

描述: 货币报价最新数据

限量: 单次返回指定货币的最新报价数据

输入参数

| 名称      | 类型  | 描述                                                                                                          |
|---------|-----|-------------------------------------------------------------------------------------------------------------|
| base    | str | base="USD"                                                                                                  |
| symbols | str | symbols=""; 默认返回全部, 可以在此处设置 symbols="AUD", 则返回 AUD 的数据; 可以在此处设置 symbols: str = "AUD,CNY", 则返回 AUD 和 CNY 的数据 |
| api_key | str | api_key="此处输入 API";                                                                                         |

更多相关参数可以访问: https://currencybeacon.com/api-documentation 和 https://currencybeacon.com/supported-currencies

输出参数

| 名称       | 类型                  | 描述        |
|----------|---------------------|-----------|
| currency | object              | 货币代码      |
| date     | datetime64[ns, UTC] | 日期时间-注意时区 |
| base     | object              | 货币        |
| rates    | float64             | 比率        |

接口示例

```python
import akshare as ak

currency_latest_df = ak.currency_latest(base="USD", symbols="", api_key="此处输入 API")
print(currency_latest_df)
```

数据示例

```
    currency                      date base         rates
0        ADA 2023-07-24 10:56:21+00:00  USD      3.213363
1        AED 2023-07-24 10:56:21+00:00  USD      3.672500
2        AFN 2023-07-24 10:56:21+00:00  USD     85.665822
3        ALL 2023-07-24 10:56:21+00:00  USD     91.125190
4        AMD 2023-07-24 10:56:21+00:00  USD    387.300314
..       ...                       ...  ...           ...
215      ZAR 2023-07-24 10:56:21+00:00  USD     17.927659
216      ZMK 2023-07-24 10:56:21+00:00  USD  19493.346892
217      ZMW 2023-07-24 10:56:21+00:00  USD     19.493347
218      ZWD 2023-07-24 10:56:21+00:00  USD    361.900000
219      ZWL 2023-07-24 10:56:21+00:00  USD   4677.170339
[220 rows x 4 columns]
```
