---
title: "bond_info_cm - 债券查询"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, bond, parameters, returns, example]
sources: [raw/data-dictionary/bond/bond.md]
confidence: high
---
# bond_info_cm

- 分类: [[bond-bond|AKShare 债券数据]]
- 主题路径: AKShare 债券数据 > 债券查询
- 描述: 中国外汇交易中心暨全国银行间同业拆借中心-数据-债券信息-信息查询
- 目标地址: https://www.chinamoney.com.cn/chinese/scsjzqxx/
- 来源页面: https://akshare.akfamily.xyz/data/bond/bond.html

## 相关

- [[bond-bond|AKShare 债券数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 债券查询

接口: bond_info_cm

目标地址: https://www.chinamoney.com.cn/chinese/scsjzqxx/

描述: 中国外汇交易中心暨全国银行间同业拆借中心-数据-债券信息-信息查询

输入参数

| 名称          | 类型  | 描述                                                      |
|-------------|-----|---------------------------------------------------------|
| bond_name   | str | bond_name=""; 默认为空                                      |
| bond_code   | str | bond_code=""; 默认为空                                      |
| bond_issue  | str | bond_issue=""; 默认为空, 通过 ak.bond_info_cm_query() 查询相关参数  |
| bond_type   | str | bond_type=""; 默认为空, 通过 ak.bond_info_cm_query() 查询相关参数   |
| coupon_type | str | coupon_type=""; 默认为空, 通过 ak.bond_info_cm_query() 查询相关参数 |
| issue_year  | str | issue_year=""; 默认为空                                     |
| underwriter | str | underwriter=""; 默认为空, 通过 ak.bond_info_cm_query() 查询相关参数 |
| grade       | str | grade=""; 默认为空                                          |

输出参数

| 名称       | 类型     | 描述  |
|----------|--------|-----|
| 债券简称     | object | -   |
| 债券代码     | object | -   |
| 发行人/受托机构 | object | -   |
| 债券类型     | object | -   |
| 发行日期     | object | -   |
| 最新债项评级   | object | -   |
| 查询代码     | object | -   |

接口示例

```python
import akshare as ak

bond_info_cm_df = ak.bond_info_cm(bond_name="", bond_code="", bond_issue="", bond_type="短期融资券", coupon_type="零息式", issue_year="2019", grade="A-1", underwriter="重庆农村商业银行股份有限公司")
print(bond_info_cm_df)
```

数据示例

```
          债券简称       债券代码      发行人/受托机构   债券类型        发行日期 最新债项评级        查询代码
0   19渝机电CP002  041900474  重庆机电控股(集团)公司  短期融资券  2019-12-16    A-1  06006vznk4
1   19渝机电CP001  041900229  重庆机电控股(集团)公司  短期融资券  2019-06-13    A-1  786875qtsi
2  19万林投资CP001  041900126  重庆万林投资发展有限公司  短期融资券  2019-03-25    A-1  695327xh9n
```
