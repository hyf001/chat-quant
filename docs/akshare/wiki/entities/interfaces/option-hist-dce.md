---
title: "option_hist_dce - 大连商品交易所"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, option, parameters, returns, example]
sources: [raw/data-dictionary/option/option.md]
confidence: high
---
# option_hist_dce

- 分类: [[option-option|AKShare 期权数据]]
- 主题路径: AKShare 期权数据 > 商品期权 > 大连商品交易所
- 描述: 大连商品交易所-商品期权数据
- 目标地址: http://www.dce.com.cn/dalianshangpin/xqsj/tjsj26/rtj/rxq/index.html
- 限量: 单次返回指定 symbol 和 trade_date 的期权日行情数据
- 来源页面: https://akshare.akfamily.xyz/data/option/option.html

## 相关

- [[option-option|AKShare 期权数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 大连商品交易所

接口: option_hist_dce

目标地址: http://www.dce.com.cn/dalianshangpin/xqsj/tjsj26/rtj/rxq/index.html

描述: 大连商品交易所-商品期权数据

限量: 单次返回指定 symbol 和 trade_date 的期权日行情数据

输入参数

| 名称         | 类型  | 描述                                                                                                                                                                                    |
|------------|-----|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| symbol     | str | symbol="聚丙烯期权"; choice of {"玉米期权", "豆粕期权", "铁矿石期权", "液化石油气期权", "聚乙烯期权", "聚氯乙烯期权", "聚丙烯期权", "棕榈油期权", "黄大豆1号期权", "黄大豆2号期权", "豆油期权", "乙二醇期权", "苯乙烯期权", "鸡蛋期权", "玉米淀粉期权", "生猪期权", "原木期权"} |
| trade_date | str | trade_date="20251016"                                                                                                                                                                 |

输出参数

Part-1: 大连商品交易所期权合约行情

| 名称       | 类型      | 描述 |
|----------|---------|----|
| 品种名称     | object  |    |
| 合约       | object  |    |
| 开盘价      | float64 |    |
| 最高价      | float64 |    |
| 最低价      | float64 |    |
| 收盘价      | float64 |    |
| 前结算价     | float64 |    |
| 结算价      | float64 |    |
| 涨跌       | float64 |    |
| 涨跌1      | float64 |    |
| Delta    | float64 |    |
| 隐含波动率(%) | float64 |    |
| 成交量      | int64   |    |
| 持仓量      | int64   |    |
| 持仓量变化    | int64   |    |
| 成交额      | float64 |    |
| 行权量      | int64   |    |

说明:

1. 价格：自2019年12月02日起，纤维板报价单位由元/张改为元/立方米
2. 价格：元/吨，鸡蛋为元/500千克，纤维板为元/立方米，胶合板为元/张，原木为元/立方米
3. 成交量、持仓量：手（按单边计算）
4. 成交额：万元（按单边计算）
5. 涨跌＝收盘价-前结算价
6. 涨跌1=今结算价-前结算价
7. 合约系列：具有相同月份标的期货合约的所有期权合约的统称
8. 隐含波动率：根据期权市场价格，利用期权定价模型计算的标的期货合约价格波动率

接口示例

```python
import akshare as ak

option_hist_dce_df = ak.option_hist_dce(symbol="聚丙烯期权", trade_date="20251016")
print(option_hist_dce_df)
```

数据示例

```
    品种名称       合约       开盘价  最高价   最低价 ...  成交量 持仓量 持仓量变化 成交额 行权量
0    聚丙烯  pp2511-C-5900     0      0     0  ...      0       0     0     0.00   0
1    聚丙烯  pp2511-C-6000     0      0     0  ...      0       0     0     0.00   0
2    聚丙烯  pp2511-C-6100     0      0     0  ...      0       0     0     0.00   0
3    聚丙烯  pp2511-C-6200   338    362   301  ...    305     185    92    51.00   0
4    聚丙烯  pp2511-C-6300   241  262.5   200  ...    353     203    59    40.73   0
..   ...            ...   ...    ...   ...  ...    ...     ...   ...      ...  ..
350  聚丙烯  pp2609-P-7200     0      0     0  ...      0       0     0     0.00   0
351  聚丙烯  pp2609-P-7400     0      0     0  ...      0       0     0     0.00   0
352  聚丙烯  pp2609-P-7600     0      0     0  ...      0       0     0     0.00   0
353  聚丙烯  pp2609-P-7800     0      0     0  ...      0       0     0     0.00   0
354   总计           None  None   None  None  ...  62945  125168  8929  1082.37   0
[355 rows x 17 columns]
```
