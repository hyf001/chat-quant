---
title: "fund_scale_structured_sina - 分级子基金"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_scale_structured_sina

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金规模 > 分级子基金
- 描述: 基金数据中心-基金规模-分级子基金
- 目标地址: https://vip.stock.finance.sina.com.cn/fund_center/index.html#jjgmfjall
- 限量: 单次返回所有分级子基金的基金规模数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 分级子基金

接口: fund_scale_structured_sina

目标地址: https://vip.stock.finance.sina.com.cn/fund_center/index.html#jjgmfjall

描述: 基金数据中心-基金规模-分级子基金

限量: 单次返回所有分级子基金的基金规模数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

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

fund_scale_structured_sina_df = ak.fund_scale_structured_sina()
print(fund_scale_structured_sina_df)
```

数据示例

```
      序号    基金代码             基金简称  ...        成立日期  基金经理        更新日期
0      1  150006            长盛同庆A  ...  2009-05-12    王宁         NaN
1      2  150007            长盛同庆B  ...  2009-05-12    王宁         NaN
2      3  150099         长盛同庆800B  ...  2012-05-12    王超         NaN
3      4  150098         长盛同庆800A  ...  2012-05-12    王超         NaN
4      5  150259       易方达重组指数分级A  ...  2015-06-03   刘树荣         NaN
..   ...     ...              ...  ...         ...   ...         ...
397  398  000910          鑫元合丰纯债C  ...  2016-12-27    陈浩  2023-11-09
398  399  000501     华富恒富18个月定开债C  ...  2017-11-22   姚姣姣         NaT
399  400  000502     华富恒富18个月定开债A  ...  2017-11-22   姚姣姣         NaT
400  401  000623      华富恒财定期开放债券C  ...  2018-08-07   倪莉莎         NaT
401  402  163118  申万菱信中证申万医药生物指数A  ...  2021-01-01   廖裕舟  2023-11-09
[402 rows x 9 columns]
```
