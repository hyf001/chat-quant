---
title: "macro_china_market_margin_sh - 上海融资融券报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_market_margin_sh

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 其他指标 > 上海融资融券报告
- 描述: 上海融资融券报告, 数据区间从 20100331-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_market_margin_sse
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 上海融资融券报告

接口: macro_china_market_margin_sh

目标地址: https://datacenter.jin10.com/reportType/dc_market_margin_sse

描述: 上海融资融券报告, 数据区间从 20100331-至今

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称     | 类型     | 描述     |
|--------|--------|--------|
| 日期     | object | 日期     |
| 融资余额   | int64  | 注意单位：元 |
| 融资买入额  | int64  | 注意单位：元 |
| 融券余量   | int64  | 注意单位：股 |
| 融券余额   | int64  | 注意单位：元 |
| 融券卖出量  | int64  | 注意单位：股 |
| 融资融券余额 | int64  | 注意单位：元 |

接口示例

```python
import akshare as ak

macro_china_market_margin_sh_df = ak.macro_china_market_margin_sh()
print(macro_china_market_margin_sh_df)
```

数据示例

```
       日期        融资买入额  ...         融券余额        融资融券余额
0     2010-03-31      5866316  ...        24142       5848955
1     2010-04-01      1054024  ...        17325       6859439
2     2010-04-02       207516  ...        11929       6774710
3     2010-04-06      3329461  ...        10267      10101510
4     2010-04-07     15141395  ...        38418      25125244
          ...          ...  ...          ...           ...
3352  2024-01-18  31033922602  ...  43743457679  862765876243
3353  2024-01-19  21406253320  ...  43641546854  859359188408
3354  2024-01-22  25940316396  ...  42027262985  851323826307
3355  2024-01-23  24325476838  ...  42650470550  849682914607
3356  2024-01-24  30879941897  ...  43796442043  849741276211
[3357 rows x 7 columns]
```
