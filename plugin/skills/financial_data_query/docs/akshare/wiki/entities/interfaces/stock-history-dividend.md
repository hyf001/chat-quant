---
title: "stock_history_dividend - 历史分红"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_history_dividend

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 历史分红
- 描述: 新浪财经-发行与分配-历史分红
- 目标地址: http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/lsfh/index.phtml
- 限量: 单次获取所有股票的历史分红数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 历史分红

接口: stock_history_dividend

目标地址: http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/lsfh/index.phtml

描述: 新浪财经-发行与分配-历史分红

限量: 单次获取所有股票的历史分红数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称   | 类型      | 描述      |
|------|---------|---------|
| 代码   | object  | -       |
| 名称   | object  | -       |
| 上市日期 | object  | -       |
| 累计股息 | float64 | 注意单位: % |
| 年均股息 | float64 | 注意单位: % |
| 分红次数 | float64 | -       |
| 融资总额 | float64 | 注意单位: 亿 |
| 融资次数 | float64 | -       |

接口示例

```python
import akshare as ak

stock_history_dividend_df = ak.stock_history_dividend()
print(stock_history_dividend_df)
```

数据示例

```
     代码      名称     上市日期   累计股息  年均股息 分红次数 融资总额 融资次数
0     000550  江铃汽车  1993-12-01  213.0  6.87    51   0.0000     0
1     000541  佛山照明  1993-11-23  192.0  6.19    56  10.8842     1
2     000429  粤高速A  1998-02-20  171.4  6.35    50  16.3350     1
3     000726   鲁泰A  2000-12-25  143.9  6.00    47   9.5082     1
4     000581  威孚高科  1998-09-24  143.1  5.50    48  28.5012     1
...      ...   ...         ...    ...   ...   ...      ...   ...
5556  920002  万达轴承  2024-05-30    0.0  0.00     0   1.0235     1
5557  920008  成电光信  2024-08-29    0.0  0.00     0   0.8949     1
5558  920016  中草香料  2024-09-13    0.0  0.00     0   1.1465     1
5559  920099  瑞华技术  2024-09-25    0.0  0.00     0   0.0000     0
5560  920118  太湖远大  2024-08-22    0.0  0.00     0   0.0000     0
[5561 rows x 8 columns]
```
