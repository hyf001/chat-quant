---
title: "fund_scale_open_sina - 开放式基金"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_scale_open_sina

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金规模 > 开放式基金
- 描述: 基金数据中心-基金规模-开放式基金
- 目标地址: https://vip.stock.finance.sina.com.cn/fund_center/index.html#jjhqetf
- 限量: 单次返回指定 symbol 的基金规模数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 开放式基金

接口: fund_scale_open_sina

目标地址: https://vip.stock.finance.sina.com.cn/fund_center/index.html#jjhqetf

描述: 基金数据中心-基金规模-开放式基金

限量: 单次返回指定 symbol 的基金规模数据

输入参数

| 名称     | 类型  | 描述                                                                       |
|--------|-----|--------------------------------------------------------------------------|
| symbol | str | symbol="股票型基金"; choice of {"股票型基金", "混合型基金", "债券型基金", "货币型基金", "QDII基金"} |

输出参数

| 名称    | 类型      | 描述       |
|-------|---------|----------|
| 序号    | int64   | -        |
| 基金代码  | object  | -        |
| 基金简称  | object  | -        |
| 单位净值  | float64 | 注意单位: 元  |
| 总募集规模 | float64 | 注意单位: 万份 |
| 最近总份额 | float64 | 注意单位: 份  |
| 成立日期  | object  | -        |
| 基金经理  | object  | -        |
| 更新日期  | object  | -        |

接口示例

```python
import akshare as ak

fund_scale_open_sina_df = ak.fund_scale_open_sina(symbol='股票型基金')
print(fund_scale_open_sina_df)
```

数据示例

```
        序号    基金代码               基金简称  ...        成立日期     基金经理        更新日期
0        1  510300       华泰柏瑞沪深300ETF  ...  2012-05-04       柳军  2023-11-06
1        2  009341          易方达均衡成长股票  ...  2020-05-22       陈皓  2023-11-06
2        3  512960        博时央企结构调整ETF  ...  2018-10-19      赵云阳  2023-11-06
3        4  000051      华夏沪深300ETF联接A  ...  2009-07-10  张弘弢、赵宗庭  2023-11-06
4        5  001409           工银互联网加股票  ...  2015-06-05       单文  2023-11-06
    ...     ...                ...  ...         ...      ...         ...
3677  3678  015676  鹏华中证移动互联网指数(LOF)C  ...  2022-05-10      罗英宇  2023-11-06
3678  3679  160222      国泰国证食品饮料行业指数A  ...  2021-01-01       梁杏  2023-11-06
3679  3680  160221      国泰国证有色金属行业指数A  ...  2021-01-01      吴中昊  2023-11-06
3680  3681  160218       国泰国证房地产行业指数A  ...  2021-01-01      吴中昊  2023-11-06
3681  3682  960000          汇丰晋信大盘股票H  ...  2015-12-29      闵良超  2023-11-06
[3682 rows x 9 columns]
```
