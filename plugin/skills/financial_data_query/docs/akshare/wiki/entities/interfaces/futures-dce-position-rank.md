---
title: "futures_dce_position_rank - 大连商品交易所"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, futures, parameters, returns, example]
sources: [raw/data-dictionary/futures/futures.md]
confidence: high
---
# futures_dce_position_rank

- 分类: [[futures-futures|AKShare 期货数据]]
- 主题路径: AKShare 期货数据 > 期货基础数据 > 会员持仓排名 > 大连商品交易所
- 描述: 大连商品交易所指定交易日的具体合约的持仓排名
- 目标地址: http://www.dce.com.cn/dalianshangpin/xqsj/tjsj26/rtj/rcjccpm/index.html
- 限量: 单次返回所有合约的持仓排名数据, 返回以合约名字为键, 具体排名数据为值的字典
- 来源页面: https://akshare.akfamily.xyz/data/futures/futures.html

## 相关

- [[futures-futures|AKShare 期货数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 大连商品交易所

接口: futures_dce_position_rank

目标地址: http://www.dce.com.cn/dalianshangpin/xqsj/tjsj26/rtj/rcjccpm/index.html

描述: 大连商品交易所指定交易日的具体合约的持仓排名

限量: 单次返回所有合约的持仓排名数据, 返回以合约名字为键, 具体排名数据为值的字典

输入参数

| 名称        | 类型   | 描述                                                                                                                    |
|-----------|------|-----------------------------------------------------------------------------------------------------------------------|
| date      | str  | date="20200511"; 指定交易日, 该数据接口可以获取从 2000 年开始的数据, 20160104 由于交易所数据问题，返回为空可以调用 **futures_dce_position_rank_other** 来返回数据 |
| vars_list | list | vars_list=cons.contract_symbols; 指定品种，比如：["C", "CS"]                                                                  |

P.S. **futures_dce_position_rank_other** 函数只返回页面显示的活跃合约，返回格式同 **futures_dce_position_rank**

输出参数-字典

P.S. 这里仅列出值(pandas.DataFrame)的字段信息

| 名称                      | 类型      | 描述      |
|-------------------------|---------|---------|
| long_open_interest      | object  | 持买单量    |
| long_open_interest_chg  | float64 | 持买单量-增减 |
| long_party_name         | object  | 会员简称    |
| rank                    | float64 | 名次      |
| short_open_interest     | float64 | 持卖单量    |
| short_open_interest_chg | float64 | 持买单量-增减 |
| short_party_name        | object  | 会员简称    |
| vol                     | float64 | 成交量     |
| vol_chg                 | float64 | 成交量-增减  |
| vol_party_name          | object  | 会员简称    |
| symbol                  | object  | 具体合约    |
| variety                 | object  | 品种      |

接口示例

```python
import akshare as ak

futures_dce_detail_dict = ak.futures_dce_position_rank(date="20200513")
print(futures_dce_detail_dict)
```

数据示例-字典

```
{'jm2009':    long_open_interest long_open_interest_chg  ...  symbol  variety
0               9,063                   -253  ...  jm2009       JM
1               8,255                     65  ...  jm2009       JM
2               5,954                   -216  ...  jm2009       JM
3               3,691                   -127  ...  jm2009       JM
4               3,387                    115  ...  jm2009       JM
..                ...                    ...  ...     ...      ...
15              1,539                   -120  ...  jm2009       JM
16              1,457                    158  ...  jm2009       JM
17              1,391                     92  ...  jm2009       JM
18              1,377                    -60  ...  jm2009       JM
19              1,343                    -40  ...  jm2009       JM
}
```
