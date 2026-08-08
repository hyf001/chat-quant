---
title: "fund_open_fund_daily_em - 开放式基金-实时数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_open_fund_daily_em

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金净值 > 开放式基金-实时数据
- 描述: 东方财富网-天天基金网-基金数据, 此接口在每个交易日 **16:00-23:00** 更新当日的最新开放式基金净值数据
- 目标地址: http://fund.eastmoney.com/fund.html#os_0;isall_0;ft_;pt_1
- 限量: 单次返回当前时刻所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 开放式基金-实时数据

接口: fund_open_fund_daily_em

目标地址: http://fund.eastmoney.com/fund.html#os_0;isall_0;ft_;pt_1

描述: 东方财富网-天天基金网-基金数据, 此接口在每个交易日 **16:00-23:00** 更新当日的最新开放式基金净值数据

限量: 单次返回当前时刻所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称        | 类型    | 描述      |
|-----------|-------|---------|
| 基金代码      | str   | -       |
| 基金简称      | str   | -       |
| 单位净值      | float | 随时间变动   |
| 累计净值      | float | 随时间变动   |
| 前交易日-单位净值 | float | 随时间变动   |
| 前交易日-累计净值 | float | 随时间变动   |
| 日增长值      | float | -       |
| 日增长率      | float | -       |
| 申购状态      | str   | -       |
| 赎回状态      | str   | -       |
| 手续费       | str   | 注意单位: % |

接口示例

```python
import akshare as ak

fund_open_fund_daily_em_df = ak.fund_open_fund_daily_em()
print(fund_open_fund_daily_em_df)
```

数据示例

```
      基金代码             基金简称 2020-12-28-单位净值  ...  申购状态  赎回状态    手续费
0      010407        安信中债1-3年政策性金融债C          1.0906  ...  开放申购  开放赎回  0.00%
1      161725             招商中证白酒指数分级          1.3869  ...   限大额  开放赎回  0.10%
2      160632                  鹏华酒分级          1.0360  ...  开放申购  开放赎回  0.12%
3      004987             诺德新享灵活配置混合          2.2665  ...  开放申购  开放赎回  0.15%
4      008135               华宸未来价值先锋          1.4346  ...  开放申购  开放赎回  0.15%
       ...                    ...             ...  ...   ...   ...    ...
10005  009209       长信稳利一年持有期混合(FOF)                  ...  开放申购   封闭期  0.80%
10006  873002  广发资管全球精选一年持有期债券(QDII)                  ...   封闭期   封闭期
10007  007401       浦银颐和稳健养老一年(FOF)A                  ...  开放申购  开放赎回  0.08%
10008  010672        鹏华创新未来18个月封闭混合B                  ...   封闭期  开放赎回
10009  010650       易方达创新未来18个月封闭混合B                  ...   封闭期  开放赎回
```
