---
title: "futures_main_sina - 期货连续合约"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, futures, parameters, returns, example]
sources: [raw/data-dictionary/futures/futures.md]
confidence: high
---
# futures_main_sina

- 分类: [[futures-futures|AKShare 期货数据]]
- 主题路径: 此处的合约需要是近期的合约, 否则会报错 > 期货连续合约
- 描述: 新浪财经-期货-主力连续合约历史数据
- 目标地址: https://vip.stock.finance.sina.com.cn/quotes_service/view/qihuohangqing.html#titlePos_0
- 限量: 单次返回单个期货品种的主力连续合约的日频历史数据
- 来源页面: https://akshare.akfamily.xyz/data/futures/futures.html

## 相关

- [[futures-futures|AKShare 期货数据]]
- [[_meta/topic-map]]

## 源文摘录

### 期货连续合约

接口: futures_main_sina

目标地址: https://vip.stock.finance.sina.com.cn/quotes_service/view/qihuohangqing.html#titlePos_0

描述: 新浪财经-期货-主力连续合约历史数据

限量: 单次返回单个期货品种的主力连续合约的日频历史数据

输入参数

| 名称         | 类型  | 描述                                                                            |
|------------|-----|-------------------------------------------------------------------------------|
| symbol     | str | symbol="IF0"; 请参考 **新浪连续合约品种一览表**, 也可通过 **ak.futures_display_main_sina()** 获取 |
| start_date | str | start_date="19900101";                                                        |
| end_date   | str | end_date="22220101";                                                          |

新浪连续合约品种一览表

| index | symbol | exchange | name        |
|------:|:-------|:---------|:------------|
|     0 | V0     | dce      | PVC连续       |
|     1 | P0     | dce      | 棕榈油连续       |
|     2 | B0     | dce      | 豆二连续        |
|     3 | M0     | dce      | 豆粕连续        |
|     4 | I0     | dce      | 铁矿石连续       |
|     5 | JD0    | dce      | 鸡蛋连续        |
|     6 | L0     | dce      | 塑料连续        |
|     7 | PP0    | dce      | 聚丙烯连续       |
|     8 | FB0    | dce      | 纤维板连续       |
|     9 | BB0    | dce      | 胶合板连续       |
|    10 | Y0     | dce      | 豆油连续        |
|    11 | C0     | dce      | 玉米连续        |
|    12 | A0     | dce      | 豆一连续        |
|    13 | J0     | dce      | 焦炭连续        |
|    14 | JM0    | dce      | 焦煤连续        |
|    15 | CS0    | dce      | 淀粉连续        |
|    16 | EG0    | dce      | 乙二醇连续       |
|    17 | RR0    | dce      | 粳米连续        |
|    18 | EB0    | dce      | 苯乙烯连续       |
|    19 | LH0    | dce      | 生猪连续        |
|    20 | TA0    | czce     | PTA连续       |
|    21 | OI0    | czce     | 菜油连续        |
|    22 | RS0    | czce     | 菜籽连续        |
|    23 | RM0    | czce     | 菜粕连续        |
|    24 | ZC0    | czce     | 动力煤连续       |
|    25 | WH0    | czce     | 强麦连续        |
|    26 | JR0    | czce     | 粳稻连续        |
|    27 | SR0    | czce     | 白糖连续        |
|    28 | CF0    | czce     | 棉花连续        |
|    29 | RI0    | czce     | 早籼稻连续       |
|    30 | MA0    | czce     | 甲醇连续        |
|    31 | FG0    | czce     | 玻璃连续        |
|    32 | LR0    | czce     | 晚籼稻连续       |
|    33 | SF0    | czce     | 硅铁连续        |
|    34 | SM0    | czce     | 锰硅连续        |
|    35 | CY0    | czce     | 棉纱连续        |
|    36 | AP0    | czce     | 苹果连续        |
|    37 | CJ0    | czce     | 红枣连续        |
|    38 | UR0    | czce     | 尿素连续        |
|    39 | SA0    | czce     | 纯碱连续        |
|    40 | PF0    | czce     | 短纤连续        |
|    41 | PK0    | czce     | 花生连续        |
|    42 | FU0    | shfe     | 燃料油连续       |
|    43 | SC0    | ine      | 上海原油连续      |
|    44 | AL0    | shfe     | 铝连续         |
|    45 | RU0    | shfe     | 天然橡胶连续      |
|    46 | ZN0    | shfe     | 沪锌连续        |
|    47 | CU0    | shfe     | 铜连续         |
|    48 | AU0    | shfe     | 黄金连续        |
|    49 | RB0    | shfe     | 螺纹钢连续       |
|    50 | WR0    | shfe     | 线材连续        |
|    51 | PB0    | shfe     | 铅连续         |
|    52 | AG0    | shfe     | 白银连续        |
|    53 | BU0    | shfe     | 沥青连续        |
|    54 | HC0    | shfe     | 热轧卷板连续      |
|    55 | SN0    | shfe     | 锡连续         |
|    56 | NI0    | shfe     | 镍连续         |
|    57 | SP0    | shfe     | 纸浆连续        |
|    58 | NR0    | ine      | 20号胶连续      |
|    59 | SS0    | shfe     | 不锈钢连续       |
|    60 | LU0    | ine      | 低硫燃料油连续     |
|    61 | BC0    | ine      | 国际铜连续       |
|    62 | IF0    | cffex    | 沪深300指数期货连续 |
|    63 | TF0    | cffex    | 5年期国债期货连续   |
|    64 | IH0    | cffex    | 上证50指数期货连续  |
|    65 | IC0    | cffex    | 中证500指数期货连续 |
|    66 | TS0    | cffex    | 2年期国债期货连续   |

