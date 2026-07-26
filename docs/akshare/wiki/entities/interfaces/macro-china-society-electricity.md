---
title: "macro_china_society_electricity - 全社会用电分类情况表"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_society_electricity

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 全社会用电分类情况表
- 描述: 国家统计局-全社会用电分类情况表
- 目标地址: http://finance.sina.com.cn/mac/#industry-6-0-31-1
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 全社会用电分类情况表

接口: macro_china_society_electricity

目标地址: http://finance.sina.com.cn/mac/#industry-6-0-31-1

描述: 国家统计局-全社会用电分类情况表

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称            | 类型      | 描述         |
|---------------|---------|------------|
| 统计时间          | object  | -          |
| 全社会用电量        | float64 | 注意单位: 万千瓦时 |
| 全社会用电量同比      | float64 | 注意单位: %    |
| 各行业用电量合计      | float64 | 注意单位: 万千瓦时 |
| 各行业用电量合计同比    | float64 | 注意单位: %    |
| 第一产业用电量       | float64 | 注意单位: 万千瓦时 |
| 第一产业用电量同比     | float64 | 注意单位: %    |
| 第二产业用电量       | float64 | 注意单位: 万千瓦时 |
| 第二产业用电量同比     | float64 | 注意单位: %    |
| 第三产业用电量       | float64 | 注意单位: 万千瓦时 |
| 第三产业用电量同比     | float64 | 注意单位: %    |
| 城乡居民生活用电量合计   | float64 | 注意单位: 万千瓦时 |
| 城乡居民生活用电量合计同比 | float64 | 注意单位: %    |
| 城镇居民用电量       | float64 | 注意单位: 万千瓦时 |
| 城镇居民用电量同比     | float64 | 注意单位: %    |
| 乡村居民用电量       | float64 | 注意单位: 万千瓦时 |
| 乡村居民用电量同比     | float64 | 注意单位: %    |

接口示例

```python
import akshare as ak

macro_china_society_electricity_df = ak.macro_china_society_electricity()
print(macro_china_society_electricity_df)
```

数据示例

```
      统计时间   全社会用电量  全社会用电量同比  ...  城镇居民用电量同比    乡村居民用电量  乡村居民用电量同比
0    2003.12  188912117.0     15.29  ...      16.12  8806708.0       5.79
1    2004.10  175828690.0     15.17  ...       8.74  7652223.0       8.99
2    2004.11  194584023.0     15.13  ...       8.95  8408040.0      10.48
3     2004.3   48045510.0     15.70  ...       9.85  2187609.0      11.68
4     2004.9  157131146.0     14.92  ...       8.58  6814158.0       9.80
..       ...          ...       ...  ...        ...        ...        ...
209   2023.6  430760000.0      5.00  ...        NaN        NaN        NaN
210   2023.7  519650000.0      5.20  ...        NaN        NaN        NaN
211   2023.8  608260000.0      5.00  ...        NaN        NaN        NaN
212   2023.9  686370000.0      5.60  ...        NaN        NaN        NaN
213   2024.2  153160000.0     11.00  ...        NaN        NaN        NaN
[214 rows x 17 columns]
```
