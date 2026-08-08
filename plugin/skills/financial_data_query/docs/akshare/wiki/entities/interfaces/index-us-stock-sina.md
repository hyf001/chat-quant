---
title: "index_us_stock_sina - 指数行情"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# index_us_stock_sina

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > 美股股票指数 > 指数行情
- 描述: 新浪财经-美股指数行情
- 目标地址: https://stock.finance.sina.com.cn/usstock/quotes/.IXIC.html
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 指数行情

接口: index_us_stock_sina

目标地址: https://stock.finance.sina.com.cn/usstock/quotes/.IXIC.html

描述: 新浪财经-美股指数行情

输入参数

| 名称     | 类型  | 描述                                                         |
|--------|-----|------------------------------------------------------------|
| symbol | str | symbol=".INX"; choice of {".IXIC", ".DJI", ".INX", ".NDX"} |

输出参数

| 名称     | 类型      | 描述 |
|--------|---------|----|
| date   | object  | -  |
| open   | float64 | -  |
| high   | float64 | -  |
| low    | float64 | -  |
| close  | float64 | -  |
| volume | int64   | -  |
| amount | int64   | -  |

接口示例

```python
import akshare as ak

index_us_stock_sina_df = ak.index_us_stock_sina(symbol=".INX")
print(index_us_stock_sina_df)
```

数据示例

```
          date       open       high  ...      close      volume         amount
0     2004-01-02  1111.9200  1118.8500  ...  1108.4800  1153200000  1281300000000
1     2004-01-05  1108.4800  1122.2200  ...  1122.2200  1578200064  1760250000000
2     2004-01-06  1122.2200  1124.4600  ...  1123.6700  1494499968  1677120000000
3     2004-01-07  1123.6700  1126.3300  ...  1126.3300  1704899968  1914940000000
4     2004-01-08  1126.3300  1131.9200  ...  1131.9200  1868400000  2108990000000
          ...        ...        ...  ...        ...         ...            ...
4951  2023-08-30  4500.3398  4521.6499  ...  4514.8701  1827645178              0
4952  2023-08-31  4517.0098  4532.2598  ...  4507.6602  2352361081              0
4953  2023-09-01  4530.6001  4541.2500  ...  4515.7700  1958155311              0
4954  2023-09-05  4510.0601  4514.2900  ...  4496.8301  2128341430              0
4955  2023-09-06  4490.3501  4490.3501  ...  4465.4800  2122160141              0
[4956 rows x 7 columns]
```
