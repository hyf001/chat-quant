---
title: "macro_china_retail_price_index - 商品零售价格指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_retail_price_index

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 商品零售价格指数
- 描述: 国家统计局-商品零售价格指数
- 目标地址: http://finance.sina.com.cn/mac/#price-12-0-31-1
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 商品零售价格指数

接口: macro_china_retail_price_index

目标地址: http://finance.sina.com.cn/mac/#price-12-0-31-1

描述: 国家统计局-商品零售价格指数

限量: 单次返回所有历史数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称       | 类型      | 描述 |
|----------|---------|----|
| 统计月份     | object  | 年月 |
| 居民消费项目   | object  | -  |
| 零售商品价格指数 | float64 | -  |

接口示例

```python
import akshare as ak

macro_china_retail_price_index_df = ak.macro_china_retail_price_index()
print(macro_china_retail_price_index_df)
```

数据示例

```
     统计月份       居民消费项目 零售商品价格指数
0     2020.8    建筑材料及五金电料   100.10
1     2020.8           燃料    90.70
2     2020.8   书报杂志及电子出版物   101.70
3     2020.8  中西药品及医疗保健用品   100.30
4     2020.8         金银珠宝   122.90
      ...          ...      ...
3777  2002.1         机电产品    94.10
3778  2002.1    家用电器及音像器材    94.20
3779  2002.1       体育娱乐用品    98.80
3780  2002.1  中西药品及医疗保健用品    97.30
3781  2002.1   书报杂志及电子出版物   101.00
```
