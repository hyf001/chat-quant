---
title: "stock_register_sz - 深圳主板"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_register_sz

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > IPO审核信息 > 科创板 > 深圳主板
- 描述: 东方财富网-数据中心-新股数据-IPO审核信息-深圳主板
- 目标地址: https://data.eastmoney.com/xg/ipo/
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 深圳主板

接口: stock_register_sz

目标地址: https://data.eastmoney.com/xg/ipo/

描述: 东方财富网-数据中心-新股数据-IPO审核信息-深圳主板

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称     | 类型     | 描述  |
|--------|--------|-----|
| 序号     | int32  | -   |
| 发行人全称  | object | -   |
| 审核状态   | object | -   |
| 注册地    | object | -   |
| 证监会行业  | object | -   |
| 保荐机构   | object | -   |
| 律师事务所  | object | -   |
| 会计师事务所 | object | -   |
| 更新日期   | object | -   |
| 受理日期   | object | -   |
| 拟上市地点  | object | -   |
| 招股说明书  | object | -   |

接口示例

```python
import akshare as ak

stock_register_sz_df = ak.stock_register_sz()
print(stock_register_sz_df)
```

数据示例

```
     序号             企业名称    最新状态 注册地            行业          保荐机构  \
0      1    山东金鸿新材料股份有限公司      撤回  山东      非金属矿物制品业    中泰证券股份有限公司
1      2    金永和精工制造股份有限公司      撤回  山东         汽车制造业    中德证券有限责任公司
2      3     江苏大艺科技股份有限公司      撤回  江苏       通用设备制造业  中信建投证券股份有限公司
3      4   浙江新纳材料科技股份有限公司      撤回  浙江  化学原料及化学制品制造业    中信证券股份有限公司
4      5  深圳宏业基岩土科技股份有限公司      中止  广东          None    招商证券股份有限公司
..   ...              ...     ...  ..           ...           ...
512  513         深圳市科达利实业  已通过发审会  广东          None  中国国际金融股份有限公司
513  514         浙江威星智能仪表  已通过发审会  浙江          None    东吴证券股份有限公司
514  515         高斯贝尔数码科技  已通过发审会  湖南          None    招商证券股份有限公司
515  516           盐津铺子食品  已通过发审会  湖南          None    西部证券股份有限公司
516  517           广东英联包装  已通过发审会  广东          None    国海证券股份有限公司
           律师事务所              会计师事务所        更新日期        受理日期 拟上市地点  \
0     北京市汉坤律师事务所    永拓会计师事务所(特殊普通合伙)  2024-06-17  2023-12-28   深主板
1      北京大成律师事务所  信永中和会计师事务所(特殊普通合伙)  2024-06-16  2023-06-30   深主板
2    国浩律师(上海)事务所    天健会计师事务所(特殊普通合伙)  2024-06-15  2023-03-02   深主板
3     北京市康达律师事务所    天健会计师事务所(特殊普通合伙)  2024-06-14  2023-03-01   深主板
4      广东华商律师事务所    大华会计师事务所(特殊普通合伙)  2024-06-13         NaT   深主板
..           ...                 ...         ...         ...   ...
512    广东信达律师事务所    瑞华会计师事务所(特殊普通合伙)  2017-02-09         NaT   深主板
513  国浩律师(杭州)事务所    天健会计师事务所(特殊普通合伙)  2017-01-19         NaT   深主板
514    湖南启元律师事务所    天健会计师事务所(特殊普通合伙)  2017-01-12         NaT   深主板
515    湖南启元律师事务所    天健会计师事务所(特殊普通合伙)  2017-01-05         NaT   深主板
516    北京国枫律师事务所    立信会计师事务所(特殊普通合伙)  2017-01-05         NaT   深主板
                                                 招股说明书
0    https://pdf.dfcfw.com/pdf/H2_AN202312281615219...
1    https://pdf.dfcfw.com/pdf/H2_AN202312261614904...
2    https://pdf.dfcfw.com/pdf/H2_AN202312271615081...
3    https://pdf.dfcfw.com/pdf/H2_AN202312291615534...
4    https://pdf.dfcfw.com/pdf/H2_AN202307061592065...
..                                                 ...
512  https://pdf.dfcfw.com/pdf/H2_AN201702190353685...
513  https://pdf.dfcfw.com/pdf/H2_AN201702060321215...
514  https://pdf.dfcfw.com/pdf/H2_AN201701250290802...
515  https://pdf.dfcfw.com/pdf/H2_AN201701180274398...
516  https://pdf.dfcfw.com/pdf/H2_AN201701180274398...
[517 rows x 12 columns]
```
