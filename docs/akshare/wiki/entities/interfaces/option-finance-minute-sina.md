---
title: "option_finance_minute_sina - 期权行情分时数据-新浪"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, option, parameters, returns, example]
sources: [raw/data-dictionary/option/option.md]
confidence: high
---
# option_finance_minute_sina

- 分类: [[option-option|AKShare 期权数据]]
- 主题路径: AKShare 期权数据 > 金融期权-新浪 > 上交所 > 期权行情分时数据-新浪
- 描述: 新浪财经-金融期权-股票期权分时行情数据
- 目标地址: https://stock.finance.sina.com.cn/option/quotes.html
- 限量: 单次返回指定期权的分时行情数据
- 来源页面: https://akshare.akfamily.xyz/data/option/option.html

## 相关

- [[option-option|AKShare 期权数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 期权行情分时数据-新浪

接口: option_finance_minute_sina

目标地址: https://stock.finance.sina.com.cn/option/quotes.html

描述: 新浪财经-金融期权-股票期权分时行情数据

限量: 单次返回指定期权的分时行情数据

输入参数

| 名称     | 类型  | 描述                                                      |
|--------|-----|---------------------------------------------------------|
| symbol | str | symbol="10002530"; 通过 **ak.option_sse_codes_sina()** 获取 |

输出参数

| 名称            | 类型      | 描述  |
|---------------|---------|-----|
| date          | object  | -   |
| time          | object  | -   |
| price         | float64 | -   |
| average_price | float64 | -   |
| volume        | int64   | -   |

接口示例

```python
import akshare as ak

option_finance_minute_sina_df = ak.option_finance_minute_sina(symbol="10002415")
print(option_finance_minute_sina_df)
```

数据示例

```
            date      time   price average_price volume
0     2020-07-13  09:26:00  0.0000        0.0000      0
1     2020-07-13  09:27:00  0.0000        0.0000      0
2     2020-07-13  09:28:00  0.0000        0.0000      0
3     2020-07-13  09:29:00  0.0000        0.0000      0
4     2020-07-13  09:30:00  0.0000        0.0000      0
          ...       ...     ...           ...    ...
1219  2020-07-17  14:56:00  1.3699        1.3677      0
1220  2020-07-17  14:57:00  1.3699        1.3677      0
1221  2020-07-17  14:58:00  1.3699        1.3677      0
1222  2020-07-17  14:59:00  1.3699        1.3677      0
1223  2020-07-17  15:00:00  1.3757        1.3679      1
```
