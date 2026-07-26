---
title: "index_zh_a_hist - 历史行情数据-通用"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, index, parameters, returns, example]
sources: [raw/data-dictionary/index/index.md]
confidence: high
---
# index_zh_a_hist

- 分类: [[index-index|AKShare 指数数据]]
- 主题路径: AKShare 指数数据 > A股股票指数 > 历史行情数据 > 历史行情数据-通用
- 描述: 东方财富网-中国股票指数-行情数据
- 目标地址: http://quote.eastmoney.com/center/hszs.html
- 限量: 单次返回具体指数指定 period 从 start_date 到 end_date 的之间的近期数据
- 来源页面: https://akshare.akfamily.xyz/data/index/index.html

## 相关

- [[index-index|AKShare 指数数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 历史行情数据-通用

接口: index_zh_a_hist

目标地址: http://quote.eastmoney.com/center/hszs.html

描述: 东方财富网-中国股票指数-行情数据

限量: 单次返回具体指数指定 period 从 start_date 到 end_date 的之间的近期数据

输入参数

| 名称         | 类型  | 描述                                                       |
|------------|-----|----------------------------------------------------------|
| symbol     | str | symbol="399282"; 指数代码，此处不用市场标识                           |
| period     | str | period="daily"; choice of {'daily', 'weekly', 'monthly'} |
| start_date | str | start_date="19700101"; 开始日期                              |
| end_date   | str | end_date="22220101"; 结束时间                                |

输出参数

| 名称  | 类型      | 描述      |
|-----|---------|---------|
| 日期  | object  | 交易日     |
| 开盘  | float64 | 开盘价     |
| 收盘  | float64 | 收盘价     |
| 最高  | float64 | 最高价     |
| 最低  | float64 | 最低价     |
| 成交量 | int32   | 注意单位: 手 |
| 成交额 | float64 | 注意单位: 元 |
| 振幅  | float64 | 注意单位: % |
| 涨跌幅 | float64 | 注意单位: % |
| 涨跌额 | float64 | 注意单位: 元 |
| 换手率 | float64 | 注意单位: % |

接口示例

```python
import akshare as ak

index_zh_a_hist_df = ak.index_zh_a_hist(symbol="000016", period="daily", start_date="19700101", end_date="22220101")
print(index_zh_a_hist_df)
```

数据示例

```
       日期       开盘       收盘       最高  ...   振幅   涨跌幅 涨跌额   换手率
0     2004-01-02   997.00  1011.35  1021.57  ...  0.00  0.00   0.00  0.00
1     2004-01-05  1008.28  1060.80  1060.90  ...  5.20  4.89  49.45  0.00
2     2004-01-06  1059.14  1075.66  1086.69  ...  2.60  1.40  14.86  0.00
3     2004-01-07  1075.56  1086.30  1095.84  ...  2.31  0.99  10.64  0.00
4     2004-01-08  1087.68  1102.66  1108.29  ...  2.37  1.51  16.36  0.00
          ...      ...      ...      ...  ...   ...   ...    ...   ...
4400  2022-02-15  3101.36  3119.93  3126.42  ...  0.95  0.51  15.93  0.24
4401  2022-02-16  3134.88  3136.08  3150.86  ...  0.70  0.52  16.15  0.20
4402  2022-02-17  3138.77  3139.18  3156.87  ...  0.79  0.10   3.10  0.20
4403  2022-02-18  3126.28  3162.82  3162.82  ...  1.30  0.75  23.64  0.19
4404  2022-02-21  3155.32  3144.86  3155.88  ...  0.86 -0.57 -17.96  0.21
```
