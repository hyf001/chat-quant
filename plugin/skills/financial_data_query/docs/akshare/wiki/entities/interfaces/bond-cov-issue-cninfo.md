---
title: "bond_cov_issue_cninfo - 可转债发行"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, bond, parameters, returns, example]
sources: [raw/data-dictionary/bond/bond.md]
confidence: high
---
# bond_cov_issue_cninfo

- 分类: [[bond-bond|AKShare 债券数据]]
- 主题路径: AKShare 债券数据 > 债券发行 > 可转债发行
- 描述: 巨潮资讯-数据中心-专题统计-债券报表-债券发行-可转债发行
- 目标地址: https://webapi.cninfo.com.cn/#/thematicStatistics
- 来源页面: https://akshare.akfamily.xyz/data/bond/bond.html

## 相关

- [[bond-bond|AKShare 债券数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 可转债发行

接口: bond_cov_issue_cninfo

目标地址: https://webapi.cninfo.com.cn/#/thematicStatistics

描述: 巨潮资讯-数据中心-专题统计-债券报表-债券发行-可转债发行

输入参数

| 名称         | 类型  | 描述                    |
|------------|-----|-----------------------|
| start_date | str | start_date="20210913" |
| end_date   | str | end_date="20211112"   |

输出参数

| 名称              | 类型      | 描述       |
|-----------------|---------|----------|
| 债券代码            | object  | -        |
| 债券简称            | object  | -        |
| 公告日期            | object  | -        |
| 发行起始日           | object  | -        |
| 发行终止日           | object  | -        |
| 计划发行总量          | float64 | 注意单位: 万元 |
| 实际发行总量          | float64 | 注意单位: 万元 |
| 发行面值            | int64   | 注意单位: 元  |
| 发行价格            | float64 | 注意单位: 元  |
| 发行方式            | object  | -        |
| 发行对象            | object  | -        |
| 发行范围            | object  | -        |
| 承销方式            | object  | -        |
| 募资用途说明          | object  | -        |
| 初始转股价格          | float64 | 注意单位: 元  |
| 转股开始日期          | object  | -        |
| 转股终止日期          | object  | -        |
| 网上申购日期          | object  | -        |
| 网上申购代码          | object  | -        |
| 网上申购简称          | object  | -        |
| 网上申购数量上限        | float64 | 注意单位: 万元 |
| 网上申购数量下限        | float64 | 注意单位: 万元 |
| 网上申购单位          | float64 | -        |
| 网上申购中签结果公告日及退款日 | object  | -        |
| 优先申购日           | object  | -        |
| 配售价格            | float64 | 注意单位: 元  |
| 债权登记日           | object  | -        |
| 优先申购缴款日         | object  | -        |
| 转股代码            | object  | -        |
| 交易市场            | object  | -        |
| 债券名称            | object  | -        |

接口示例

```python
import akshare as ak

bond_cov_issue_cninfo_df = ak.bond_cov_issue_cninfo(start_date="20210913", end_date="20211112")
print(bond_cov_issue_cninfo_df)
```

数据示例

```
      债券代码  债券简称  ... 交易市场                                       债券名称
0   110083  苏租转债  ...  上交所             2021年江苏金融租赁股份有限公司公开发行A股可转换公司债券
1   123130  设研转债  ...  深交所  2021年河南省交通规划设计研究院股份有限公司创业板向不特定对象发行可转换公司债券
2   127050  麒麟转债  ...  深交所              2021年青岛森麒麟轮胎股份有限公司公开发行可转换公司债券
3   111001  山玻转债  ...  上交所               2021年山东玻纤集团股份有限公司公开发行可转换公司债券
4   113631  皖天转债  ...  上交所             2021年安徽省天然气开发股份有限公司公开发行可转换公司债券
5   123129  锦鸡转债  ...  深交所        2021年江苏锦鸡实业股份有限公司创业板向不特定对象发行可转换公司债券
6   127049  希望转2  ...  深交所                2021年新希望六和股份有限公司公开发行可转换公司债券
7   123128  首华转债  ...  深交所    2021年首华燃气科技(上海)股份有限公司创业板向不特定对象发行可转换公司债券
8   123127  耐普转债  ...  深交所           2021年江西耐普矿机股份有限公司向不特定对象发行可转换公司债券
9   110082  宏发转债  ...  上交所                 2021年宏发科技股份有限公司公开发行可转换公司债券
10  113630  赛伍转债  ...  上交所                  苏州赛伍应用技术股份有限公司公开发行可转换公司债券
11  127048  中大转债  ...  深交所                宁波中大力德智能传动股份有限公司公开发行可转换公司债券
12  127047  帝欧转债  ...  深交所                 2021年帝欧家居股份有限公司公开发行可转换公司债券
13  127046  百润转债  ...  深交所           2021年上海百润投资控股集团股份有限公司公开发行可转换公司债券
14  113629  泉峰转债  ...  上交所           2021年南京泉峰汽车精密技术股份有限公司公开发行可转换公司债券
[15 rows x 31 columns]
```
