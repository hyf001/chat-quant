---
title: "stock_zh_a_disclosure_report_cninfo - 信息披露公告-巨潮资讯"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_zh_a_disclosure_report_cninfo

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 年报季报 > 信息披露公告-巨潮资讯
- 描述: 巨潮资讯-首页-公告查询-信息披露公告
- 目标地址: http://www.cninfo.com.cn/new/commonUrl/pageOfSearch?url=disclosure/list/search
- 限量: 单次获取指定 symbol 的信息披露公告数据; 无数据时返回空的 pandas.DataFrame
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 信息披露公告-巨潮资讯

接口: stock_zh_a_disclosure_report_cninfo

目标地址: http://www.cninfo.com.cn/new/commonUrl/pageOfSearch?url=disclosure/list/search

描述: 巨潮资讯-首页-公告查询-信息披露公告

限量: 单次获取指定 symbol 的信息披露公告数据; 无数据时返回空的 pandas.DataFrame

输入参数

| 名称         | 类型  | 描述                                                                                                                                                                                                                         |
|------------|-----|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| symbol     | str | symbol="000001"; 股票代码                                                                                                                                                                                                      |
| market     | str | market="沪深京"; choice of {"沪深京", "港股", "三板", "基金", "债券", "监管", "预披露"}                                                                                                                                                       |
| keyword    | str | keyword=""; 关键词                                                                                                                                                                                                            |
| category   | str | category=""; choice of {'年报', '半年报', '一季报', '三季报', '业绩预告', '权益分派', '董事会', '监事会', '股东大会', '日常经营', '公司治理', '中介报告', '首发', '增发', '股权激励', '配股', '解禁', '公司债', '可转债', '其他融资', '股权变动', '补充更正', '澄清致歉', '风险提示', '特别处理和退市', '退市整理期'} |
| start_date | str | start_date="20230618"                                                                                                                                                                                                      |
| end_date   | str | end_date="20231219"                                                                                                                                                                                                        |

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

stock_zh_a_disclosure_report_cninfo_df = ak.stock_zh_a_disclosure_report_cninfo(symbol="000001", market="沪深京", category="公司治理", start_date="20230619", end_date="20231220")
print(stock_zh_a_disclosure_report_cninfo_df)
```

数据示例

```
   代码    简称  ...        公告时间                               公告链接
0  000001  平安银行  ...  2023-12-09  http://www.cninfo.com.cn/new/disclosure/detail...
1  000001  平安银行  ...  2023-11-21  http://www.cninfo.com.cn/new/disclosure/detail...
2  000001  平安银行  ...  2023-10-25  http://www.cninfo.com.cn/new/disclosure/detail...
3  000001  平安银行  ...  2023-08-24  http://www.cninfo.com.cn/new/disclosure/detail...
4  000001  平安银行  ...  2023-07-29  http://www.cninfo.com.cn/new/disclosure/detail...
5  000001  平安银行  ...  2023-07-25  http://www.cninfo.com.cn/new/disclosure/detail...
[6 rows x 5 columns]
```
