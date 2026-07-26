---
title: "stock_institute_hold_detail - 机构持股详情"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_institute_hold_detail

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 机构持股 > 机构持股详情
- 描述: 新浪财经-机构持股-机构持股详情
- 目标地址: http://vip.stock.finance.sina.com.cn/q/go.php/vComStockHold/kind/jgcg/index.phtml
- 限量: 单次所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 机构持股详情

接口: stock_institute_hold_detail

目标地址: http://vip.stock.finance.sina.com.cn/q/go.php/vComStockHold/kind/jgcg/index.phtml

描述: 新浪财经-机构持股-机构持股详情

限量: 单次所有历史数据

输入参数

| 名称      | 类型  | 描述                                                                                                               |
|---------|-----|------------------------------------------------------------------------------------------------------------------|
| stock   | str | stock="300003"; 股票代码                                                                                             |
| quarter | str | quarter="20201"; 从 2005 年开始, {"一季报":1, "中报":2 "三季报":3 "年报":4}, e.g., "20191", 其中的 1 表示一季报; "20193", 其中的 3 表示三季报; |

输出参数

| 名称       | 类型      | 描述       |
|----------|---------|----------|
| 持股机构类型   | object  | -        |
| 持股机构代码   | object  | -        |
| 持股机构简称   | object  | -        |
| 持股机构全称   | object  | -        |
| 持股数      | float64 | 注意单位: 万股 |
| 最新持股数    | float64 | 注意单位: 万股 |
| 持股比例     | float64 | 注意单位: %  |
| 最新持股比例   | float64 | 注意单位: %  |
| 占流通股比例   | float64 | 注意单位: %  |
| 最新占流通股比例 | float64 | 注意单位: %  |
| 持股比例增幅   | float64 | 注意单位: %  |
| 占流通股比例增幅 | float64 | 注意单位: %  |

接口示例

```python
import akshare as ak

stock_institute_hold_detail_df = ak.stock_institute_hold_detail(stock="300003", quarter="20201")
print(stock_institute_hold_detail_df)
```

数据示例

```
   持股机构类型  持股机构代码      持股机构简称  ... 最新占流通股比例  持股比例增幅  占流通股比例增幅
0      基金    519069          汇添富价值精选混合A  ...     1.18   -0.22     -0.23
1      基金    159915           易方达创业板ETF  ...     0.73    0.02      0.02
2      基金    001417      汇添富医疗服务灵活配置混合A  ...     1.01   -0.35     -0.37
3      基金    470009          汇添富民营活力混合A  ...     0.48    0.03      0.02
4      基金    159949          华安创业板50ETF  ...     0.36    0.13      0.13
5      基金    000831            工银医疗保健股票  ...     0.57   -0.09     -0.10
6    全国社保  70010117         全国社保基金一一七组合  ...     1.30   -0.22     -0.23
7    全国社保  70010104         全国社保基金一零四组合  ...     0.60   -0.06     -0.07
8    全国社保  70010503         全国社保基金五零三组合  ...     0.38    0.07      0.07
9      保险  70304136  华夏人寿保险股份有限公司－自有...  ...     0.00    1.39      1.47
10   QFII  70304002         挪威中央银行－自有资金  ...     0.90    0.25      0.27
11   QFII  70304274        澳门金融管理局－自有资金  ...     0.99    0.00      0.00
12   QFII  80126479           魁北克储蓄投资集团  ...     0.71    0.00      0.00
13   QFII  70304150  鼎晖投资咨询新加坡有限公司－鼎...  ...     0.57    0.01      0.01
14   QFII  80128964             阿布达比投资局  ...     0.56    0.02      0.02
15   QFII  80195934            科威特政府投资局  ...     0.39    0.04      0.04
[16 rows x 12 columns]
```
