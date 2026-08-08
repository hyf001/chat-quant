---
title: "stock_zh_a_disclosure_relation_cninfo - 信息披露调研-巨潮资讯"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_zh_a_disclosure_relation_cninfo

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 年报季报 > 信息披露调研-巨潮资讯
- 描述: 巨潮资讯-首页-公告查询-信息披露调研
- 目标地址: http://www.cninfo.com.cn/new/commonUrl/pageOfSearch?url=disclosure/list/search
- 限量: 单次获取指定 symbol 的信息披露调研数据; 无数据时返回空的 pandas.DataFrame
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 信息披露调研-巨潮资讯

接口: stock_zh_a_disclosure_relation_cninfo

目标地址: http://www.cninfo.com.cn/new/commonUrl/pageOfSearch?url=disclosure/list/search

描述: 巨潮资讯-首页-公告查询-信息披露调研

限量: 单次获取指定 symbol 的信息披露调研数据; 无数据时返回空的 pandas.DataFrame

输入参数

| 名称         | 类型  | 描述                                                                   |
|------------|-----|----------------------------------------------------------------------|
| symbol     | str | symbol="000001"; 股票代码                                                |
| market     | str | market="沪深京"; choice of {"沪深京", "港股", "三板", "基金", "债券", "监管", "预披露"} |
| start_date | str | start_date="20230618"                                                |
| end_date   | str | end_date="20231219"                                                  |

输出参数

| 名称   | 类型     | 描述 |
|------|--------|----|
| 代码   | object | -  |
| 简称   | object | -  |
| 公告标题 | object | -  |
| 公告时间 | object | -  |
| 公告链接 | object | -  |

接口示例

```python
import akshare as ak

stock_zh_a_disclosure_relation_cninfo_df = ak.stock_zh_a_disclosure_relation_cninfo(symbol="000001", market="沪深京", start_date="20230619", end_date="20231220")
print(stock_zh_a_disclosure_relation_cninfo_df)
```

数据示例

```
   代码    简称  ...        公告时间                               公告链接
0  000001  平安银行  ...  2023-11-08  http://www.cninfo.com.cn/new/disclosure/detail...
1  000001  平安银行  ...  2023-11-01  http://www.cninfo.com.cn/new/disclosure/detail...
2  000001  平安银行  ...  2023-10-24  http://www.cninfo.com.cn/new/disclosure/detail...
3  000001  平安银行  ...  2023-10-24  http://www.cninfo.com.cn/new/disclosure/detail...
4  000001  平安银行  ...  2023-10-24  http://www.cninfo.com.cn/new/disclosure/detail...
5  000001  平安银行  ...  2023-10-24  http://www.cninfo.com.cn/new/disclosure/detail...
6  000001  平安银行  ...  2023-08-23  http://www.cninfo.com.cn/new/disclosure/detail...
7  000001  平安银行  ...  2023-08-23  http://www.cninfo.com.cn/new/disclosure/detail...
8  000001  平安银行  ...  2023-08-23  http://www.cninfo.com.cn/new/disclosure/detail...
9  000001  平安银行  ...  2023-08-23  http://www.cninfo.com.cn/new/disclosure/detail...
[10 rows x 5 columns]
```
