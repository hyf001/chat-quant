---
title: "stock_cg_lawsuit_cninfo - 公司诉讼"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_cg_lawsuit_cninfo

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 机构推荐 > 公司诉讼
- 描述: 巨潮资讯-数据中心-专题统计-公司治理-公司诉讼
- 目标地址: https://webapi.cninfo.com.cn/#/thematicStatistics
- 限量: 单次指定 symbol 和起始日期的公司诉讼数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 公司诉讼

接口: stock_cg_lawsuit_cninfo

目标地址: https://webapi.cninfo.com.cn/#/thematicStatistics

描述: 巨潮资讯-数据中心-专题统计-公司治理-公司诉讼

限量: 单次指定 symbol 和起始日期的公司诉讼数据

说明: 接口内部已兼容巨潮资讯当前鉴权方式; 源站无数据时返回空 DataFrame

输入参数

| 名称         | 类型  | 描述                                                        |
|------------|-----|-----------------------------------------------------------|
| symbol     | str | symbol="全部"; choice of {"全部", "深市主板", "沪市", "创业板", "科创板"} |
| start_date | str | start_date="20180630"                                     |
| end_date   | str | end_date="20210927"                                       |

输出参数

| 名称     | 类型      | 描述       |
|--------|---------|----------|
| 证券代码   | object  | -        |
| 证券简称   | object  | -        |
| 公告统计区间 | object  | -        |
| 诉讼次数   | int64   | -        |
| 诉讼金额   | float64 | 注意单位: 万元 |

接口示例

```python
import akshare as ak

stock_cg_lawsuit_cninfo_df = ak.stock_cg_lawsuit_cninfo(symbol="全部", start_date="20180630", end_date="20210927")
print(stock_cg_lawsuit_cninfo_df)
```

数据示例

```
        证券代码  证券简称                   公告统计区间  诉讼次数      诉讼金额
0     002524  光正眼科  2018-06-30---2021-09-27     1       NaN
1     603507  振江股份  2018-06-30---2021-09-27     1       NaN
2     600410  华胜天成  2018-06-30---2021-09-27     2       NaN
3     601333  广深铁路  2018-06-30---2021-09-27     1       NaN
4     301013   利和兴  2018-06-30---2021-09-27     1       NaN
      ...   ...                      ...   ...       ...
948   300310  宜通世纪  2018-06-30---2021-09-27    13   8716.50
949   300353  东土科技  2018-06-30---2021-09-27     3       NaN
950   600526  菲达环保  2018-06-30---2021-09-27    80  20593.75
951   600645  中源协和  2018-06-30---2021-09-27     1   5155.00
952   600733  北汽蓝谷  2018-06-30---2021-09-27     4    309.93
```
