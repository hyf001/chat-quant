---
title: "macro_china_new_house_price - 新房价指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_new_house_price

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 新房价指数
- 描述: 中国新房价指数月度数据, 数据区间从 201101-至今
- 目标地址: http://data.eastmoney.com/cjsj/newhouse.html
- 限量: 单次返回指定城市的所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 新房价指数

接口: macro_china_new_house_price

目标地址: http://data.eastmoney.com/cjsj/newhouse.html

描述: 中国新房价指数月度数据, 数据区间从 201101-至今

限量: 单次返回指定城市的所有历史数据

输入参数

| 名称          | 类型  | 描述                          |
|-------------|-----|-----------------------------|
| city_first  | str | city_first="北京"; 城市列表见目标网站  |
| city_second | str | city_second="上海"; 城市列表见目标网站 |

输出参数

| 名称            | 类型      | 描述  |
|---------------|---------|-----|
| 日期            | object  | 日期  |
| 城市            | object  | -   |
| 新建商品住宅价格指数-环比 | float64 | -   |
| 新建商品住宅价格指数-同比 | float64 | -   |
| 新建商品住宅价格指数-定基 | float64 | -   |
| 二手住宅价格指数-环比   | float64 | -   |
| 二手住宅价格指数-同比   | float64 | -   |
| 二手住宅价格指数-定基   | float64 | -   |

接口示例

```python
import akshare as ak

macro_china_new_house_price_df = ak.macro_china_new_house_price(city_first="北京", city_second="上海")
print(macro_china_new_house_price_df)
```

数据示例

```
           日期  城市  新建商品住宅价格指数-同比  ... 二手住宅价格指数-同比 二手住宅价格指数-环比 二手住宅价格指数-定基
0    2011-01-01  上海          101.8  ...        101.7        100.5        100.6
1    2011-01-01  北京          109.1  ...        102.6        100.3        101.2
2    2011-02-01  北京          108.4  ...        102.9        100.4        101.5
3    2011-02-01  上海          102.8  ...        102.0        100.4        101.0
4    2011-03-01  北京          106.2  ...        101.9         99.9        101.4
..          ...  ..            ...  ...          ...          ...          ...
327  2024-08-01  北京           96.4  ...         91.5         99.0          NaN
328  2024-09-01  上海          104.9  ...         92.4         98.8          NaN
329  2024-09-01  北京           95.4  ...         89.7         98.7          NaN
330  2024-10-01  上海          105.0  ...         93.3        100.2          NaN
331  2024-10-01  北京           95.1  ...         91.6        101.0          NaN
[332 rows x 8 columns]
```
