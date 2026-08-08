---
title: "futures_contract_detail - 期货合约详情-新浪"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, futures, parameters, returns, example]
sources: [raw/data-dictionary/futures/futures.md]
confidence: high
---
# futures_contract_detail

- 分类: [[futures-futures|AKShare 期货数据]]
- 主题路径: 此处的合约需要是近期的合约, 否则会报错 > 期货合约详情-新浪
- 描述: 新浪财经-期货-期货合约详情数据
- 目标地址: https://finance.sina.com.cn/futures/quotes/V2101.shtml
- 限量: 单次返回指定 symbol 的合约详情数据
- 来源页面: https://akshare.akfamily.xyz/data/futures/futures.html

## 相关

- [[futures-futures|AKShare 期货数据]]
- [[_meta/topic-map]]

## 源文摘录

### 期货合约详情-新浪

接口: futures_contract_detail

目标地址: https://finance.sina.com.cn/futures/quotes/V2101.shtml

描述: 新浪财经-期货-期货合约详情数据

限量: 单次返回指定 symbol 的合约详情数据

输入参数

| 名称     | 类型  | 描述                                                                              |
|--------|-----|---------------------------------------------------------------------------------|
| symbol | str | symbol='AP2101'; 请参考**新浪连续合约品种一览表**, 也可通过 **ak.futures_display_main_sina()** 获取 |

新浪连续合约品种一览表（更新于 20241226）

|    | symbol | exchange | name        |
|---:|:-------|:---------|:------------|
|  0 | V0     | dce      | PVC连续       |
|  1 | P0     | dce      | 棕榈油连续       |
|  2 | B0     | dce      | 豆二连续        |
|  3 | M0     | dce      | 豆粕连续        |
|  4 | I0     | dce      | 铁矿石连续       |
|  5 | JD0    | dce      | 鸡蛋连续        |
|  6 | L0     | dce      | 塑料连续        |
|  7 | PP0    | dce      | 聚丙烯连续       |
|  8 | FB0    | dce      | 纤维板连续       |
|  9 | BB0    | dce      | 胶合板连续       |
| 10 | Y0     | dce      | 豆油连续        |
| 11 | C0     | dce      | 玉米连续        |
| 12 | A0     | dce      | 豆一连续        |
| 13 | J0     | dce      | 焦炭连续        |
| 14 | JM0    | dce      | 焦煤连续        |
| 15 | CS0    | dce      | 淀粉连续        |
| 16 | EG0    | dce      | 乙二醇连续       |
| 17 | RR0    | dce      | 粳米连续        |
| 18 | EB0    | dce      | 苯乙烯连续       |
| 19 | PG0    | dce      | 液化石油气连续     |
| 20 | LH0    | dce      | 生猪连续        |
| 21 | TA0    | czce     | PTA连续       |
| 22 | OI0    | czce     | 菜油连续        |
| 23 | RS0    | czce     | 菜籽连续        |
| 24 | RM0    | czce     | 菜粕连续        |
| 25 | WH0    | czce     | 强麦连续        |
| 26 | JR0    | czce     | 粳稻连续        |
| 27 | SR0    | czce     | 白糖连续        |
| 28 | CF0    | czce     | 棉花连续        |
| 29 | RI0    | czce     | 早籼稻连续       |
| 30 | MA0    | czce     | 甲醇连续        |
| 31 | FG0    | czce     | 玻璃连续        |
| 32 | LR0    | czce     | 晚籼稻连续       |
| 33 | SF0    | czce     | 硅铁连续        |
| 34 | SM0    | czce     | 锰硅连续        |
| 35 | CY0    | czce     | 棉纱连续        |
| 36 | AP0    | czce     | 苹果连续        |
| 37 | CJ0    | czce     | 红枣连续        |
| 38 | UR0    | czce     | 尿素连续        |
| 39 | SA0    | czce     | 纯碱连续        |
| 40 | PF0    | czce     | 短纤连续        |
| 41 | PK0    | czce     | 花生连续        |
| 42 | SH0    | czce     | 烧碱连续        |
| 43 | PX0    | czce     | 对二甲苯连续      |
| 44 | FU0    | shfe     | 燃料油连续       |
| 45 | SC0    | ine      | 上海原油连续      |
| 46 | AL0    | shfe     | 铝连续         |
| 47 | RU0    | shfe     | 天然橡胶连续      |
| 48 | ZN0    | shfe     | 沪锌连续        |
| 49 | CU0    | shfe     | 铜连续         |
| 50 | AU0    | shfe     | 黄金连续        |
| 51 | RB0    | shfe     | 螺纹钢连续       |
| 52 | WR0    | shfe     | 线材连续        |
| 53 | PB0    | shfe     | 铅连续         |
| 54 | AG0    | shfe     | 白银连续        |
| 55 | BU0    | shfe     | 沥青连续        |
| 56 | HC0    | shfe     | 热轧卷板连续      |
| 57 | SN0    | shfe     | 锡连续         |
| 58 | NI0    | shfe     | 镍连续         |
| 59 | SP0    | shfe     | 纸浆连续        |
| 60 | NR0    | ine      | 20号胶连续      |
| 61 | SS0    | shfe     | 不锈钢连续       |
| 62 | LU0    | ine      | 低硫燃料油连续     |
| 63 | BC0    | ine      | 国际铜连续       |
| 64 | AO0    | shfe     | 氧化铝连续       |
| 65 | BR0    | shfe     | 丁二烯橡胶连续     |
| 66 | EC0    | ine      | 集运指数欧线期货连续  |
| 67 | IF0    | cffex    | 沪深300指数期货连续 |
| 68 | TF0    | cffex    | 5年期国债期货连续   |
| 69 | IH0    | cffex    | 上证50指数期货连续  |
| 70 | IC0    | cffex    | 中证500指数期货连续 |
| 71 | TS0    | cffex    | 2年期国债期货连续   |
| 72 | IM0    | cffex    | 中证连续指数期货连续  |
| 73 | SI0    | gfex     | 工业硅连续       |
| 74 | LC0    | gfex     | 碳酸锂连续       |
| 75 | PS0    | gfex     | 多晶硅连续       |

输出参数

| 名称    | 类型     | 描述       |
|-------|--------|----------|
| item  | object | 合约具体的项目  |
| value | object | 合约具体的项目值 |

接口示例

```python
import akshare as ak

futures_contract_detail_df = ak.futures_contract_detail(symbol='V2001')
print(futures_contract_detail_df)
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
13    交易手续费                                  开平仓2元/手，短线开平仓1元/手
14    上市交易所                                            大连商品交易所
```
