---
title: "macro_china_international_tourism_fx - 国际旅游外汇收入构成"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_international_tourism_fx

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 国际旅游外汇收入构成
- 描述: 国家统计局-国际旅游外汇收入构成
- 目标地址: http://finance.sina.com.cn/mac/#industry-15-0-31-3
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 国际旅游外汇收入构成

接口: macro_china_international_tourism_fx

目标地址: http://finance.sina.com.cn/mac/#industry-15-0-31-3

描述: 国家统计局-国际旅游外汇收入构成

限量: 单次返回所有历史数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称   | 类型      | 描述         |
|------|---------|------------|
| 统计年度 | object  | 年          |
| 指标   | object  | -          |
| 数量   | float64 | 注意单位: 百万美元 |
| 比重   | float64 | 注意单位: %    |

接口示例

```python
import akshare as ak

macro_china_international_tourism_fx_df = ak.macro_china_international_tourism_fx()
print(macro_china_international_tourism_fx_df)
```

数据示例

```
     统计年度    指标        数量     比重
0    2019    餐饮   16041.0   12.2
1    2019    总计  131254.0  100.0
2    2019  市内交通    3453.0    2.6
3    2019  其他服务   10189.0    7.8
4    2019    汽车    1593.0    1.2
..    ...   ...       ...    ...
251  1996    餐饮    1376.0   13.5
252  1995    总计    8733.0  100.0
253  1994    总计    7323.0  100.0
254  1993    总计    4683.0  100.0
255  1992    总计    3947.0  100.0
[256 rows x 4 columns]
```
