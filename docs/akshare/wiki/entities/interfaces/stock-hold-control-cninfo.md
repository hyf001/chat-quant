---
title: "stock_hold_control_cninfo - 实际控制人持股变动"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_hold_control_cninfo

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 机构推荐 > 实际控制人持股变动
- 描述: 巨潮资讯-数据中心-专题统计-股东股本-实际控制人持股变动
- 目标地址: https://webapi.cninfo.com.cn/#/thematicStatistics
- 限量: 单次指定 symbol 的实际控制人持股变动数据, 从 2010 开始
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 实际控制人持股变动

接口: stock_hold_control_cninfo

目标地址: https://webapi.cninfo.com.cn/#/thematicStatistics

描述: 巨潮资讯-数据中心-专题统计-股东股本-实际控制人持股变动

限量: 单次指定 symbol 的实际控制人持股变动数据, 从 2010 开始

输入参数

| 名称     | 类型  | 描述                                                                         |
|--------|-----|----------------------------------------------------------------------------|
| symbol | str | symbol="全部"; choice of {"单独控制", "实际控制人", "一致行动人", "家族控制", "全部"}; 从 2010 开始 |

输出参数

| 名称      | 类型      | 描述       |
|---------|---------|----------|
| 证劵代码    | object  | -        |
| 证券简称    | object  | -        |
| 变动日期    | object  | -        |
| 实际控制人名称 | object  | -        |
| 控股数量    | float64 | 注意单位: 万股 |
| 控股比例    | float64 | 注意单位: %  |
| 直接控制人名称 | object  | -        |
| 控制类型    | object  | -        |

接口示例

```python
import akshare as ak

stock_hold_control_cninfo_df = ak.stock_hold_control_cninfo(symbol="全部")
print(stock_hold_control_cninfo_df)
```

数据示例

```
        证券代码  证券简称  ...                                        直接控制人名称   控制类型
0     601777  力帆股份  ...                 尹明善\r;陈巧凤\r;尹喜地\r;尹索微\r;重庆力帆控股有限公司  一致行动人
1     002460  赣锋锂业  ...                           李良彬;黄闻;熊剑浪;李良学;罗顺香\r;李华彪  一致行动人
2     000966  长源电力  ...                                           中国国电集团公司   单独控制
3     600019  宝钢股份  ...                                           宝钢集团有限公司   单独控制
4     600031  三一重工  ...                                       三一集团有限公司;梁稳根   单独控制
...      ...   ...  ...                                                ...    ...
5391  600354  敦煌种业  ...                                     酒泉钢铁(集团)有限责任公司   单独控制
5392  600208  新湖中宝  ...                          衢州工业投资集团有限公司;衢州工业发展集团有限公司   单独控制
5393  600399  抚顺特钢  ...  江苏沙钢集团有限公司;沙钢集团的股东张家港市保税区润源不锈钢贸易有限公司;宁波梅山保税港区锦...  一致行动人
5394  002075  沙钢股份  ...  江苏沙钢集团有限公司;宁波梅山保税港区锦程沙洲股权投资有限公司;张家港保税区润源不锈钢贸易有限公司   单独控制
5395  301552  科力装备  ...                   张万武;郭艳芝;张子恒;天津科达企业管理咨询合伙企业(有限合伙)   家族控制
[5396 rows x 8 columns]
```
