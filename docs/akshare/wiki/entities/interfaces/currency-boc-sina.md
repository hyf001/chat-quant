---
title: "currency_boc_sina - 人民币牌价数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fx, parameters, returns, example]
sources: [raw/data-dictionary/fx/fx.md]
confidence: high
---
# currency_boc_sina

- 分类: [[fx-fx|AKShare 外汇数据]]
- 主题路径: AKShare 外汇数据 > 人民币牌价数据
- 描述: 新浪财经-中行人民币牌价历史数据
- 目标地址: https://biz.finance.sina.com.cn/forex/forex.php?startdate=2012-01-01&enddate=2021-06-14&money_code=EUR&type=0
- 限量: 单次返回指定日期的所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/fx/fx.html

## 相关

- [[fx-fx|AKShare 外汇数据]]
- [[_meta/topic-map]]

## 源文摘录

### 人民币牌价数据

接口: currency_boc_sina

目标地址: https://biz.finance.sina.com.cn/forex/forex.php?startdate=2012-01-01&enddate=2021-06-14&money_code=EUR&type=0

描述: 新浪财经-中行人民币牌价历史数据

限量: 单次返回指定日期的所有历史数据

输入参数

| 名称         | 类型  | 描述                                                                                                                                                   |
|------------|-----|------------------------------------------------------------------------------------------------------------------------------------------------------|
| symbol     | str | symbol="美元"; choice of {'美元', '英镑', '欧元', '澳门元', '泰国铢', '菲律宾比索', '港币', '瑞士法郎', '新加坡元', '瑞典克朗', '丹麦克朗', '挪威克朗', '日元', '加拿大元', '澳大利亚元', '新西兰元', '韩国元'} |
| start_date | str | start_date="20230304"; 开始日期和结束日期之间的间隔要超过 6 个月                                                                                                        |
| end_date   | str | end_date="20231110"; 开始日期和结束日期之间的间隔要超过 6 个月                                                                                                          |

输出参数

| 名称        | 类型      | 描述      |
|-----------|---------|---------|
| 日期        | object  | -       |
| 中行汇买价     | float64 | 注意单位: 元 |
| 中行钞买价     | float64 | 注意单位: 元 |
| 中行钞卖价/汇卖价 | float64 | 注意单位: 元 |
| 央行中间价     | float64 | 注意单位: 元 |

接口示例

```python
import akshare as ak

currency_boc_sina_df = ak.currency_boc_sina(symbol="美元", start_date="20230304", end_date="20231110")
print(currency_boc_sina_df)
```

数据示例

```
    日期   中行汇买价   中行钞买价  中行钞卖价/汇卖价   央行中间价
0    2023-03-06  691.80  686.17     694.73  689.51
1    2023-03-07  694.49  688.84     697.44  691.56
2    2023-03-08  693.49  687.85     696.43  695.25
3    2023-03-09  695.04  689.39     697.99  696.66
4    2023-03-10  689.70  684.09     692.62  696.55
..          ...     ...     ...        ...     ...
175  2023-11-06  725.83  725.67     728.73  717.80
176  2023-11-07  726.73  726.57     729.63  717.76
177  2023-11-08  726.73  726.57     729.63  717.73
178  2023-11-09  727.28  727.12     730.18  717.72
179  2023-11-10  727.93  727.77     730.83  717.71
[180 rows x 5 columns]
```
