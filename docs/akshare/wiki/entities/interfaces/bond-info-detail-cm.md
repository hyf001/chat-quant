---
title: "bond_info_detail_cm - 债券基础信息"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, bond, parameters, returns, example]
sources: [raw/data-dictionary/bond/bond.md]
confidence: high
---
# bond_info_detail_cm

- 分类: [[bond-bond|AKShare 债券数据]]
- 主题路径: AKShare 债券数据 > 债券基础信息
- 描述: 中国外汇交易中心暨全国银行间同业拆借中心-数据-债券信息-信息查询-债券详情
- 目标地址: https://www.chinamoney.com.cn/chinese/zqjc/?bondDefinedCode=egfjh08154
- 来源页面: https://akshare.akfamily.xyz/data/bond/bond.html

## 相关

- [[bond-bond|AKShare 债券数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 债券基础信息

接口: bond_info_detail_cm

目标地址: https://www.chinamoney.com.cn/chinese/zqjc/?bondDefinedCode=egfjh08154

描述: 中国外汇交易中心暨全国银行间同业拆借中心-数据-债券信息-信息查询-债券详情

输入参数

| 名称     | 类型  | 描述                                                 |
|--------|-----|----------------------------------------------------|
| symbol | str | symbol="19万林投资CP001"; 通过 ak.bond_info_cm() 查询 债券简称 |

输出参数

| 名称    | 类型     | 描述  |
|-------|--------|-----|
| name  | object | -   |
| value | object | -   |

接口示例

```python
import akshare as ak

bond_info_detail_cm_df = ak.bond_info_detail_cm(symbol="19万林投资CP001")
print(bond_info_detail_cm_df)
```

数据示例

```
        name                       value
0        bondFullName  重庆万林投资发展有限公司2019年度第一期短期融资券
1     bondDefinedCode                  695327xh9n
2            bondName                 19万林投资CP001
3            bondCode                   041900126
4            isinCode                         ---
..                ...                         ...
59        chrgngMthds                         ---
60             crdtEv                         ---
61     brchStlmntMthd                         ---
62  rgstrtnCnfrmtnDay                         ---
63             inptTp                           0
[64 rows x 2 columns]
```
