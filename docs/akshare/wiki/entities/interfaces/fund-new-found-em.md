---
title: "fund_new_found_em - 新发基金"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_new_found_em

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 新发基金
- 描述: 天天基金网-基金数据-新发基金-新成立基金
- 目标地址: https://fund.eastmoney.com/data/xinfound.html
- 限量: 单次返回所有新发基金数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

### 新发基金

接口: fund_new_found_em

目标地址: https://fund.eastmoney.com/data/xinfound.html

描述: 天天基金网-基金数据-新发基金-新成立基金

限量: 单次返回所有新发基金数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称    | 类型      | 描述       |
|-------|---------|----------|
| 基金代码  | object  | -        |
| 基金简称  | object  | -        |
| 发行公司  | object  | -        |
| 基金类型  | object  | -        |
| 集中认购期 | object  | -        |
| 募集份额  | float64 | 注意单位: 亿份 |
| 成立日期  | object  | -        |
| 成立来涨幅 | float64 | 注意单位: %  |
| 基金经理  | object  | -        |
| 申购状态  | object  | -        |
| 优惠费率  | float64 | 注意单位: %  |

接口示例

```python
import akshare as ak

fund_new_found_em_df = ak.fund_new_found_em()
print(fund_new_found_em_df)
```

数据示例

```
        基金代码                      基金简称    发行公司  ...   基金经理  申购状态  优惠费率
0     019879              万家周期驱动股票发起式A    万家基金  ...     叶勇  开放申购  0.15
1     019873                     长城短债E    长城基金  ...    邹德立   限大额  0.00
2     019872                     长城短债D    长城基金  ...    邹德立   限大额  0.03
3     019880              万家周期驱动股票发起式C    万家基金  ...     叶勇  开放申购  0.00
4     019671  广发中证香港创新药ETF发起式联接(QDII)C    广发基金  ...     刘杰  开放申购  0.00
      ...                       ...     ...  ...    ...   ...   ...
7310  008411                  博时富信纯债债券    博时基金  ...     陈黎   限大额  0.08
7311  008135                  华宸未来价值先锋  华宸未来基金  ...    张翼翔  开放申购  0.15
7312  007729     招商普盛全球配置(QDII-FOF)人民币    招商基金  ...    范刚强  开放申购  0.15
7313  008055            汇添富中债7-10年国开债C   汇添富基金  ...  何旻,李伟  开放申购  0.00
7314  008054            汇添富中债7-10年国开债A   汇添富基金  ...  何旻,李伟  开放申购  0.05
[7315 rows x 11 columns]
```
