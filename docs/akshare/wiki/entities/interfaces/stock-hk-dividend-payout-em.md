---
title: "stock_hk_dividend_payout_em - 分红派息"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_hk_dividend_payout_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 港股 > 分红派息
- 描述: 东方财富-港股-核心必读-分红派息
- 目标地址: https://emweb.securities.eastmoney.com/PC_HKF10/pages/home/index.html?code=03900&type=web&color=w#/CoreReading
- 限量: 单次返回全部数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 分红派息

接口: stock_hk_dividend_payout_em

目标地址: https://emweb.securities.eastmoney.com/PC_HKF10/pages/home/index.html?code=03900&type=web&color=w#/CoreReading

描述: 东方财富-港股-核心必读-分红派息

限量: 单次返回全部数据

输入参数

| 名称     | 类型  | 描述             |
|--------|-----|----------------|
| symbol | str | symbol="03900" |

输出参数

| 名称     | 类型     | 描述 |
|--------|--------|----|
| 最新公告日期 | object | -  |
| 财政年度   | object | -  |
| 分红方案   | object | -  |
| 分配类型   | object | -  |
| 除净日    | object | -  |
| 截至过户日  | object | -  |
| 发放日    | object | -  |

接口示例

```python
import akshare as ak

stock_hk_dividend_payout_em_df = ak.stock_hk_dividend_payout_em(symbol="03900")
print(stock_hk_dividend_payout_em_df)
```

数据示例

```
    最新公告日期  财政年度  ...      截至过户日         发放日
0   2025-06-20  2024  ...  2025/06/27-2025/07/02  2025-07-31
1   2024-06-14  2023  ...  2024/06/21-2024/06/25  2024-07-31
2   2023-06-16  2022  ...  2023/06/23-2023/06/27  2023-07-31
3   2022-06-17  2021  ...  2022/06/24-2022/06/28  2022-07-29
4   2021-06-18  2020  ...  2021/06/25-2021/06/29  2021-07-31
5   2020-06-12  2019  ...  2020/06/19-2020/06/23  2020-07-31
6   2019-06-14  2018  ...  2019/06/21-2019/06/25  2019-07-29
7   2018-06-15  2017  ...  2018/06/22-2018/06/26  2018-07-18
8   2017-06-16  2016  ...  2017/06/22-2017/06/26  2017-07-31
9   2014-06-27  2013  ...  2014/07/04-2014/07/09  2014-07-18
10  2013-06-18  2012  ...  2013/06/27-2013/07/02  2013-07-12
11  2012-02-07  2011  ...  2012/02/29-2012/03/02  2012-03-19
12  2011-06-14  2010  ...  2011/06/07-2011/06/13  2011-06-17
13  2010-08-25  2010  ...  2010/09/13-2010/09/15  2010-09-27
14  2010-06-04  2009  ...  2010/06/01-2010/06/03  2010-06-11
15  2009-09-18  2009  ...  2009/10/12-2009/10/14  2009-10-23
16  2012-06-18  2008  ...  2009/07/04-2009/07/08  2009-07-17
17  2008-05-26  2007  ...  2008/05/21-2008/05/23  2008-05-30
18  2007-05-14  2006  ...  2007/05/07-2007/05/11  2007-05-22
[19 rows x 7 columns]
```
