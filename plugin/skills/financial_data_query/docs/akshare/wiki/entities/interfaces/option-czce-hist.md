---
title: "option_czce_hist - 历史数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, option, parameters, returns, example]
sources: [raw/data-dictionary/option/option.md]
confidence: high
---
# option_czce_hist

- 分类: [[option-option|AKShare 期权数据]]
- 主题路径: AKShare 期权数据 > 商品期权 > 历史数据
- 描述: 郑州商品交易所的商品期权历史行情数据
- 目标地址: http://www.czce.com.cn/cn/jysj/lshqxz/H770319index_1.htm
- 限量: 单次返回指定年份指定品种期权历史行情数据
- 来源页面: https://akshare.akfamily.xyz/data/option/option.html

## 相关

- [[option-option|AKShare 期权数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 历史数据

接口: option_czce_hist

目标地址: http://www.czce.com.cn/cn/jysj/lshqxz/H770319index_1.htm

描述: 郑州商品交易所的商品期权历史行情数据

限量: 单次返回指定年份指定品种期权历史行情数据

输入参数

| 名称     | 类型  | 描述                                                                                                                                                                                                                                                                |
|--------|-----|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| year   | str | year="2019"; 指定年份                                                                                                                                                                                                                                                 |
| symbol | str | symbol="SR"; choice of {"白糖": "SR", "棉花": "CF", "PTA": "TA", "甲醇": "MA", "菜籽粕": "RM", "动力煤": "ZC", "菜籽油": "OI", "花生": "PK", "对二甲苯": "PX", "烧碱": "SH", "纯碱": "SA", "短纤": "PF", "锰硅": "SM", "硅铁": "SF", "尿素": "UR", "苹果": "AP", "红枣": "CJ", "玻璃": "FG", "瓶片": "PR"} |

输出参数

| 名称      | 类型      | 描述  |
|---------|---------|-----|
| 交易日期    | object  |     |
| 品种代码    | object  |     |
| 昨结算     | float64 |     |
| 今开盘     | float64 |     |
| 最高价     | float64 |     |
| 最低价     | float64 |     |
| 今收盘     | float64 |     |
| 今结算     | float64 |     |
| 涨跌1     | float64 |     |
| 涨跌2     | float64 |     |
| 成交量(手)  | object  |     |
| 空盘量     | object  |     |
| 增减量     | object  |     |
| 成交额(万元) | object  |     |
| DELTA   | float64 |     |
| 隐含波动率   | float64 |     |
| 行权量     | float64 |     |

说明:

1. 价格: 元/吨
2. 成交量、空盘量: 手
3. 成交额: 万元
4. 涨跌一: 今收盘-昨结算
5. 涨跌二: 今结算-昨结算
6. 隐含波动率: 将当日期权合约的结算价代入期权定价模型, 反推出来的波动率数值

接口示例

```python
import akshare as ak

option_hist_yearly_czce_df = ak.option_hist_yearly_czce(symbol="RM", year="2025")
print(option_hist_yearly_czce_df)
```

数据示例

```
       交易日期     合约代码     ...  隐含波动率                       行权量
0      2025-01-02  RM503C1925  ...  22.64  0
1      2025-01-02  RM503C1950  ...  22.42  0
2      2025-01-02  RM503C1975  ...  22.25  0
3      2025-01-02  RM503C2000  ...  22.12  0
4      2025-01-02  RM503C2025  ...  22.05  0
...           ...         ...  ...    ...                              ...
16067  2025-03-21  RM601P2600  ...  21.49  0
16068  2025-03-21  RM601P2650  ...  21.78  0
16069  2025-03-21  RM601P2700  ...  22.11  0
16070  2025-03-21  RM601P2750  ...  22.48  0
16071  2025-03-21  RM601P2800  ...  22.90  0
[16072 rows x 17 columns]
```
