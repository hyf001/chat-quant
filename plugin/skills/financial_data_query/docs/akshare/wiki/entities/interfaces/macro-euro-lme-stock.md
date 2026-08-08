---
title: "macro_euro_lme_stock - 库存报告"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_euro_lme_stock

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 重要机构 > 伦敦金属交易所 > 库存报告
- 描述: 伦敦金属交易所(LME)-库存报告, 数据区间从 20140702-至今
- 目标地址: https://datacenter.jin10.com/reportType/dc_lme_report
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 库存报告

接口: macro_euro_lme_stock

目标地址: https://datacenter.jin10.com/reportType/dc_lme_report

描述: 伦敦金属交易所(LME)-库存报告, 数据区间从 20140702-至今

限量: 单次返回所有历史数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称     | 类型  | 描述  |
|--------|-----|-----|
| 日期     | -   | -   |
| 铜-库存   | -   | -   |
| ...    | ... | ... |
| 镍-注销仓单 | -   | -   |

接口示例

```python
import akshare as ak

macro_euro_lme_stock_df = ak.macro_euro_lme_stock()
print(macro_euro_lme_stock_df)
```

数据示例

```
        日期    铜-库存  铜-注册仓单  铜-注销仓单  ...   铝-注销仓单    镍-库存  镍-注册仓单  镍-注销仓单
0     2014-07-02  156775  128475   28300  ...  2990950  305394  192672  112722
1     2014-07-03  157050  129250   27800  ...  2983375  304938  192972  111966
2     2014-07-04  156500  129250   27250  ...  2974775  304536  192900  111636
3     2014-07-07  159350  126350   33000  ...  2965600  305394  194334  111060
4     2014-07-08  158050  126975   31075  ...  2963275  305280  196404  108876
          ...     ...     ...     ...  ...      ...     ...     ...     ...
2144  2024-03-25  117900   99250   18650  ...   218650   77454   71178    6276
2145  2024-03-26  117400   97725   19675  ...   214825   77076   71148    5928
2146  2024-03-27  113100   97725   15375  ...   214075   76836   70716    6120
2147  2024-03-28  112475   97775   14700  ...   212025   77148   70374    6774
2148  2024-04-02  111925   97775   14150  ...   209175   77772   68916    8856
[2149 rows x 19 columns]
```
