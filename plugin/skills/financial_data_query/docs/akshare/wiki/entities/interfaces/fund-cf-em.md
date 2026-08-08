---
title: "fund_cf_em - 基金拆分"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_cf_em

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 分红送配 > 基金拆分
- 描述: 天天基金网-基金数据-分红送配-基金拆分
- 目标地址: http://fund.eastmoney.com/data/fundchaifen.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 基金拆分

接口: fund_cf_em

目标地址: http://fund.eastmoney.com/data/fundchaifen.html

描述: 天天基金网-基金数据-分红送配-基金拆分

限量: 单次返回所有历史数据

输入参数

| 名称   | 类型  | 描述                                                                                                                                                                                                                             |
|------|-----|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| year | str | year="2025"; 最早支持 2005 年                                                                                                                                                                                                       |
| typ  | str | typ=""; 空串表示全部; choice of {"", "指数型-其他", "指数型-海外股票", "指数型-固收", "指数型-股票", "债券型-中短债", "债券型-长债", "债券型-可转债", "债券型-混合债", "债券型-混合一级", "债券型-混合二级", "商品（不含QDII）", "货币型", "混合型-平衡", "混合型-偏债", "混合型-偏股", "混合型-灵活", "股票型", "QDII", "FOF"} |
| rank | str | rank="FSRQ"; 排序字段; choice of {"BZDM", "ABBNAME", "FSRQ", "FHFCZ"}; "BZDM": 基金代码, "ABBNAME": 基金简称, "FSRQ": 拆分折算日, "FHFCZ": 拆分折算(每份)                                                                                             |
| sort | str | sort="desc"; choice of {"asc", "desc"}                                                                                                                                                                                         |
| page | int | page=-1; 请求第page页数据; -1 表示全部页面                                                                                                                                                                                                 |

输出参数

| 名称    | 类型      | 描述       |
|-------|---------|----------|
| 序号    | int64   | -        |
| 基金代码  | object  | -        |
| 基金简称  | object  | -        |
| 拆分折算日 | object  | -        |
| 拆分类型  | object  | -        |
| 拆分折算  | float64 | 注意单位: 每份 |

接口示例

```python
import akshare as ak

fund_cf_em_df = ak.fund_cf_em(year="2025")
print(fund_cf_em_df)
```

数据示例

```
   序号   基金代码           基金简称       拆分折算日  拆分类型      拆分折算
0    1  159220    华宝标普港股通低波红利ETF  2025-11-07  份额分拆  2.000000
1    2  562000       华宝中证A100ETF  2025-11-07  份额分拆  2.000000
2    3  562080   华宝沪深300自由现金流ETF  2025-11-07  份额分拆  2.000000
3    4  159583     富国中证通信设备主题ETF  2025-11-05  份额分拆  2.000000
4    5  588860  工银瑞信上证科创板生物医药ETF  2025-10-24  份额分拆  2.000000
..  ..     ...               ...         ...   ...       ...
77  78  159396    博时深证基准做市信用债ETF  2025-01-17  份额折算  0.010000
78  79  511110   易方达上证基准做市公司债ETF  2025-01-17  份额折算  0.010000
79  80  511200    华夏上证基准做市公司债ETF  2025-01-17  份额折算  0.010000
80  81  511070    南方上证基准做市公司债ETF  2025-01-14  份额折算  0.010000
81  82  000465     景顺长城鑫月薪定期支付债券  2025-01-09  份额折算  1.056828
[82 rows x 6 columns]
```
