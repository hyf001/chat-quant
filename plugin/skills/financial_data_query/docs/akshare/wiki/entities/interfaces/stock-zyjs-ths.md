---
title: "stock_zyjs_ths - 主营介绍-同花顺"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_zyjs_ths

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 主营介绍-同花顺
- 描述: 同花顺-主营介绍
- 目标地址: https://basic.10jqka.com.cn/new/000066/operate.html
- 限量: 单次返回所有数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

### 主营介绍-同花顺

接口: stock_zyjs_ths

目标地址: https://basic.10jqka.com.cn/new/000066/operate.html

描述: 同花顺-主营介绍

限量: 单次返回所有数据

输入参数

| 名称     | 类型  | 描述              |
|--------|-----|-----------------|
| symbol | str | symbol="000066" |

输出参数

| 名称   | 类型      | 描述      |
|------|---------|---------|
| 股票代码 | object  | -       |
| 主营业务 | object  | -       |
| 产品类型 | object  | -       |
| 产品名称 | object  | -       |
| 经营范围 | object  | -       |

接口示例

```python
import akshare as ak

stock_zyjs_ths_df = ak.stock_zyjs_ths(symbol="000066")
print(stock_zyjs_ths_df)
```

数据示例

```
     股票代码  ...                                               经营范围
0  000066  ...  计算机软件、硬件、终端及其外部设备、网络系统及系统集成、电子产品及零部件、金融机具、税控机具...
[1 rows x 5 columns]
```
