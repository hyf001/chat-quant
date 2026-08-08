---
title: "macro_china_nbs_nation - 国家统计局全国数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_nbs_nation

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 国家统计局通用接口 > 国家统计局全国数据
- 描述: 国家统计局全国数据通用接口，包括月度数据、季度数据、年度数据，具体指标见国家统计局新站官网。
- 目标地址: https://data.stats.gov.cn/dg/website/page.html#/pc/national/yearData
- 限量: 根据参数返回指定数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 国家统计局全国数据

接口: macro_china_nbs_nation

目标地址: https://data.stats.gov.cn/dg/website/page.html#/pc/national/yearData

描述: 国家统计局全国数据通用接口，包括月度数据、季度数据、年度数据，具体指标见国家统计局新站官网。

限量: 根据参数返回指定数据

输入参数

| 名称     | 类型  | 描述                                                                                                                                                 |
|--------|-----|----------------------------------------------------------------------------------------------------------------------------------------------------|
| kind   | str | 数据类别，包括：月度数据、季度数据、年度数据。                                                                                                                            |
| path   | str | 数据路径， 需与kind参数匹配，具体见官网，多层级之间使用  > 连接 。<br> 示例：<br>    国民经济核算 > 支出法国内生产总值<br>   人口 > 总人口<br>   金融业 > 保险系统机构、人员数 > 保险系统机构数                           |
| period | str | 时间区间 <br/>参考格式如下(英文逗号分割，且不能有多余空格)：<br/>    月：201201,201205<br/>    季：2012A,2012B,2012C,2012D<br/>    年：2012,2013 <br>    至今：2013-<br>    最近：last10；接口内部会自动兼容新站时间编码 |

输出参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

接口示例

```python
import akshare as ak

macro_china_nbs_nation_df = ak.macro_china_nbs_nation(kind="年度数据", path="人口 > 总人口", period="LAST5")
print(macro_china_nbs_nation_df)
```

数据示例

```
                  2022年    2021年    2020年      2019年        2018年
年末总人口(万人)  141175.0  141260.0  141212.0  141008.0000  140541.000000
男性人口(万人)    72206.0   72311.0   72357.0   72039.0000   71863.871426
女性人口(万人)    68969.0   68949.0   68855.0   68969.0000   68677.128574
城镇人口(万人)    92071.0   91425.0   90220.0   88426.1168   86432.715000
乡村人口(万人)    49104.0   49835.0   50992.0   52581.8832   54108.285000
```
