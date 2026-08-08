---
title: "stock_industry_pe_ratio_cninfo - 行业市盈率"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_industry_pe_ratio_cninfo

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 机构推荐 > 行业市盈率
- 描述: 巨潮资讯-数据中心-行业分析-行业市盈率
- 目标地址: http://webapi.cninfo.com.cn/#/thematicStatistics
- 限量: 单次获取指定 symbol 在指定交易日的所有数据; 只能获取近期的数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 行业市盈率

接口: stock_industry_pe_ratio_cninfo

目标地址: http://webapi.cninfo.com.cn/#/thematicStatistics

描述: 巨潮资讯-数据中心-行业分析-行业市盈率

限量: 单次获取指定 symbol 在指定交易日的所有数据; 只能获取近期的数据

输入参数

| 名称     | 类型  | 描述                                                |
|--------|-----|---------------------------------------------------|
| symbol | str | symbol="证监会行业分类"; choice of {"证监会行业分类", "国证行业分类"} |
| date   | str | date="20210910"; 交易日                              |

输出参数

| 名称         | 类型      | 描述       |
|------------|---------|----------|
| 变动日期       | object  | -        |
| 行业分类       | object  | -        |
| 行业层级       | int64   | -        |
| 行业编码       | object  | -        |
| 行业名称       | object  | -        |
| 公司数量       | float64 | -        |
| 纳入计算公司数量   | float64 | -        |
| 总市值-静态     | float64 | 注意单位: 亿元 |
| 净利润-静态     | float64 | 注意单位: 亿元 |
| 静态市盈率-加权平均 | float64 | -        |
| 静态市盈率-中位数  | float64 | -        |
| 静态市盈率-算术平均 | float64 | -        |

接口示例

```python
import akshare as ak

stock_industry_pe_ratio_cninfo_df = ak.stock_industry_pe_ratio_cninfo(symbol="国证行业分类", date="20240617")
print(stock_industry_pe_ratio_cninfo_df)
```

数据示例

```
        变动日期          行业分类  行业层级  ... 静态市盈率-加权平均 静态市盈率-中位数  静态市盈率-算术平均
0    2024-06-17  国证行业分类标准2019     1  ...      11.54     15.75       49.19
1    2024-06-17  国证行业分类标准2019     2  ...      11.54     15.75       49.19
2    2024-06-17  国证行业分类标准2019     3  ...      18.44     22.05       28.24
3    2024-06-17  国证行业分类标准2019     4  ...      19.23     21.45       30.02
4    2024-06-17  国证行业分类标准2019     4  ...      18.10     24.86       25.35
..          ...           ...   ...  ...        ...       ...         ...
288  2024-06-17  国证行业分类标准2019     4  ...        NaN       NaN         NaN
289  2024-06-17  国证行业分类标准2019     3  ...      19.59     22.28       43.17
290  2024-06-17  国证行业分类标准2019     4  ...      19.59     22.28       43.17
291  2024-06-17  国证行业分类标准2019     3  ...      14.12     14.12       14.12
292  2024-06-17  国证行业分类标准2019     4  ...      14.12     14.12       14.12
[293 rows x 12 columns]
```
