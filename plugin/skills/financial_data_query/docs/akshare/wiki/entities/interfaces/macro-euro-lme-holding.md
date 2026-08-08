---
title: "macro_euro_lme_holding - 持仓报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_euro_lme_holding

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 重要机构 > 伦敦金属交易所 > 持仓报告
- 描述: 伦敦金属交易所(LME)-持仓报告, 数据区间从 20151022-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_lme_traders_report
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 持仓报告

接口: macro_euro_lme_holding

目标地址: https://datacenter.jin10.com/reportType/dc_lme_traders_report

描述: 伦敦金属交易所(LME)-持仓报告, 数据区间从 20151022-至今

限量: 单次返回所有历史数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称     | 类型 | 描述  |
|--------|----|-----|
| 日期     | -  | -   |
| 铜-多头仓位 | -  | -   |
| ...    | -  | ... |
| 铝-净仓位  | -  | -   |

接口示例

```python
import akshare as ak

macro_euro_lme_holding_df = ak.macro_euro_lme_holding()
print(macro_euro_lme_holding_df)
```

数据示例

```
        日期     铜-多头仓位    铜-空头仓位  ...     铝-多头仓位     铝-空头仓位      铝-净仓位
0    2015-10-22  107991.00 -84529.00  ...  327120.00 -304606.00  631726.00
1    2015-10-23  107881.00 -85003.00  ...  326996.00 -304797.00  631793.00
2    2015-10-26  108904.00 -84484.00  ...  327814.00 -305974.00  633788.00
3    2015-10-27  108818.00 -83438.00  ...  331239.00 -305348.00  636587.00
4    2015-10-28  109631.00 -84558.00  ...  331586.00 -302432.00  634018.00
..          ...        ...       ...  ...        ...        ...        ...
751  2021-08-06    8785.16  12656.84  ...   37711.94   42438.71   -4726.77
752  2021-08-13    8872.87  12349.74  ...   37007.09   41819.17   -4812.08
753  2021-08-20    7676.48  10610.98  ...   35348.31   41029.67   -5681.36
754  2021-08-27    8262.28  11853.99  ...   36410.21   40359.70   -3949.49
755  2021-09-03    7453.93  10574.36  ...   35312.19   42067.01   -6754.82
[756 rows x 19 columns]
```
