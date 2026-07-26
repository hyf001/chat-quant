---
title: "fx_spot_quote - 人民币外汇即期报价"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fx, parameters, returns, example]
sources: [raw/data-dictionary/fx/fx.md]
confidence: high
---
# fx_spot_quote

- 分类: [[fx-fx|AKShare 外汇数据]]
- 主题路径: AKShare 外汇数据 > 人民币外汇即期报价
- 描述: 人民币外汇即期报价
- 目标地址: http://www.chinamoney.com.cn/chinese/mkdatapfx/
- 限量: 单次返回实时行情数据
- 来源页面: https://akshare.akfamily.xyz/data/fx/fx.html

## 相关

- [[fx-fx|AKShare 外汇数据]]
- [[_meta/topic-map]]

## 源文摘录

### 人民币外汇即期报价

接口: fx_spot_quote

目标地址: http://www.chinamoney.com.cn/chinese/mkdatapfx/

描述: 人民币外汇即期报价

限量: 单次返回实时行情数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

人民币外汇即期报价

| 名称  | 类型      | 描述  |
|-----|---------|-----|
| 货币对 | object  |     |
| 买报价 | float64 |     |
| 卖报价 | float64 |     |

**注：本行情为询价报价行情(美元为ODM), 实时更新**

接口示例
```python
import akshare as ak

fx_spot_quote_df = ak.fx_spot_quote()
print(fx_spot_quote_df)
```

数据示例

```
      货币对        买报价        卖报价
0      USD/CNY    6.68500    6.68540
1      EUR/CNY    7.08170    7.08260
2   100JPY/CNY    4.92400    4.92480
3      HKD/CNY    0.85184    0.85196
4      GBP/CNY    8.20610    8.20690
5      AUD/CNY    4.65300    4.65310
6      NZD/CNY    4.21240    4.21320
7      SGD/CNY    4.82670    4.82680
8      CHF/CNY    7.00390    7.00450
9      CAD/CNY    5.21290    5.21360
10     CNY/MYR    0.65590    0.65750
11     CNY/RUB    7.93950    7.98320
12     CNY/ZAR    2.37330    2.37360
13     CNY/KRW  192.14000  192.20000
14     CNY/AED    0.54935    0.54948
15     CNY/SAR    0.56142    0.56147
16     CNY/HUF   56.53140   56.57020
17     CNY/PLN    0.66319    0.66344
18     CNY/DKK    1.05070    1.05070
19     CNY/SEK    1.50220    1.50240
20     CNY/NOK    1.45980    1.46000
21     CNY/TRY    2.48949    2.48980
22     CNY/MXN    2.97690    2.97870
23     CNY/THB    5.24800    5.25000
```
