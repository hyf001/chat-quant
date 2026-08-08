---
title: "stock_zh_ah_name - A+H股票字典"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_zh_ah_name

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > A+H股 > A+H股票字典
- 描述: A+H 股数据是从腾讯财经获取的数据, 历史数据按日频率更新
- 目标地址: https://stockapp.finance.qq.com/mstats/#mod=list&id=hk_ah&module=HK&type=AH
- 限量: 单次返回所有 A+H 上市公司的代码和名称
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### A+H股票字典

接口: stock_zh_ah_name

目标地址: https://stockapp.finance.qq.com/mstats/#mod=list&id=hk_ah&module=HK&type=AH

描述: A+H 股数据是从腾讯财经获取的数据, 历史数据按日频率更新

限量: 单次返回所有 A+H 上市公司的代码和名称

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称  | 类型     | 描述  |
|-----|--------|-----|
| 代码  | object | -   |
| 名称  | object | -   |

接口示例

```python
import akshare as ak

stock_zh_ah_name_df = ak.stock_zh_ah_name()
print(stock_zh_ah_name_df)
```

数据示例

```
     代码        名称
0    01211     比亚迪股份
1    06160      百济神州
2    01880      中国中免
3    00941      中国移动
4    06821       凯莱英
..     ...       ...
144  01053    重庆钢铁股份
145  00588  北京北辰实业股份
146  02009      金隅集团
147  02880      辽港股份
148  01033     中石化油服
[149 rows x 2 columns]
```
