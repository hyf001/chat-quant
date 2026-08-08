---
title: "stock_cg_guarantee_cninfo - 对外担保"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_cg_guarantee_cninfo

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 机构推荐 > 对外担保
- 描述: 巨潮资讯-数据中心-专题统计-公司治理-对外担保
- 目标地址: https://webapi.cninfo.com.cn/#/thematicStatistics
- 限量: 单次指定 symbol 和起始日期的对外担保数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 对外担保

接口: stock_cg_guarantee_cninfo

目标地址: https://webapi.cninfo.com.cn/#/thematicStatistics

描述: 巨潮资讯-数据中心-专题统计-公司治理-对外担保

限量: 单次指定 symbol 和起始日期的对外担保数据

输入参数

| 名称         | 类型  | 描述                                                        |
|------------|-----|-----------------------------------------------------------|
| symbol     | str | symbol="全部"; choice of {"全部", "深市主板", "沪市", "创业板", "科创板"} |
| start_date | str | start_date="20180630"                                     |
| end_date   | str | end_date="20210927"                                       |

输出参数

| 名称          | 类型      | 描述       |
|-------------|---------|----------|
| 证劵代码        | object  | -        |
| 证券简称        | object  | -        |
| 公告统计区间      | object  | -        |
| 担保笔数        | int64   | -        |
| 担保金额        | float64 | 注意单位: 万元 |
| 归属于母公司所有者权益 | float64 | 注意单位: 万元 |
| 担保金融占净资产比例  | float64 | 注意单位: %  |

接口示例

```python
import akshare as ak

stock_corporate_governance_guarantee_df = ak.stock_cg_guarantee_cninfo(symbol="全部", start_date="20180630", end_date="20210927")
print(stock_corporate_governance_guarantee_df)
```

数据示例

```
      证券代码  证券简称  ... 归属于母公司所有者权益  担保金融占净资产比例
0     000683  远兴能源  ...  1416683.55       93.19
1     000698  沈阳化工  ...   152836.81     1413.11
2     000732  ST泰禾  ...   387149.45    11353.60
3     000751  锌业股份  ...   358173.79       64.21
4     000818  航锦科技  ...   368945.73       30.90
...      ...   ...  ...         ...         ...
3075  688025   杰普特  ...   196706.09        5.08
3076  300822  贝仕达克  ...   126328.08        3.96
3077  300907  康平科技  ...    78724.85       10.16
3078  688296  和达科技  ...    70535.91        1.42
3079  300632  光莆股份  ...   189380.21       24.29
[3080 rows x 7 columns]
```
