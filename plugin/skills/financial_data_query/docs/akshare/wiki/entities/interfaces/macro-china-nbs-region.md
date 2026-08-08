---
title: "macro_china_nbs_region - 国家统计局地区数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_nbs_region

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 国家统计局通用接口 > 国家统计局地区数据
- 描述: 国家统计局地区数据通用接口，包括分省月度数据、分省季度数据、分省年度数据、主要城市月度价格、主要城市年度数据、港澳台月度数据、港澳台年度数据，具体指标见国家统计局新站官网。
- 目标地址: https://data.stats.gov.cn/dg/website/page.html#/pc/national/fsYearData
- 限量: 根据参数返回指定数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 国家统计局地区数据

接口: macro_china_nbs_region

目标地址: https://data.stats.gov.cn/dg/website/page.html#/pc/national/fsYearData

描述: 国家统计局地区数据通用接口，包括分省月度数据、分省季度数据、分省年度数据、主要城市月度价格、主要城市年度数据、港澳台月度数据、港澳台年度数据，具体指标见国家统计局新站官网。

限量: 根据参数返回指定数据

输入参数

| 名称        | 类型               | 描述                                                                                                                                                |
|-----------|------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|
| kind      | str              | 数据类别，包括：分省月度数据、分省季度数据、分省年度数据、主要城市月度价格、主要城市年度数据、港澳台月度数据、港澳台年度数据。                                                                                   |
| path      | str              | 数据路径， 需与kind匹配，具体见官网，多层级之间使用  > 连接 。<br> 示例：<br>   国民经济核算 > 地区生产总值<br>   财政 > 地方财政收入                                                              |
| indicator | Union[str, None] | 指定指标，表示在当前path下可选择的指标。在指定region参数的情况下，此参数可以设置为None，此时将获取指定地区下所有可选指标的值。indicator和region参数不能同时为None。                                                |
| region    | Union[str, None] | 指定地区，为可选指标。指定时表示仅获取当前地区下的数据。                                                                                                                      |
| period    | str              | 时间区间<br/>参考格式如下(英文逗号分割，且不能有多余空格)：<br/>    月：201201,201205<br/>    季：2012A,2012B,2012C,2012D<br/>    年：2012,2013 <br>    至今：2013-<br>    最近：last10；接口内部会自动兼容新站时间编码 |

输出参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

接口示例

```python
import akshare as ak

macro_china_nbs_region_df = ak.macro_china_nbs_region(kind="分省季度数据", path="国民经济核算 > 地区生产总值", period="last3", indicator=None, region="河北省")
print(macro_china_nbs_region_df)

macro_china_nbs_region_df = ak.macro_china_nbs_region(kind="分省季度数据", path="人民生活 > 居民人均可支配收入", indicator='居民人均可支配收入_累计值(元)', period="2022")
print(macro_china_nbs_region_df)
```

数据示例

```
region_gdp_df
河北省                                2023年第二季度   2023年第一季度  2022年第四季度
地区生产总值_累计值(亿元)                 20779.0        10041.0        42370.0
地区生产总值指数(上年同期=100)_累计值(%)    106.1         105.1          103.8

region_income_df
居民人均可支配收入_累计值(元)      2022年第四季度     2022年第三季度     2022年第二季度  2022年第一季度
北京市                            77414.548842      58596.590041     39391.260057    20630.0
天津市                            48976.122565      38934.695987     25453.536929    14082.0
河北省                            30867.016699      22783.082852     14998.243977     7863.0
...                               ...               ...              ...              ...
新疆维吾尔自治区                   27062.738782      16553.955250     10747.883634     5713.0
```
