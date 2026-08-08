---
title: "stock_industry_clf_hist_sw - 申万个股行业分类变动历史"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_industry_clf_hist_sw

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 机构推荐 > 申万个股行业分类变动历史
- 描述: 申万宏源研究-行业分类-全部行业分类
- 目标地址: http://www.swhyresearch.com/institute_sw/allIndex/downloadCenter/industryType
- 限量: 单次获取所有个股的行业分类变动历史数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 申万个股行业分类变动历史

接口: stock_industry_clf_hist_sw

目标地址: http://www.swhyresearch.com/institute_sw/allIndex/downloadCenter/industryType

描述: 申万宏源研究-行业分类-全部行业分类

限量: 单次获取所有个股的行业分类变动历史数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称            | 类型     | 描述     |
|---------------|--------|--------|
| symbol        | object | 股票代码   |
| start_date    | object | 计入日期   |
| industry_code | object | 申万行业代码 |
| update_time   | object | 更新日期   |

接口示例

```python
import akshare as ak

stock_industry_clf_hist_sw_df = ak.stock_industry_clf_hist_sw()
print(stock_industry_clf_hist_sw_df)
```

数据示例

```
       symbol  start_date industry_code update_time
0      000001  1991-04-03        440101  2015-10-27
1      000001  2014-01-01        480101  2015-10-27
2      000001  2021-07-30        480301  2021-07-31
3      000002  1991-01-29        430101  2015-10-27
4      000003  1991-04-14        510101  2015-10-27
...       ...         ...           ...         ...
12360  873706  2024-03-12        640601  2024-03-13
12361  873726  2023-10-30        640209  2023-10-30
12362  873806  2024-01-17        710301  2024-01-17
12363  873833  2023-11-20        640106  2023-11-20
12364  874090  2023-08-21        370304  2023-08-21
[12365 rows x 4 columns]
```
