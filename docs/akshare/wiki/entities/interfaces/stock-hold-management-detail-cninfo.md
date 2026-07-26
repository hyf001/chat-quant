---
title: "stock_hold_management_detail_cninfo - 高管持股变动明细"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_hold_management_detail_cninfo

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 机构推荐 > 高管持股变动明细
- 描述: 巨潮资讯-数据中心-专题统计-股东股本-高管持股变动明细
- 目标地址: https://webapi.cninfo.com.cn/#/thematicStatistics
- 限量: 单次指定 symbol 的高管持股变动明细数据, 返回近一年的数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 高管持股变动明细

接口: stock_hold_management_detail_cninfo

目标地址: https://webapi.cninfo.com.cn/#/thematicStatistics

描述: 巨潮资讯-数据中心-专题统计-股东股本-高管持股变动明细

限量: 单次指定 symbol 的高管持股变动明细数据, 返回近一年的数据

输入参数

| 名称     | 类型  | 描述                                  |
|--------|-----|-------------------------------------|
| symbol | str | symbol="增持"; choice of {"增持", "减持"} |

输出参数

| 名称        | 类型      | 描述       |
|-----------|---------|----------|
| 证劵代码      | object  | -        |
| 证券简称      | object  | -        |
| 截止日期      | object  | -        |
| 公告日期      | object  | -        |
| 高管姓名      | object  | -        |
| 董监高姓名     | object  | -        |
| 董监高职务     | object  | -        |
| 变动人与董监高关系 | object  | -        |
| 期初持股数量    | float64 | 注意单位: 万股 |
| 期末持股数量    | float64 | 注意单位: 万股 |
| 变动数量      | float64 | -        |
| 变动比例      | int64   | 注意单位: %  |
| 成交均价      | float64 | 注意单位: 元  |
| 期末市值      | float64 | 注意单位: 万元 |
| 持股变动原因    | object  | -        |
| 数据来源      | object  | -        |

接口示例

```python
import akshare as ak

stock_hold_management_detail_cninfo_df = ak.stock_hold_management_detail_cninfo(symbol="增持")
print(stock_hold_management_detail_cninfo_df)
```

数据示例

```
        证券代码  证券简称  截止日期    公告日期 高管姓名  ... 变动比例 成交均价 期末市值  持股变动原因  数据来源
0      000010  美丽生态  2023-12-31  2024-04-27   张琳  ...  NaN  NaN  NaN    None  定期报告
1      000010  美丽生态  2023-12-31  2024-04-27   张龙  ...  NaN  NaN  NaN    None  定期报告
2      000010  美丽生态  2023-12-31  2024-04-27  周成斌  ...  NaN  NaN  NaN    None  定期报告
3      000010  美丽生态  2023-12-31  2024-04-27  林孔凤  ...  NaN  NaN  NaN    None  定期报告
4      000010  美丽生态  2023-12-31  2024-04-27  江成汉  ...  NaN  NaN  NaN    None  定期报告
...       ...   ...         ...         ...  ...  ...  ...  ...  ...     ...   ...
15229  900946  天雁B股  2023-12-31  2024-04-20  何光清  ...  NaN  NaN  NaN    None  定期报告
15230  900946  天雁B股  2023-12-31  2024-04-20  刘青娥  ...  NaN  NaN  NaN    None  定期报告
15231  900946  天雁B股  2023-12-31  2024-04-20  杨国旗  ...  NaN  NaN  NaN    None  定期报告
15232  900946  天雁B股  2023-12-31  2024-04-20  杨宝全  ...  NaN  NaN  NaN    None  定期报告
15233  900946  天雁B股  2023-12-31  2024-04-20  胡辽平  ...  NaN  NaN  NaN    None  定期报告
[15234 rows x 16 columns]
```
