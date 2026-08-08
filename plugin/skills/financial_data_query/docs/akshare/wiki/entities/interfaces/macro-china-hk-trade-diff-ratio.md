---
title: "macro_china_hk_trade_diff_ratio - 香港商品贸易差额年率"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_hk_trade_diff_ratio

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国香港宏观 > 香港商品贸易差额年率
- 描述: 东方财富-经济数据一览-中国香港-香港商品贸易差额年率
- 目标地址: https://data.eastmoney.com/cjsj/foreign_8_7.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 香港商品贸易差额年率

接口: macro_china_hk_trade_diff_ratio

目标地址: https://data.eastmoney.com/cjsj/foreign_8_7.html

描述: 东方财富-经济数据一览-中国香港-香港商品贸易差额年率

限量: 单次返回所有历史数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称   | 类型      | 描述      |
|------|---------|---------|
| 时间   | object  | -       |
| 前值   | float64 | 注意单位: % |
| 现值   | float64 | 注意单位: % |
| 发布日期 | object  | -       |

接口示例

```python
import akshare as ak

macro_china_hk_trade_diff_ratio_df = ak.macro_china_hk_trade_diff_ratio()
print(macro_china_hk_trade_diff_ratio_df)
```

数据示例

```
           时间      前值         现值        发布日期
0    2008年01月  -31.654573  -69.070295  2008-02-27
1    2008年02月  -69.070295 -109.659467  2008-03-29
2    2008年03月 -109.659467    0.699128  2008-04-27
3    2008年04月    0.699128   21.249636  2008-05-28
4    2008年05月   21.249636  -92.302304  2008-06-27
..        ...         ...         ...         ...
189  2023年10月  -43.766696  -23.398342  2023-11-27
190  2023年11月  -23.398342   -3.056591  2023-12-28
191  2023年12月   -3.056591  -15.908299  2024-01-25
192  2024年01月  -15.908299  114.357782  2024-02-27
193  2024年02月  114.357782    8.186928  2024-03-26
[194 rows x 4 columns]
```
