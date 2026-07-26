---
title: "stock_dividend_cninfo - 历史分红"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_dividend_cninfo

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 历史分红
- 描述: 巨潮资讯-个股-历史分红
- 目标地址: http://webapi.cninfo.com.cn/#/company?companyid=600009
- 限量: 单次获取指定股票的历史分红数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 历史分红

接口: stock_dividend_cninfo

目标地址: http://webapi.cninfo.com.cn/#/company?companyid=600009

描述: 巨潮资讯-个股-历史分红

限量: 单次获取指定股票的历史分红数据

输入参数

| 名称     | 类型  | 描述              |
|--------|-----|-----------------|
| symbol | str | symbol="600009" |

输出参数

| 名称       | 类型      | 描述           |
|----------|---------|--------------|
| 实施方案公告日期 | object  | -            |
| 送股比例     | float64 | 注意单位: 每 10 股 |
| 转增比例     | float64 | 注意单位: 每 10 股 |
| 派息比例     | float64 | 注意单位: 每 10 股 |
| 股权登记日    | object  | -            |
| 除权日      | object  | -            |
| 派息日      | object  | -            |
| 股份到账日    | object  | -            |
| 实施方案分红说明 | object  | -            |
| 分红类型     | object  | -            |
| 报告时间     | object  | -            |

接口示例

```python
import akshare as ak

stock_dividend_cninfo_df = ak.stock_dividend_cninfo(symbol="600009")
print(stock_dividend_cninfo_df)
```

数据示例

```
    实施方案公告日期  分红类型  送股比例  转增比例  ...派息日 股份到账日   实施方案分红说明  报告时间
0   1998-11-28  中期分红   0.0   5.0  ...         NaT  None          10转增5股  1998半年报
1   2001-06-23  年度分红   NaN   NaN  ...  2001-07-06  None    10派2.93元(含税)   2000年报
2   2002-07-18  年度分红   NaN   NaN  ...  2002-08-01  None     10派1.5元(含税)   2001年报
3   2003-08-05  年度分红   NaN   NaN  ...  2003-08-14  None   10股派1.99元（含税）   2002年报
4   2003-12-22  中期分红   3.0   NaN  ...         NaT  None           10送3股  2003半年报
5   2004-07-16  年度分红   NaN   NaN  ...  2004-07-28  None    10派0.96元（含税）   2003年报
6   2005-05-17  年度分红   NaN   NaN  ...  2005-05-27  None       10派1元(含税)   2004年报
7   2006-08-15  年度分红   NaN   NaN  ...  2006-08-25  None     10派1.5元(含税)   2005年报
8   2006-12-01  中期分红   NaN   NaN  ...  2006-12-13  None       10派1元（含税）  2006半年报
9   2007-08-16  年度分红   NaN   NaN  ...  2007-08-28  None     10派1.5元（含税）   2006年报
10  2008-07-24  年度分红   NaN   NaN  ...  2008-08-05  None       10派1元（含税）   2007年报
11  2009-07-30  年度分红   NaN   NaN  ...  2009-08-11  None     10派0.5元（含税）   2008年报
12  2010-07-29  年度分红   NaN   NaN  ...  2010-08-10  None     10派0.5元（含税）   2009年报
13  2011-08-08  年度分红   NaN   NaN  ...  2011-08-18  None       10派1元(含税)   2010年报
14  2012-08-07  年度分红   NaN   NaN  ...  2012-08-17  None       10派6元(含税)   2011年报
15  2013-08-12  年度分红   NaN   NaN  ...  2013-08-22  None     10派3.7元(含税)   2012年报
16  2014-08-11  年度分红   NaN   NaN  ...  2014-08-15  None       10派3元(含税)   2013年报
17  2015-08-14  年度分红   NaN   NaN  ...  2015-08-20  None     10派3.5元(含税)   2014年报
18  2016-08-12  年度分红   NaN   NaN  ...  2016-08-18  None     10派4.3元(含税)   2015年报
19  2017-08-18  年度分红   NaN   NaN  ...  2017-08-24  None     10派4.4元(含税)   2016年报
20  2018-08-17  年度分红   NaN   NaN  ...  2018-08-23  None     10派5.8元(含税)   2017年报
21  2019-08-16  年度分红   NaN   NaN  ...  2019-08-22  None     10派6.6元(含税)   2018年报
22  2020-08-14  年度分红   NaN   NaN  ...  2020-08-20  None     10派7.9元(含税)   2019年报
23  2024-07-15  年度分红   NaN   NaN  ...  2024-07-19  None     10派1.2元(含税)   2023年报
24  2024-09-03  中期分红   NaN   NaN  ...  2024-09-09  None  10派1.0034元(含税)  2024半年报
25  2025-08-04  年度分红   NaN   NaN  ...  2025-08-08  None       10派3元(含税)   2024年报
26  2025-10-10  中期分红   NaN   NaN  ...  2025-10-16  None     10派2.1元(含税)  2025半年报
[27 rows x 11 columns]
```
