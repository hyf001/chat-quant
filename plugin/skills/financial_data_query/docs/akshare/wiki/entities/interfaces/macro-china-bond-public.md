---
title: "macro_china_bond_public - 新债发行"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, macro, parameters, returns, example]
sources: [raw/data-dictionary/macro/macro.md]
confidence: high
---
# macro_china_bond_public

- 分类: [[macro-macro|AKShare 宏观数据]]
- 主题路径: AKShare 宏观数据 > 中国宏观 > 金融指标 > 新债发行
- 描述: 中国外汇交易中心暨全国银行间同业拆借中心-债券信息披露-新债发行; 近期债券发行数据
- 目标地址: https://www.chinamoney.com.cn/chinese/xzjfx/
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/macro/macro.html

## 相关

- [[macro-macro|AKShare 宏观数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 新债发行

接口: macro_china_bond_public

目标地址: https://www.chinamoney.com.cn/chinese/xzjfx/

描述: 中国外汇交易中心暨全国银行间同业拆借中心-债券信息披露-新债发行; 近期债券发行数据

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称    | 类型      | 描述       |
|-------|---------|----------|
| 债券全称  | object  | -        |
| 债券类型  | object  | -        |
| 发行日期  | object  | -        |
| 计息方式  | object  | -        |
| 价格    | float64 | 注意单位: 元  |
| 债券期限  | object  | -        |
| 计划发行量 | float64 | 注意单位: 亿元 |
| 债券评级  | object  | -        |

接口示例

```python
import akshare as ak

macro_china_bond_public_df = ak.macro_china_bond_public()
print(macro_china_bond_public_df)
```

数据示例

```
                                   债券全称    债券类型   发行日期  ...  债券期限  计划发行量  债券评级
0          江苏金融租赁股份有限公司2024年绿色金融债券(第一期)   普通金融债  01-16  ...    3年   15.0   AAA
1            杭银消费金融股份有限公司2024年金融债券(第一期)   普通金融债  01-12  ...    3年   10.0   AAA
2                      2024年记账式附息(一期)国债      国债  01-12  ...    5年  990.0  None
3              湖南银行股份有限公司2024年第006期同业存单    同业存单  01-12  ...    6月   11.0  None
4          北京农村商业银行股份有限公司2024年第012期同业存单    同业存单  01-12  ...    6月   19.0  None
..                                  ...     ...    ...  ...   ...    ...   ...
376    江西省国有资本运营控股集团有限公司2024年度第一期超短期融资券  超短期融资券  01-10  ...  180日   30.0  None
377  中国建筑第八工程局有限公司2024年度第二期超短期融资券(科创票据)  超短期融资券  01-10  ...   44日   30.0  None
378         厦门国贸集团股份有限公司2024年度第二期超短期融资券  超短期融资券  01-10  ...  120日   20.0  None
379          广东省环保集团有限公司2024年度第一期超短期融资券  超短期融资券  01-10  ...  260日    5.0  None
380  台州市路桥公共资产投资管理集团有限公司2024年度第一期超短期融资券  超短期融资券  01-10  ...  252日    6.3  None
[381 rows x 8 columns]
```
