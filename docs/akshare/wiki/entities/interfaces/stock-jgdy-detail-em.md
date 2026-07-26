---
title: "stock_jgdy_detail_em - 机构调研-详细"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_jgdy_detail_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 机构调研 > 机构调研-详细
- 描述: 东方财富网-数据中心-特色数据-机构调研-机构调研详细
- 目标地址: http://data.eastmoney.com/jgdy/xx.html
- 限量: 单次所有历史数据, 由于数据量比较大需要等待一定时间
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 机构调研-详细

接口: stock_jgdy_detail_em

目标地址: http://data.eastmoney.com/jgdy/xx.html

描述: 东方财富网-数据中心-特色数据-机构调研-机构调研详细

限量: 单次所有历史数据, 由于数据量比较大需要等待一定时间

输入参数

| 名称   | 类型  | 描述                       |
|------|-----|--------------------------|
| date | str | date="20241211"; 开始查询的时间 |

输出参数

| 名称   | 类型      | 描述      |
|------|---------|---------|
| 序号   | int64   | -       |
| 代码   | object  | -       |
| 名称   | object  | -       |
| 最新价  | float64 | -       |
| 涨跌幅  | float64 | 注意单位: % |
| 调研机构 | object  | -       |
| 机构类型 | object  | -       |
| 调研人员 | object  | -       |
| 接待方式 | object  | -       |
| 接待人员 | object  | -       |
| 接待地点 | object  | -       |
| 调研日期 | object  | -       |
| 公告日期 | object  | -       |

接口示例

```python
import akshare as ak

stock_jgdy_detail_em_df = ak.stock_jgdy_detail_em(date="20241211")
print(stock_jgdy_detail_em_df)
```

数据示例

```
   序号   代码    名称  ...     接待地点      调研日期      公告日期
0   1  002024  ST易购  ...     武汉中南店  2024-12-12  2024-12-12
1   2  002024  ST易购  ...     武汉中南店  2024-12-12  2024-12-12
2   3  002521  齐峰新材  ...     公司接待室  2024-12-12  2024-12-12
3   4  002521  齐峰新材  ...     公司接待室  2024-12-12  2024-12-12
4   5  301390  经纬股份  ...        公司  2024-12-12  2024-12-12
5   6  600030  中信证券  ...  北京中信证券大厦  2024-12-12  2024-12-12
6   7  600030  中信证券  ...  北京中信证券大厦  2024-12-12  2024-12-12
7   8  688528  秦川物联  ...    上证路演中心  2024-12-12  2024-12-12
[8 rows x 13 columns]
```
