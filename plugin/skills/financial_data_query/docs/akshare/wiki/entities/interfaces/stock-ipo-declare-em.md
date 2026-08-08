---
title: "stock_ipo_declare_em - 首发申报信息"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_ipo_declare_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 首发申报信息
- 描述: 东方财富网-数据中心-新股申购-首发申报信息-首发申报企业信息
- 目标地址: https://data.eastmoney.com/xg/xg/sbqy.html
- 限量: 单次返回所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 首发申报信息

接口: stock_ipo_declare_em

目标地址: https://data.eastmoney.com/xg/xg/sbqy.html

描述: 东方财富网-数据中心-新股申购-首发申报信息-首发申报企业信息

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称     | 类型     | 描述 |
|--------|--------|----|
| 序号     | int64  | -  |
| 企业名称   | object | -  |
| 最新状态   | object | -  |
| 注册地    | object | -  |
| 保荐机构   | object | -  |
| 律师事务所  | object | -  |
| 会计师事务所 | object | -  |
| 拟上市地点  | object | -  |
| 更新日期   | object | -  |
| 招股说明书  | object | -  |

接口示例

```python
import akshare as ak

stock_ipo_declare_em_df = ak.stock_ipo_declare_em()
print(stock_ipo_declare_em_df)
```

数据示例

```
      序号     申报企业 拟上市地  ...               会计师事务所        律师事务所      备注
0      1     奥精医疗科技股份有限公司  科创板  ...     立信会计师事务所(特殊普通合伙)  北京观韬中茂律师事务所  进一步问询中
1      2       爱威科技股份有限公司  科创板  ...     天健会计师事务所(特殊普通合伙)    湖南启元律师事务所  进一步问询中
2      3   北京弘成立业科技股份有限公司  创业板  ...     大华会计师事务所(特殊普通合伙)   北京市君合律师事务所  进一步问询中
3      4   北京海天瑞声科技股份有限公司  科创板  ...  毕马威华振会计师事务所(特殊普通合伙)   北京市天元律师事务所  进一步问询中
4      5  北京挖金客信息科技股份有限公司  创业板  ...     容诚会计师事务所(特殊普通合伙)  国浩律师(北京)事务所  进一步问询中
..   ...              ...  ...  ...                  ...          ...     ...
106  107   浙江嘉益保温科技股份有限公司  创业板  ...     天健会计师事务所(特殊普通合伙)   北京市金杜律师事务所  进一步问询中
107  108   浙江日发纺织机械股份有限公司  创业板  ...     天健会计师事务所(特殊普通合伙)    浙江天册律师事务所  进一步问询中
108  109     浙江泰福泵业股份有限公司  创业板  ...     天健会计师事务所(特殊普通合伙)  国浩律师(杭州)事务所  进一步问询中
109  110     中兰环保科技股份有限公司  创业板  ...     立信会计师事务所(特殊普通合伙)    北京国枫律师事务所  进一步问询中
110  111   中联云港数据科技股份有限公司  创业板  ...   天职国际会计师事务所(特殊普通合伙)  国浩律师(北京)事务所  进一步问询中
```
