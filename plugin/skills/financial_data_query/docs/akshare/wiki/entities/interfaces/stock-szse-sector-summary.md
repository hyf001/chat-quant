---
title: "stock_szse_sector_summary - 股票行业成交"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_szse_sector_summary

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: AKShare 股票数据 > A股 > 股票市场总貌 > 深圳证券交易所 > 股票行业成交
- 描述: 深圳证券交易所-统计资料-股票行业成交数据
- 目标地址: http://docs.static.szse.cn/www/market/periodical/month/W020220511355248518608.html
- 限量: 单次返回指定 symbol 和 date 的统计资料-股票行业成交数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 股票行业成交

接口: stock_szse_sector_summary

目标地址: http://docs.static.szse.cn/www/market/periodical/month/W020220511355248518608.html

描述: 深圳证券交易所-统计资料-股票行业成交数据

限量: 单次返回指定 symbol 和 date 的统计资料-股票行业成交数据

输入参数

| 名称     | 类型  | 描述                                  |
|--------|-----|-------------------------------------|
| symbol | str | symbol="当月"; choice of {"当月", "当年"} |
| date   | str | date="202501"; 年月                   |

输出参数

| 名称        | 类型      | 描述      |
|-----------|---------|---------|
| 项目名称      | object  | -       |
| 项目名称-英文   | object  | -       |
| 交易天数      | int64   | -       |
| 成交金额-人民币元 | int64   |         |
| 成交金额-占总计  | float64 | 注意单位: % |
| 成交股数-股数   | int64   | -       |
| 成交股数-占总计  | float64 | 注意单位: % |
| 成交笔数-笔    | int64   | -       |
| 成交笔数-占总计  | float64 | 注意单位: % |

接口示例

```python
import akshare as ak

stock_szse_sector_summary_df = ak.stock_szse_sector_summary(symbol="当年", date="202501")
print(stock_szse_sector_summary_df)
```

数据示例

```
    项目名称            项目名称-英文 交易天数  ... 成交股数-占总计 成交笔数-笔 成交笔数-占总计
0     合计                     Total    18  ...    100.00  1072706301    100.00
1   农林牧渔               Agriculture    18  ...      0.85     7661044      0.71
2    采矿业                    Mining    18  ...      0.90     9355248      0.87
3    制造业             Manufacturing    18  ...     59.75   715973899     66.74
4   水电煤气                 Utilities    18  ...      1.47    12802444      1.19
5    建筑业              Construction    18  ...      1.39    10222345      0.95
6   批发零售        Wholesale & Retail    18  ...      4.73    40706994      3.79
7   运输仓储            Transportation    18  ...      0.99    11426446      1.07
8   住宿餐饮         Hotels & Catering    18  ...      0.19     1728478      0.16
9   信息技术                        IT    18  ...     11.73   137478307     12.82
10   金融业                   Finance    18  ...      3.76    31633210      2.95
11   房地产               Real Estate    18  ...      2.88    13878880      1.29
12  商务服务          Business Support    18  ...      6.48    38310245      3.57
13  科研服务    Research & Development    18  ...      0.63    10972681      1.02
14  公共环保  Environmental Protection    18  ...      1.61    10919804      1.02
15  居民服务         Resident Services    18  ...      0.01      217920      0.02
16    教育                 Education    18  ...      0.64     3040949      0.28
17    卫生             Public Health    18  ...      0.51     4706600      0.44
18  文化传播                     Media    18  ...      1.33    10017645      0.93
19    综合             Conglomerates    18  ...      0.14     1653162      0.15
[20 rows x 9 columns]
```
