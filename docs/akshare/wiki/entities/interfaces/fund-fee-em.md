---
title: "fund_fee_em - 基金交易费率"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_fee_em

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金交易费率
- 描述: 天天基金-基金档案-购买信息
- 目标地址: https://fundf10.eastmoney.com/jjfl_015641.html
- 限量: 单次返回指定 symbol 的 indicator 数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

### 基金交易费率

接口: fund_fee_em

目标地址: https://fundf10.eastmoney.com/jjfl_015641.html

描述: 天天基金-基金档案-购买信息

限量: 单次返回指定 symbol 的 indicator 数据

输入参数

| 名称        | 类型  | 描述                                                                                                          |
|-----------|-----|-------------------------------------------------------------------------------------------------------------|
| symbol    | str | symbol="015641"; 基金代码                                                                                       |
| indicator | str | indicator="申购费率"; choice of {"交易状态", "申购与赎回金额", "交易确认日", "运作费用", "认购费率（前端）", "认购费率（后端）","申购费率（前端）", "赎回费率"} |

输出参数

| 名称    | 类型      | 描述 |
|-------|---------|----|
| 费用类型  | object  | -  |
| 条件或名称 | object  | -  |
| 费用    | float64 | -  |

接口示例

```python
import akshare as ak

fund_fee_em_df = ak.fund_fee_em(symbol="015641", indicator="认购费率")
print(fund_fee_em_df)
```

数据示例

```
                适用金额 适用期限      原费率 天天基金优惠费率
0            小于100万元  ---    1.20%    0.12%
1  大于等于100万元，小于200万元  ---    0.80%    0.08%
2  大于等于200万元，小于500万元  ---    0.50%    0.05%
3          大于等于500万元  ---  每笔1000元  每笔1000元
```
