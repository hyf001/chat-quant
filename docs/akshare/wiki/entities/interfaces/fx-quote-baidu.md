---
title: "fx_quote_baidu - 外汇行情报价"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fx, parameters, returns, example]
sources: [raw/data-dictionary/fx/fx.md]
confidence: high
---
# fx_quote_baidu

- 分类: [[fx-fx|AKShare 外汇数据]]
- 主题路径: AKShare 外汇数据 > 外汇行情报价
- 描述: 百度股市通-外汇-行情榜单
- 目标地址: https://gushitong.baidu.com/top/foreign-rmb
- 限量: 单次返回指定 symbol 当前时点的行情报价
- 来源页面: https://akshare.akfamily.xyz/data/fx/fx.html

## 相关

- [[fx-fx|AKShare 外汇数据]]
- [[_meta/topic-map]]

## 源文摘录

### 外汇行情报价

接口: fx_quote_baidu

目标地址: https://gushitong.baidu.com/top/foreign-rmb

描述: 百度股市通-外汇-行情榜单

限量: 单次返回指定 symbol 当前时点的行情报价

输入参数

| 名称     | 类型  | 描述                                   |
|--------|-----|--------------------------------------|
| symbol | str | symbol="人民币"; choice of {"人民币", 美元"} |
| token  | str | 目标网站复制 acs-token 后传入                 |

输出参数

| 名称  | 类型      | 描述  |
|-----|---------|-----|
| 代码  | object  | -   |
| 名称  | object  | -   |
| 最新价 | float64 | -   |
| 涨跌额 | float64 | -   |
| 涨跌幅 | float64 | -   |

接口示例

```python
import akshare as ak

fx_quote_baidu_df = ak.fx_quote_baidu(symbol="人民币")
print(fx_quote_baidu_df)
```

数据示例

```
         代码         名称       最新价     涨跌额     涨跌幅
0    CNYSCR      人民币塞舌尔卢比    2.1391  0.2164  0.1126
1    CNYETH   人民币Ethereum    0.0000  0.0000  0.0217
2    CNYSBD     人民币所罗门群岛元    1.1711  0.0224  0.0195
3    CNYTOP       人民币汤加潘加    0.3461  0.0038  0.0111
4    CNYMDL     人民币摩尔多瓦列伊    2.4150  0.0238  0.0100
..      ...           ...       ...     ...     ...
150  CNYXPT       人民币珀价盎司    0.0001 -0.0000 -0.0071
151  CNYPKR     人民币巴基斯坦卢比   40.1263 -0.3054 -0.0076
152  CNYMGA  人民币马达加斯加阿里亚里  655.2200 -7.9000 -0.0119
153  CNYRUB      人民币俄罗斯卢布   11.3331 -0.1375 -0.0120
154  CNYXAG       人民币银价盎司    0.0018 -0.0000 -0.0151
[155 rows x 5 columns]
```
