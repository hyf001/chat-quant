---
title: "macro_china_freight_index - 航贸运价指数"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_freight_index

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 航贸运价指数
- 描述: 新浪财经-中国宏观经济数据-航贸运价指数
- 目标地址: http://finance.sina.com.cn/mac/#industry-22-0-31-2
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 航贸运价指数

接口: macro_china_freight_index

目标地址: http://finance.sina.com.cn/mac/#industry-22-0-31-2

描述: 新浪财经-中国宏观经济数据-航贸运价指数

限量: 单次返回所有历史数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称                | 类型      | 描述 |
|-------------------|---------|----|
| 截止日期              | object  | 年月 |
| 波罗的海好望角型船运价指数BCI  | float64 | -  |
| 灵便型船综合运价指数BHMI    | float64 | -  |
| 波罗的海超级大灵便型船BSI指数  | float64 | -  |
| 波罗的海综合运价指数BDI     | float64 | -  |
| HRCI国际集装箱租船指数     | float64 | -  |
| 油轮运价指数成品油运价指数BCTI | float64 | -  |
| 油轮运价指数原油运价指数BDTI  | float64 | -  |

接口示例

```python
import akshare as ak

macro_china_freight_index_df = ak.macro_china_freight_index()
print(macro_china_freight_index_df)
```

数据示例

```
      截止日期  波罗的海好望角型船运价指数BCI  ...  油轮运价指数成品油运价指数BCTI  油轮运价指数原油运价指数BDTI
0     2021-08-10            4328.0  ...                NaN               NaN
1     2021-08-09            4342.0  ...                NaN               NaN
2     2021-08-06            4359.0  ...                NaN               NaN
3     2021-08-05            4414.0  ...                NaN               NaN
4     2021-08-04            4302.0  ...                NaN               NaN
          ...               ...  ...                ...               ...
3845  2005-12-13            3459.0  ...             1326.0            2063.0
3846  2005-12-12            3476.0  ...             1286.0            2051.0
3847  2005-12-09            3509.0  ...             1261.0            2061.0
3848  2005-12-08            3553.0  ...                NaN               NaN
3849  2005-12-07            3709.0  ...                NaN               NaN
```