输出参数

| 名称    | 类型     | 描述   |
|-------|--------|------|
| 日期    | object | -    |
| 开盘价   | int64  | -    |
| 最高价   | int64  | -    |
| 最低价   | int64  | -    |
| 收盘价   | int64  | -    |
| 成交量   | int64  | 注意单位 |
| 持仓量   | int64  | 注意单位 |
| 动态结算价 | int64  | -    |

接口示例-主力连续合约

```python
import akshare as ak

futures_main_sina_hist = ak.futures_main_sina(symbol="V0", start_date="20200101", end_date="20220101")
print(futures_main_sina_hist)
```

数据示例-主力连续合约

```
     日期        开盘价  最高价 最低价 收盘价  成交量  持仓量  动态结算价
0    2020-01-02  6520  6530  6485  6500    54491  230632   6500
1    2020-01-03  6500  6510  6480  6495    72391  229655   6495
2    2020-01-06  6495  6590  6480  6545   174761  237376   6535
3    2020-01-07  6540  6545  6495  6510    86013  230968   6515
4    2020-01-08  6515  6570  6510  6565   115493  235940   6550
..          ...   ...   ...   ...   ...      ...     ...    ...
481  2021-12-27  8500  8605  8233  8239  1162292  322968   8413
482  2021-12-28  8239  8510  8224  8483   930875  342271   8362
483  2021-12-29  8500  8520  8413  8484   797016  348914   8468
484  2021-12-30  8480  8503  8372  8478   924423  351493      0
485  2021-12-31  8492  8530  8276  8321   987714  320158   8384
```

接口示例-新浪主力连续合约品种一览表接口

```python
import akshare as ak

futures_display_main_sina_df = ak.futures_display_main_sina()
print(futures_display_main_sina_df)
```

数据示例-新浪主力连续合约品种一览表接口

```
   symbol    exchange       name
0      V0      dce        PVC连续
1      P0      dce        棕榈油连续
2      B0      dce         豆二连续
3      M0      dce         豆粕连续
4      I0      dce        铁矿石连续
..    ...      ...          ...
58    IF0    cffex  沪深300指数期货连续
59    TF0    cffex    5年期国债期货连续
60    IH0    cffex   上证50指数期货连续
61    IC0    cffex  中证500指数期货连续
62    TS0    cffex    2年期国债期货连续
```
