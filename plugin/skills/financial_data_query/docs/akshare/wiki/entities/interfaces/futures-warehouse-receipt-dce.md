---
title: "futures_warehouse_receipt_dce - 仓单日报-大连商品交易所"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, futures, parameters, returns, example]
sources: [raw/data-dictionary/futures/futures.md]
confidence: high
---
# futures_warehouse_receipt_dce

- 分类: [[futures-futures|AKShare 期货数据]]
- 主题路径: AKShare 期货数据 > 期货基础数据 > 仓单日报 > 仓单日报-大连商品交易所
- 描述: 大连商品交易所-行情数据-统计数据-日统计-仓单日报
- 目标地址: http://www.dce.com.cn/dce/channel/list/187.html
- 限量: 单次返回当前交易日的所有仓单日报数据
- 来源页面: https://akshare.akfamily.xyz/data/futures/futures.html

## 相关

- [[futures-futures|AKShare 期货数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 仓单日报-大连商品交易所

接口: futures_warehouse_receipt_dce

目标地址: http://www.dce.com.cn/dce/channel/list/187.html

描述: 大连商品交易所-行情数据-统计数据-日统计-仓单日报

限量: 单次返回当前交易日的所有仓单日报数据

输入参数

| 名称   | 类型  | 描述                   |
|------|-----|----------------------|
| date | str | date="20251027"; 交易日 |

输出参数

| 名称           | 类型     | 描述 |
|--------------|--------|----|
| 品种代码         | object | -  |
| 品种名称         | object | -  |
| 仓库/分库        | object | -  |
| 可选提货地点/分库-数量 | object | -  |
| 昨日仓单量（手）     | int64  | -  |
| 今日仓单量（手）     | int64  | -  |
| 增减（手）        | int64  | -  |

接口示例

```python
import akshare as ak

futures_warehouse_receipt_dce_df = ak.futures_warehouse_receipt_dce(date="20251027")
print(futures_warehouse_receipt_dce_df)
```

数据示例

```
     品种代码  品种名称   仓库/分库 可选提货地点/分库-数量  昨日仓单量（手）  今日仓单量（手）  增减（手）
0       a    豆一   哈尔滨益海         None      2200      2200      0
1       a    豆一  桦南宏安粮贸         None       200       200      0
2       a    豆一    源发物流         None      3021      3021      0
3       a    豆一    嫩江九三         None       454       454      0
4       a    豆一    中船东北         None      1215      1215      0
..    ...   ...     ...          ...       ...       ...    ...
186     y    豆油    天津九三         None      1200      1200      0
187     y    豆油    河北嘉好         None      2000      2000      0
188     y    豆油    钦州中粮         None      2000      2000      0
189     y  豆油小计    None         None     27344     27144   -200
190  None    总计    None         None    315072    314394   -678
```
