---
title: "stock_register_sh - 上海主板"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_register_sh

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > IPO审核信息 > 科创板 > 上海主板
- 描述: 东方财富网-数据中心-新股数据-IPO审核信息-上海主板
- 目标地址: https://data.eastmoney.com/xg/ipo/
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

###### 上海主板

接口: stock_register_sh

目标地址: https://data.eastmoney.com/xg/ipo/

描述: 东方财富网-数据中心-新股数据-IPO审核信息-上海主板

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

stock_register_sh_df = ak.stock_register_sh()
print(stock_register_sh_df)
```

数据示例

```
      序号              企业名称       最新状态 注册地          行业              保荐机构  \
0      1      浙江亘古电缆股份有限公司         终止  浙江  电气机械和器材制造业        招商证券股份有限公司
1      2  上海生生医药冷链科技股份有限公司         终止  上海  多式联运和运输代理业      中国国际金融股份有限公司
2      3    新疆凯龙清洁能源股份有限公司         终止  新疆  开采专业及辅助性活动        东兴证券股份有限公司
3      4      广州三晶电气股份有限公司  已收到注册申请材料  广东        None        民生证券股份有限公司
4      5      合肥汇通控股股份有限公司  已收到注册申请材料  安徽        None      中银国际证券股份有限公司
..   ...               ...        ...  ..         ...               ...
874  875             上海数据港     已通过发审会  上海        None      中信建投证券股份有限公司
875  876            镇海石化工程     已通过发审会  浙江        None        浙商证券股份有限公司
876  877          浙江德创环保科技     已通过发审会  浙江        None        民生证券股份有限公司
877  878           重庆建工集团*     已通过发审会  重庆        None        华融证券股份有限公司
878  879            大连百傲化学     已通过发审会  辽宁        None  申万宏源证券承销保荐有限责任公司
           律师事务所              会计师事务所        更新日期        受理日期 拟上市地点  \
0      北京国枫律师事务所    天健会计师事务所(特殊普通合伙)  2024-06-17  2023-03-03   沪主板
1    上海市锦天城律师事务所    立信会计师事务所(特殊普通合伙)  2024-06-17  2023-06-30   沪主板
2     北京市中伦律师事务所  信永中和会计师事务所(特殊普通合伙)  2024-06-14  2023-06-15   沪主板
3      国信信扬律师事务所    立信会计师事务所(特殊普通合伙)  2024-06-13         NaT   沪主板
4      安徽天禾律师事务所    容诚会计师事务所(特殊普通合伙)  2024-06-13         NaT   沪主板
..           ...                 ...         ...         ...   ...
874  上海市锦天城律师事务所    立信会计师事务所(特殊普通合伙)  2017-01-05         NaT   沪主板
875   北京市天元律师事务所    天健会计师事务所(特殊普通合伙)  2017-01-05         NaT   沪主板
876   北京市天元律师事务所    天健会计师事务所(特殊普通合伙)  2017-01-05         NaT   沪主板
877   北京市金杜律师事务所    大信会计师事务所(特殊普通合伙)  2017-01-05         NaT   沪主板
878    北京德恒律师事务所    瑞华会计师事务所(特殊普通合伙)  2017-01-05         NaT   沪主板
                                                 招股说明书
0    https://pdf.dfcfw.com/pdf/H2_AN202303031584027...
1    https://pdf.dfcfw.com/pdf/H2_AN202306301591956...
2    https://pdf.dfcfw.com/pdf/H2_AN202306151590972...
3    https://pdf.dfcfw.com/pdf/H2_AN202303031584027...
4    https://pdf.dfcfw.com/pdf/H2_AN202303031584027...
..                                                 ...
874  https://pdf.dfcfw.com/pdf/H2_AN201701150271855...
875  https://pdf.dfcfw.com/pdf/H2_AN201701180277302...
876  https://pdf.dfcfw.com/pdf/H2_AN201701170274362...
877  https://pdf.dfcfw.com/pdf/H2_AN201701170274362...
878  https://pdf.dfcfw.com/pdf/H2_AN201701160272431...
[879 rows x 12 columns]
```
