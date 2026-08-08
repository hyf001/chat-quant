---
title: "fund_overview_em - 基金基本概况"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_overview_em

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金基本概况
- 描述: 天天基金-基金档案-基本概况
- 目标地址: https://fundf10.eastmoney.com/jbgk_015641.html
- 限量: 单次返回指定 symbol 的数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

### 基金基本概况

接口: fund_overview_em

目标地址: https://fundf10.eastmoney.com/jbgk_015641.html

描述: 天天基金-基金档案-基本概况

限量: 单次返回指定 symbol 的数据

输入参数

| 名称     | 类型  | 描述                    |
|--------|-----|-----------------------|
| symbol | str | symbol="015641"; 基金代码 |

输出参数

| 名称      | 类型     | 描述 |
|---------|--------|----|
| 基金全称    | object | -  |
| 基金简称    | object | -  |
| 基金代码    | object | -  |
| 基金类型    | object | -  |
| 发行日期    | object | -  |
| 成立日期/规模 | object | -  |
| 资产规模    | object | -  |
| 份额规模    | object | -  |
| 基金管理人   | object | -  |
| 基金托管人   | object | -  |
| 基金经理人   | object | -  |
| 成立来分红   | object | -  |
| 管理费率    | object | -  |
| 托管费率    | object | -  |
| 销售服务费率  | object | -  |
| 最高认购费率  | object | -  |
| 业绩比较基准  | object | -  |
| 跟踪标的    | object | -  |

接口示例

```python
import akshare as ak

fund_overview_em_df = ak.fund_overview_em(symbol="015641")
print(fund_overview_em_df)
```

数据示例

```
                 基金全称          基金简称        基金代码 基金类型         发行日期                成立日期/规模  ...       跟踪标的
0  银华数字经济股票型发起式证券投资基金  银华数字经济股票发起式A  015641（前端）  股票型  2022年05月12日  2022年05月20日 / 0.137亿份  ...  该基金无跟踪标的
[1 rows x 18 columns]
```
