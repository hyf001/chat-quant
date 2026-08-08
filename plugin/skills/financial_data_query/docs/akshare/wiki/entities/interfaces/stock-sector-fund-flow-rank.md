---
title: "stock_sector_fund_flow_rank - 板块资金流排名"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_sector_fund_flow_rank

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 资金流向 > 东方财富 > 板块资金流排名
- 描述: 东方财富网-数据中心-资金流向-板块资金流-排名
- 目标地址: https://data.eastmoney.com/bkzj/hy.html
- 限量: 单次获取指定板块的指定期限的资金流排名数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 板块资金流排名

接口: stock_sector_fund_flow_rank

目标地址: https://data.eastmoney.com/bkzj/hy.html

描述: 东方财富网-数据中心-资金流向-板块资金流-排名

限量: 单次获取指定板块的指定期限的资金流排名数据

说明: 若东财对新上线板块返回 `-`，相关数值列将转换为 `NaN`，调用方可按需过滤

输入参数

| 名称          | 类型  | 描述                                                         |
|-------------|-----|------------------------------------------------------------|
| indicator   | str | indicator="今日"; choice of {"今日", "5日", "10日"}              |
| sector_type | str | sector_type="行业资金流"; choice of {"行业资金流", "概念资金流", "地域资金流"} |

输出参数-行业资金流-今日

| 名称         | 类型      | 描述      |
|------------|---------|---------|
| 序号         | int64   | -       |
| 名称         | object  | -       |
| 今日涨跌幅      | float64 | 注意单位: % |
| 主力净流入-净额   | float64 | -       |
| 主力净流入-净占比  | float64 | 注意单位: % |
| 超大单净流入-净额  | float64 | -       |
| 超大单净流入-净占比 | float64 | 注意单位: % |
| 大单净流入-净额   | float64 | -       |
| 大单净流入-净占比  | float64 | 注意单位: % |
| 中单净流入-净额   | float64 | -       |
| 中单净流入-净占比  | float64 | 注意单位: % |
| 小单净流入-净额   | float64 | -       |
| 小单净流入-净占比  | float64 | 注意单位: % |
| 主力净流入最大股   | object  | -       |

接口示例-行业资金流-今日

```python
import akshare as ak

stock_sector_fund_flow_rank_df = ak.stock_sector_fund_flow_rank(indicator="今日", sector_type="行业资金流")
print(stock_sector_fund_flow_rank_df)
```

数据示例-行业资金流-今日

```
    序号   名称  今日涨跌幅  ... 今日小单净流入-净额  今日小单净流入-净占比  今日主力净流入最大股
0    1    小金属   2.36  ... -9.101186e+08        -6.32        中国稀土
1    2   有色金属   1.96  ... -1.032419e+09        -5.49        铜陵有色
2    3    贵金属   3.94  ... -4.187458e+08        -4.25        紫金矿业
3    4   交运设备   4.51  ... -2.841601e+08        -3.35        中国通号
4    5   钢铁行业   1.69  ... -3.279502e+08        -3.82        包钢股份
..  ..    ...    ...  ...           ...          ...         ...
81  82   文化传媒  -2.23  ...  2.344617e+09         7.19         人民网
82  83    半导体  -2.20  ...  2.329264e+09         5.38        富创精密
83  84  互联网服务  -2.39  ...  3.482296e+09         7.76        荣联科技
84  85   软件开发  -2.82  ...  3.012122e+09         6.56        云赛智联
85  86   通信设备  -2.24  ...  3.339649e+09         7.95        精伦电子
[86 rows x 14 columns]
```
