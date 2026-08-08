---
title: "stock_gdfx_holding_change_em - 股东持股变动统计-十大股东"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_gdfx_holding_change_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 股东持股变动统计-十大股东
- 描述: 东方财富网-数据中心-股东分析-股东持股变动统计-十大股东
- 目标地址: https://data.eastmoney.com/gdfx/HoldingAnalyse.html
- 限量: 单次返回指定 date 的所有数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 股东持股变动统计-十大股东

接口: stock_gdfx_holding_change_em

目标地址: https://data.eastmoney.com/gdfx/HoldingAnalyse.html

描述: 东方财富网-数据中心-股东分析-股东持股变动统计-十大股东

限量: 单次返回指定 date 的所有数据

输入参数

| 名称   | 类型  | 描述                         |
|------|-----|----------------------------|
| date | str | date="20210930"; 财报发布季度最后日 |

输出参数

| 名称           | 类型      | 描述      |
|--------------|---------|---------|
| 序号           | int64   | -       |
| 股东名称         | object  | -       |
| 股东类型         | object  | -       |
| 期末持股只数统计-总持有 | float64 | -       |
| 期末持股只数统计-新进  | float64 | -       |
| 期末持股只数统计-增加  | float64 | -       |
| 期末持股只数统计-不变  | float64 | -       |
| 期末持股只数统计-减少  | float64 | -       |
| 流通市值统计       | float64 | 注意单位: 元 |
| 持有个股         | object  | -       |

接口示例

```python
import akshare as ak

stock_gdfx_holding_change_em_df = ak.stock_gdfx_holding_change_em(date="20210930")
print(stock_gdfx_holding_change_em_df)
```

数据示例

```
          序号  ...                                               持有个股
0          1  ...  600763|通策医疗,300229|拓尔思,603039|泛微网络,300006|莱美药业...
1          2  ...  002225|濮耐股份,600435|北方导航,600422|昆药集团,600009|上海机...
2          3  ...  600340|华夏幸福,600009|上海机场,000001|平安银行,601899|紫金矿...
3          4  ...  601865|福莱特,601899|紫金矿业,000756|新华制药,600036|招商银行...
4          5  ...  002479|富春环保,300582|英飞特,300358|楚天科技,002892|科力尔,...
      ...  ...                                                ...
33896  33897  ...                                        300047|天源迪科
33897  33898  ...                                        300969|恒帅股份
33898  33899  ...                                        000425|徐工机械
33899  33900  ...                                        002896|中大力德
33900  33901  ...                            000761|本钢板材,200761|本钢板B
```
