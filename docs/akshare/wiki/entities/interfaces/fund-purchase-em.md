---
title: "fund_purchase_em - 基金申购状态"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_purchase_em

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金申购状态
- 描述: 东方财富网站-天天基金网-基金数据-基金申购状态
- 目标地址: http://fund.eastmoney.com/Fund_sgzt_bzdm.html#fcode,asc_1
- 限量: 单次返回当前时刻所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

### 基金申购状态

接口: fund_purchase_em

目标地址: http://fund.eastmoney.com/Fund_sgzt_bzdm.html#fcode,asc_1

描述: 东方财富网站-天天基金网-基金数据-基金申购状态

限量: 单次返回当前时刻所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称             | 类型      | 描述      |
|----------------|---------|---------|
| 序号             | object  | -       |
| 基金代码           | object  | -       |
| 基金简称           | object  | -       |
| 基金类型           | object  | -       |
| 最新净值/万份收益      | float64 | -       |
| 最新净值/万份收益-报告时间 | object  | -       |
| 申购状态           | object  | -       |
| 赎回状态           | object  | -       |
| 下一开放日          | object  | -       |
| 购买起点           | float64 | -       |
| 日累计限定金额        | float64 | -       |
| 手续费            | float64 | 注意单位: % |

接口示例

```python
import akshare as ak

fund_purchase_em_df = ak.fund_purchase_em()
print(fund_purchase_em_df)
```

数据示例

```
          序号    基金代码                基金简称  ... 购买起点       日累计限定金额   手续费
0          1  000001              华夏成长混合  ...   10  1.000000e+11  0.15
1          2  000003            中海可转债债券A  ...   10  1.000000e+10  0.08
2          3  000004            中海可转债债券C  ...   10  1.000000e+10  0.00
3          4  000005          嘉实增强信用定期债券  ...   10  1.000000e+11  0.08
4          5  000006         西部利得量化成长混合A  ...   10  2.000000e+04  0.15
      ...     ...                 ...  ...  ...           ...   ...
14955  14956  970118        东吴裕丰6个月持有债券C  ...   10  1.000000e+11  0.00
14956  14957  970119  兴证资管金麒麟恒睿致远一年持有混合A  ...    0  0.000000e+00  1.20
14957  14958  970120  兴证资管金麒麟恒睿致远一年持有混合B  ...    0  0.000000e+00   NaN
14958  14959  970121  兴证资管金麒麟恒睿致远一年持有混合C  ...    0  0.000000e+00  0.00
14959  14960  980003         太平洋六个月滚动持有债  ...  100  1.000000e+11  0.05
```
