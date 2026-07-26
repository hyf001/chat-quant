---
title: "bond_cov_stock_issue_cninfo - 可转债转股"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, bond, parameters, returns, example]
sources: [raw/data-dictionary/bond/bond.md]
confidence: high
---
# bond_cov_stock_issue_cninfo

- 分类: [[bond-bond|AKShare 债券数据]]
- 主题路径: AKShare 债券数据 > 债券发行 > 可转债转股
- 描述: 巨潮资讯-数据中心-专题统计-债券报表-债券发行-可转债转股
- 目标地址: https://webapi.cninfo.com.cn/#/thematicStatistics
- 来源页面: https://akshare.akfamily.xyz/data/bond/bond.html

## 相关

- [[bond-bond|AKShare 债券数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 可转债转股

接口: bond_cov_stock_issue_cninfo

目标地址: https://webapi.cninfo.com.cn/#/thematicStatistics

描述: 巨潮资讯-数据中心-专题统计-债券报表-债券发行-可转债转股

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称       | 类型      | 描述      |
|----------|---------|---------|
| 债券代码     | object  | -       |
| 债券简称     | object  | -       |
| 公告日期     | object  | -       |
| 转股代码     | object  | -       |
| 转股简称     | object  | -       |
| 转股价格     | float64 | 注意单位: 元 |
| 自愿转换期起始日 | object  | -       |
| 自愿转换期终止日 | object  | -       |
| 标的股票     | object  | -       |
| 债券名称     | object  | -       |

接口示例

```python
import akshare as ak

bond_cov_stock_issue_cninfo_df = ak.bond_cov_stock_issue_cninfo()
print(bond_cov_stock_issue_cninfo_df)
```

数据示例

```
       债券代码   债券简称  ...    标的股票                                 债券名称
0    113685  升24转债  ...  603305     2024年宁波旭升集团股份有限公司向不特定对象发行可转换公司债券
1    111019   宏柏转债  ...  605366    2024年江西宏柏新材料股份有限公司向不特定对象发行可转换公司债券
2    113684   湘泵转债  ...  603319      2024年湖南机油泵股份有限公司向不特定对象发行可转换公司债券
3    113683  伟24转债  ...  603568     2024年浙江伟明环保股份有限公司向不特定对象发行可转换公司债券
4    113682   益丰转债  ...  603939    2024年益丰大药房连锁股份有限公司向不特定对象发行可转换公司债券
..      ...    ...  ...     ...                                  ...
281  118029   富淼转债  ...  688350     2022年江苏富淼科技股份有限公司向不特定对象发行可转换公司债券
282  123172   漱玉转债  ...  301017  2022年漱玉平民大药房连锁股份有限公司向不特定对象发行可转换公司债券
283  123172   漱玉转债  ...  301017  2022年漱玉平民大药房连锁股份有限公司向不特定对象发行可转换公司债券
284  127078   优彩转债  ...  002998       2022年优彩环保资源科技股份有限公司公开发行可转换公司债券
285  127078   优彩转债  ...  002998       2022年优彩环保资源科技股份有限公司公开发行可转换公司债券
[286 rows x 10 columns]
```
