---
title: "stock_hold_management_person_em - 人员增减持股变动明细"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, stock, parameters, returns, example]
sources: [raw/data-dictionary/stock/stock.md]
confidence: high
---
# stock_hold_management_person_em

- 分类: [[stock-stock|AKShare 股票数据]]
- 主题路径: 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0 > 基本面数据 > 机构推荐 > 人员增减持股变动明细
- 描述: 东方财富网-数据中心-特色数据-高管持股-人员增减持股变动明细
- 目标地址: https://data.eastmoney.com/executive/personinfo.html?name=%E5%90%B4%E8%BF%9C&code=001308
- 限量: 单次返回指定 symbol 和 name 的数据
- 来源页面: https://akshare.akfamily.xyz/data/stock/stock.html

## 相关

- [[stock-stock|AKShare 股票数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 人员增减持股变动明细

接口: stock_hold_management_person_em

目标地址: https://data.eastmoney.com/executive/personinfo.html?name=%E5%90%B4%E8%BF%9C&code=001308

描述: 东方财富网-数据中心-特色数据-高管持股-人员增减持股变动明细

限量: 单次返回指定 symbol 和 name 的数据

输入参数

| 名称     | 类型  | 描述                    |
|--------|-----|-----------------------|
| symbol | str | symbol="001308"; 股票代码 |
| name   | str | name="吴远"; 高管名称       |

输出参数

| 名称         | 类型      | 描述 |
|------------|---------|----|
| 日期         | object  | -  |
| 代码         | object  | -  |
| 名称         | object  | -  |
| 变动人        | object  | -  |
| 变动股数       | int64   | -  |
| 成交均价       | int64   | -  |
| 变动金额       | float64 | -  |
| 变动原因       | object  | -  |
| 变动比例       | float64 | -  |
| 变动后持股数     | float64 | -  |
| 持股种类       | object  | -  |
| 董监高人员姓名    | object  | -  |
| 职务         | object  | -  |
| 变动人与董监高的关系 | object  | -  |
| 开始时持有      | float64 | -  |
| 结束后持有      | float64 | -  |

接口示例

```python
import akshare as ak

stock_hold_management_person_em_df = ak.stock_hold_management_person_em(symbol="001308", name="孙建华")
print(stock_hold_management_person_em_df)
```

数据示例

```
   日期      代码    名称 变动人   变动股数  ...  董监高人员姓名    职务 变动人与董监高的关系    开始时持有  结束后持有
0  2023-08-08  001308  康冠科技  吴远  10000  ...       吴远  财务总监         本人  64350.0  74350
1  2022-08-24  001308  康冠科技  吴远  14000  ...       吴远    高管         本人      NaN  49500
2  2022-06-17  001308  康冠科技  吴远  35500  ...       吴远  财务总监         本人      0.0  35500
[3 rows x 16 columns]
```
