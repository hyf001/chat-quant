---
title: "futures_contract_detail_em - 期货合约详情-东财"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, futures, parameters, returns, example]
sources: [raw/data-dictionary/futures/futures.md]
confidence: high
---
# futures_contract_detail_em

- 分类: [[futures-futures|AKShare 期货数据]]
- 主题路径: 此处的合约需要是近期的合约, 否则会报错 > 期货合约详情-东财
- 描述: 东方财富-期货-期货合约详情数据
- 目标地址: https://quote.eastmoney.com/qihuo/v2602F.html
- 限量: 单次返回指定 symbol 的合约详情数据
- 来源页面: https://akshare.akfamily.xyz/data/futures/futures.html

## 相关

- [[futures-futures|AKShare 期货数据]]
- [[_meta/topic-map]]

## 源文摘录

### 期货合约详情-东财

接口: futures_contract_detail_em

目标地址: https://quote.eastmoney.com/qihuo/v2602F.html

描述: 东方财富-期货-期货合约详情数据

限量: 单次返回指定 symbol 的合约详情数据

输入参数

| 名称     | 类型  | 描述                                                                              |
|--------|-----|---------------------------------------------------------------------------------|
| symbol | str | symbol='v2602F'; 请参考东方财富的期货品种标识：https://quote.eastmoney.com/center/futures.html |

输出参数

| 名称    | 类型     | 描述       |
|-------|--------|----------|
| item  | object | 合约具体的项目  |
| value | object | 合约具体的项目值 |

接口示例

```python
import akshare as ak

futures_contract_detail_em_df = ak.futures_contract_detail_em(symbol="v2603F")
print(futures_contract_detail_em_df)
```

数据示例

```
       item                                              value
0      交易品种                                               聚氯乙烯
1    最小变动价位                                               5元/吨
2      交易时间  上午 09:00-10:15 10:30-11:30 下午 13:30-15:00 夜间 2...
3      交割品级  质量标准符合《悬浮法通用型聚氯乙烯树脂（GB/T 5761-2006）》规定的SG5型一等品...
4      交割方式                                               实物交割
5      交易单位                                               5吨/手
6    涨跌停板幅度                                       上一交易日结算价的±4%
7     最后交易日                                        合约月份第10个交易日
8   最低交易保证金                                投机买卖20.0%，套保买卖20.0%
9      交易代码                                                  V
10     报价单位                                           元(人民币/吨)
11   合约交割月份                                            1---12月
12    最后交割日                                       最后交易日后第3个交易日
13    交易手续费                                  开平仓1元/手，短线开平仓1元/手
14    上市交易所                                            大连商品交易所
```
