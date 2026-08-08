---
title: "fund_info_ths - 基金基本信息-同花顺"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_public.md]
confidence: high
---
# fund_info_ths

- 分类: [[fund-fund-public|AKShare 公募基金数据]]
- 主题路径: AKShare 公募基金数据 > 基金基本信息-同花顺
- 描述: 同花顺-基金数据-基金基本信息
- 目标地址: https://fund.10jqka.com.cn/161130/interduce.html
- 限量: 单次返回指定基金的基本信息
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_public.html

## 相关

- [[fund-fund-public|AKShare 公募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

### 基金基本信息-同花顺

接口: fund_info_ths

目标地址: https://fund.10jqka.com.cn/161130/interduce.html

描述: 同花顺-基金数据-基金基本信息

限量: 单次返回指定基金的基本信息

输入参数

| 名称     | 类型  | 描述                    |
|--------|-----|-----------------------|
| symbol | str | symbol="161130"; 基金代码 |

输出参数

| 名称     | 类型     | 描述  |
|--------|--------|-----|
| 字段     | object | -   |
| 值      | object | -   |

接口示例

```python
import akshare as ak

fund_info_ths_df = ak.fund_info_ths(symbol="161130")
print(fund_info_ths_df)
```

数据示例

```
              字段                                                  值
0         基金代码                                             161130
1         基金简称                                 纳斯达克100LOF
2         基金类型                                               QDII
3         基金全称  易方达纳斯达克100ETF联接(QDII-LOF)A(人民币份额)
4         投资类型                                              指数型
5         基金经理                                              伍臣东
6         成立日期                                          2017-06-23
7         成立规模                                          3.28亿份
8            管理费                                               0.50%
9         份额规模                             4.13亿份（2026-03-31）
10  首次最低金额（元）                                                1
11           托管费                                               0.10%
12       基金管理人                           易方达基金管理有限公司
13       基金托管人                        中国建设银行股份有限公司
14       最高认购费                                               1.00%
15       最高申购费                                               1.20%
16       最高赎回费                                               1.50%
15    业绩比较基准  纳斯达克100指数收益率(使用估值汇率折算)*95%+活期存款利率(税后)*5%
```
