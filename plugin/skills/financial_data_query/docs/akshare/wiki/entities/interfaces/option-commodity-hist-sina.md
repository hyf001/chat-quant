---
title: "option_commodity_hist_sina - 历史行情"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, option, parameters, returns, example]
sources: [raw/data-dictionary/option/option.md]
confidence: high
---
# option_commodity_hist_sina

- 分类: [[option-option|AKShare 期权数据]]
- 主题路径: AKShare 期权数据 > 商品期权-新浪 > 历史行情
- 描述: 新浪财经-商品期权的历史行情数据-日频率
- 目标地址: https://stock.finance.sina.com.cn/futures/view/optionsDP.php
- 限量: 单次返回指定合约的历史行情数据
- 来源页面: https://akshare.akfamily.xyz/data/option/option.html

## 相关

- [[option-option|AKShare 期权数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 历史行情

接口: option_commodity_hist_sina

目标地址: https://stock.finance.sina.com.cn/futures/view/optionsDP.php

描述: 新浪财经-商品期权的历史行情数据-日频率

限量: 单次返回指定合约的历史行情数据

输入参数

| 名称     | 类型  | 描述                                                                           |
|--------|-----|------------------------------------------------------------------------------|
| symbol | str | symbol="au2012C328"; 可以通过 ak.option_commodity_contract_table_sina() 获取具体合约代码 |

输出参数

| 名称     | 类型      | 描述  |
|--------|---------|-----|
| date   | object  | -   |
| open   | float64 | -   |
| high   | float64 | -   |
| low    | float64 | -   |
| close  | float64 | -   |
| volume | int64   | -   |

接口示例

```python
import akshare as ak

option_commodity_hist_sina_df = ak.option_commodity_hist_sina(symbol="au2012C328")
print(option_commodity_hist_sina_df)
```

数据示例

```
         date     open     high      low    close volume
0  2019-12-20   0.0000   0.0000   0.0000  22.9200      0
1  2019-12-23   0.0000   0.0000   0.0000  25.9000      0
2  2019-12-24  25.0600  25.0600  25.0600  25.0600      2
3  2019-12-25  27.8400  27.8400  23.4400  27.2000     12
4  2020-01-07  38.1800  38.1800  38.1800  38.1800      1
5  2020-02-11  40.2200  40.2200  35.6000  35.6000      2
6  2020-03-16  33.2800  33.2800  33.2800  33.2800      2
7  2020-03-24  46.0400  46.0400  46.0400  46.0400      1
8  2020-05-07  58.3200  58.3200  57.1400  58.2200      3
```
