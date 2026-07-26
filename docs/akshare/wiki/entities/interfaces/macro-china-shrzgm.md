---
title: "macro_china_shrzgm - 社会融资规模增量统计"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_shrzgm

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 国民经济运行状况 > 经济状况 > 社会融资规模增量统计
- 描述: 商务数据中心-国内贸易-社会融资规模增量统计, 数据区间从 201501-至今
- 目标地址: http://data.mofcom.gov.cn/gnmy/shrzgm.shtml
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 社会融资规模增量统计

接口: macro_china_shrzgm

目标地址: http://data.mofcom.gov.cn/gnmy/shrzgm.shtml

描述: 商务数据中心-国内贸易-社会融资规模增量统计, 数据区间从 201501-至今

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称             | 类型      | 描述              |
|----------------|---------|-----------------|
| 月份             | object  | 年月              |
| 社会融资规模增量       | float64 | 注意单位: 亿元        |
| 其中-人民币贷款       | float64 | 注意单位: 亿元        |
| 其中-委托贷款外币贷款    | float64 | 注意单位: 折合人民币, 亿元 |
| 其中-委托贷款        | float64 | 注意单位: 亿元        |
| 其中-信托贷款        | float64 | 注意单位: 亿元        |
| 其中-未贴现银行承兑汇票   | float64 | 注意单位: 亿元        |
| 其中-企业债券        | float64 | 注意单位: 亿元        |
| 其中-非金融企业境内股票融资 | float64 | 注意单位: 亿元        |

接口示例

```python
import akshare as ak

macro_china_shrzgm_df = ak.macro_china_shrzgm()
print(macro_china_shrzgm_df)
```

数据示例

```
        月份  社会融资规模增量  其中-人民币贷款  ...  其中-未贴现银行承兑汇票  其中-企业债券  其中-非金融企业境内股票融资
0   201501     20516     14708  ...          1946     1868           526.0
1   201502     13609     11437  ...          -592      716           542.0
2   201503     12433      9920  ...          -910     1344           639.0
3   201504     10582      8045  ...           -74     1616           597.0
4   201505     12397      8510  ...           961     1710           584.0
..     ...       ...       ...  ...           ...      ...             ...
82  202111     25983     13021  ...          -383     4006          1294.0
83  202112     23682     10350  ...         -1419     2167          2075.0
84  202201     61750     41988  ...          4733     5829          1439.0
85  202202     11928      9084  ...         -4228     3377           585.0
86  202203     46531     32291  ...           287     3573           958.0
```
