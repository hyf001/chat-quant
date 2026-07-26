---
title: "futures_gfex_position_rank - 广州期货交易所"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, futures, parameters, returns, example]
sources: [raw/data-dictionary/futures/futures.md]
confidence: high
---
# futures_gfex_position_rank

- 分类: [[futures-futures|AKShare 期货数据]]
- 主题路径: AKShare 期货数据 > 期货基础数据 > 会员持仓排名 > 广州期货交易所
- 描述: 广州期货交易所-日成交持仓排名
- 目标地址: http://www.gfex.com.cn/gfex/rcjccpm/hqsj_tjsj.shtml
- 限量: 单次返回所有合约的日成交持仓排名数据, 返回以合约名字为键, 具体排名数据为值的字典
- 来源页面: https://akshare.akfamily.xyz/data/futures/futures.html

## 相关

- [[futures-futures|AKShare 期货数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 广州期货交易所

接口: futures_gfex_position_rank

目标地址: http://www.gfex.com.cn/gfex/rcjccpm/hqsj_tjsj.shtml

描述: 广州期货交易所-日成交持仓排名

限量: 单次返回所有合约的日成交持仓排名数据, 返回以合约名字为键, 具体排名数据为值的字典

输入参数

| 名称        | 类型   | 描述                                                       |
|-----------|------|----------------------------------------------------------|
| date      | str  | date="20231113"; 指定交易日, 该数据接口可以获取从 20231110 开始的日成交持仓排名数据 |
| vars_list | list | vars_list=None; 指定品种，比如：['SI', 'LC']                     |

输出参数-字典

P.S. 这里仅列出值(pandas.DataFrame)的字段信息

| 名称                      | 类型     | 描述      |
|-------------------------|--------|---------|
| rank                    | int64  | 名次      |
| vol_party_name          | object | 会员简称    |
| vol                     | int64  | 成交量     |
| vol_chg                 | int64  | 成交量-增减  |
| long_party_name         | object | 会员简称    |
| long_open_interest      | int64  | 持买单量    |
| long_open_interest_chg  | int64  | 持买单量-增减 |
| short_party_name        | object | 会员简称    |
| short_open_interest     | int64  | 持卖单量    |
| short_open_interest_chg | int64  | 持卖单量-增减 |
| symbol                  | object | 具体合约    |
| variety                 | object | 品种      |

接口示例

```python
import akshare as ak

futures_gfex_position_rank_dict = ak.futures_gfex_position_rank(date="20231113")
print(futures_gfex_position_rank_dict)
```

数据示例-字典

```
{'si2312':     rank vol_party_name   vol  ...  short_open_interest_chg  symbol  variety
0      1           中信期货  2940  ...                       50  SI2312       SI
1      2           国海良时  1013  ...                        1  SI2312       SI
2      3           永安期货   956  ...                     -376  SI2312       SI
3      4           宝城期货   901  ...                      120  SI2312       SI
4      5           浙商期货   648  ...                      -10  SI2312       SI
5      6         国投安信期货   640  ...                     -460  SI2312       SI
6      7         国泰君安期货   620  ...                      -94  SI2312       SI
7      8           东证期货   515  ...                        1  SI2312       SI
8      9           广发期货   352  ...                       52  SI2312       SI
9     10           南华期货   294  ...                      895  SI2312       SI
10    11         物产中大期货   275  ...                      -90  SI2312       SI
11    12           华金期货   263  ...                       24  SI2312       SI
12    13           广州期货   211  ...                       -4  SI2312       SI
13    14           华泰期货   205  ...                        0  SI2312       SI
14    15           国贸期货   185  ...                        0  SI2312       SI
15    16           中粮期货   178  ...                        2  SI2312       SI
16    17           申银万国   128  ...                        0  SI2312       SI
17    18           中原期货   118  ...                      -20  SI2312       SI
18    19           海证期货   113  ...                      -10  SI2312       SI
19    20           兴证期货   108  ...                      -22  SI2312       SI
[20 rows x 12 columns], 'si2401':     rank vol_party_name    vol  ...  short_open_interest_chg  symbol  variety
0      1           中信期货  11711  ...                     -195  SI2401       SI
1      2           广州期货   8079  ...                       96  SI2401       SI
2      3           中信建投   7222  ...                      535  SI2401       SI
3      4           广发期货   4361  ...                     1045  SI2401       SI
4      5           华泰期货   3014  ...                       97  SI2401       SI
5      6           东证期货   2252  ...                       89  SI2401       SI
6      7         国投安信期货   1897  ...                      -70  SI2401       SI
7      8           永安期货   1757  ...                       25  SI2401       SI
8      9           海通期货   1723  ...                      -27  SI2401       SI
9     10         国泰君安期货   1514  ...                       16  SI2401       SI
10    11           国海良时   1456  ...                      611  SI2401       SI
11    12           长安期货   1441  ...                      418  SI2401       SI
12    13           华闻期货   1307  ...                    -1199  SI2401       SI
13    14           方正中期   1247  ...                       20  SI2401       SI
14    15           宝城期货   1158  ...                      317  SI2401       SI
15    16           华金期货   1052  ...                       35  SI2401       SI
16    17           信达期货    924  ...                      -45  SI2401       SI
17    18           兴证期货    866  ...                        2  SI2401       SI
18    19           浙商期货    777  ...                       19  SI2401       SI
19    20           徽商期货    761  ...                        5  SI2401       SI
[20 rows x 12 columns], 'lc2401':     rank vol_party_name     vol  ...  short_open_interest_chg  symbol  variety
0      1           中信期货  164523  ...                    -1741  LC2401       LC
1      2           华闻期货   50941  ...                     -284  LC2401       LC
2      3           海通期货   47107  ...                     -822  LC2401       LC
3      4           徽商期货   23884  ...                     1523  LC2401       LC
4      5         东方财富期货   22906  ...                      205  LC2401       LC
5      6         国泰君安期货   21530  ...                     -277  LC2401       LC
6      7           中信建投   21033  ...                      541  LC2401       LC
7      8           渤海期货   20804  ...                     -146  LC2401       LC
8      9           宝城期货   18449  ...                      568  LC2401       LC
9     10           东证期货   16656  ...                      -76  LC2401       LC
10    11           华泰期货   16101  ...                      325  LC2401       LC
11    12           广发期货   15262  ...                      146  LC2401       LC
12    13           方正中期   15198  ...                     1664  LC2401       LC
13    14           银河期货   11187  ...                      863  LC2401       LC
14    15           东吴期货   10747  ...                      723  LC2401       LC
15    16           平安期货    9572  ...                      -54  LC2401       LC
16    17           华安期货    9340  ...                      296  LC2401       LC
17    18           国信期货    9284  ...                      -44  LC2401       LC
18    19           民生期货    9213  ...                      -91  LC2401       LC
19    20           国富期货    9171  ...                     -174  LC2401       LC
[20 rows x 12 columns], 'lc2407':     rank vol_party_name    vol  ...  short_open_interest_chg  symbol  variety
0      1           中信期货  36637  ...                      244  LC2407       LC
1      2           海通期货   4366  ...                       30  LC2407       LC
2      3           中信建投   3499  ...                       10  LC2407       LC
3      4         国泰君安期货   3314  ...                      308  LC2407       LC
4      5           广发期货   3123  ...                       43  LC2407       LC
5      6         东方财富期货   2976  ...                       82  LC2407       LC
6      7           东证期货   2782  ...                     -133  LC2407       LC
7      8           徽商期货   2716  ...                      411  LC2407       LC
8      9           永安期货   2269  ...                       -7  LC2407       LC
9     10           华泰期货   2076  ...                       23  LC2407       LC
10    11           平安期货   2065  ...                       -7  LC2407       LC
11    12           方正中期   1991  ...                      301  LC2407       LC
12    13           华闻期货   1956  ...                       -3  LC2407       LC
13    14           华安期货   1766  ...                       76  LC2407       LC
14    15           安粮期货   1758  ...                     -190  LC2407       LC
15    16           申银万国   1481  ...                       19  LC2407       LC
16    17           东吴期货   1398  ...                       18  LC2407       LC
17    18           中泰期货   1175  ...                      -93  LC2407       LC
18    19           先锋期货   1144  ...                      -19  LC2407       LC
19    20           银河期货   1100  ...                     -218  LC2407       LC
[20 rows x 12 columns]}
```
