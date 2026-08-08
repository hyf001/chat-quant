---
title: "stock_zh_index_daily_em - 历史行情数据-东方财富"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# stock_zh_index_daily_em

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > A股股票指数 > 历史行情数据 > 历史行情数据-东方财富
- 描述: 东方财富股票指数数据, 历史数据按日频率更新
- 目标地址: http://quote.eastmoney.com/center/hszs.html
- 限量: 单次返回具体指数的所有历史行情数据
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 历史行情数据-东方财富

接口: stock_zh_index_daily_em

目标地址: http://quote.eastmoney.com/center/hszs.html

描述: 东方财富股票指数数据, 历史数据按日频率更新

限量: 单次返回具体指数的所有历史行情数据

输入参数

| 名称         | 类型  | 描述                                                                      |
|------------|-----|-------------------------------------------------------------------------|
| symbol     | str | symbol="sz399552"; 支持 sz: 深交所, sh: 上交所, bj: 北交所, csi: 中证指数 + id(000905) |
| start_date | str | start_date="19900101"                                                   |
| end_date   | str | end_date="20500101"                                                     |

输出参数

| 名称     | 类型      | 描述                    |
|--------|---------|-----------------------|
| date   | object  | 东方财富的数据开始时间, 不是证券上市时间 |
| open   | float64 | -                     |
| close  | float64 | -                     |
| high   | float64 | -                     |
| low    | float64 | -                     |
| volume | int64   | -                     |
| amount | float64 | -                     |

接口示例

```python
import akshare as ak

stock_zh_index_daily_em_df = ak.stock_zh_index_daily_em(symbol="sz399812")
print(stock_zh_index_daily_em_df)
```

数据示例

```
            date     open    close     high      low    volume        amount
0     2005-01-04   996.03   989.56   996.03   986.46    675733  4.986503e+08
1     2005-01-05   989.87  1008.59  1011.29   989.46   1037894  9.068431e+08
2     2005-01-06  1008.88  1002.81  1008.88   999.76    779152  5.631133e+08
3     2005-01-07  1002.10  1004.06  1015.61   999.56    898377  7.554397e+08
4     2005-01-10  1002.63  1014.12  1014.12  1000.90    651187  5.609582e+08
          ...      ...      ...      ...      ...       ...           ...
4566  2023-10-23  5659.09  5590.27  5666.15  5563.09   7956295  1.752549e+10
4567  2023-10-24  5608.75  5692.22  5700.26  5590.94   8032521  1.902381e+10
4568  2023-10-25  5735.01  5713.71  5751.73  5713.65   8597481  2.057249e+10
4569  2023-10-26  5694.04  5749.56  5755.59  5684.16   8636096  2.021819e+10
4570  2023-10-27  5747.77  5952.02  5969.61  5741.26  11493696  3.220613e+10
[4571 rows x 7 columns]
```
