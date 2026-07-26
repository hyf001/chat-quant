---
title: "stock_yzxdr_em - 一致行动人"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_yzxdr_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 一致行动人
- 描述: 东方财富网-数据中心-特色数据-一致行动人
- 目标地址: http://data.eastmoney.com/yzxdr/
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

### 一致行动人

接口: stock_yzxdr_em

目标地址: http://data.eastmoney.com/yzxdr/

描述: 东方财富网-数据中心-特色数据-一致行动人

限量: 单次返回所有历史数据

输入参数

| 名称   | 类型  | 描述                         |
|------|-----|----------------------------|
| date | str | date="20200930"; 每年的季度末时间点 |

输出参数

| 名称     | 类型      | 描述      |
|--------|---------|---------|
| 序号     | int64   | -       |
| 股票代码   | object  | -       |
| 股票简称   | object  | -       |
| 一致行动人  | object  | -       |
| 股东排名   | object  | -       |
| 持股数量   | int64   | -       |
| 持股比例   | float64 | -       |
| 持股数量变动 | object  | 注意单位: % |
| 行业     | object  | -       |
| 公告日期   | object  | -       |

接口示例

```python
import akshare as ak

stock_yzxdr_em_df = ak.stock_yzxdr_em(date="20210331")
print(stock_yzxdr_em_df)
```

数据示例

```
      序号    股票代码  股票简称  ... 持股数量变动     行业        公告日期
0        1  688981  中芯国际  ...    NaN    半导体  2024-11-08
1        2  688981  中芯国际  ...    NaN    半导体  2024-11-08
2        3  688981  中芯国际  ...    NaN    半导体  2024-11-08
3        4  688347  华虹公司  ...    NaN    半导体  2024-11-08
4        5  688347  华虹公司  ...    NaN    半导体  2024-11-08
...    ...     ...   ...  ...    ...    ...         ...
4637  4638  002521  齐峰新材  ...    NaN   造纸印刷  2024-10-12
4638  4639  300102  乾照光电  ...    NaN  光学光电子  2024-10-12
4639  4640  301227  森鹰窗业  ...    NaN   装修建材  2024-10-12
4640  4641  301227  森鹰窗业  ...    NaN   装修建材  2024-10-12
4641  4642  300708  聚灿光电  ...    NaN  光学光电子  2024-10-11
[4642 rows x 10 columns]
```
