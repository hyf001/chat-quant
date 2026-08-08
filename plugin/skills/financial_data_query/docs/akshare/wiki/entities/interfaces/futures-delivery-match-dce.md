---
title: "futures_delivery_match_dce - 交割配对-大商所"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, futures, parameters, returns, example]
sources: [raw/data-dictionary/futures/futures.md]
confidence: high
---
# futures_delivery_match_dce

- 分类: [[futures-futures|AKShare 期货数据]]
- 主题路径: AKShare 期货数据 > 期货基础数据 > 交割配对-大商所
- 描述: 大连商品交易所-交割配对
- 目标地址: http://www.dce.com.cn/dalianshangpin/xqsj/tjsj26/jgtj/jgsj/index.html
- 限量: 单次返回指定品种的的交割配对数据
- 来源页面: https://akshare.akfamily.xyz/data/futures/futures.html

## 相关

- [[futures-futures|AKShare 期货数据]]
- [[_meta/topic-map]]

## 源文摘录

#### 交割配对-大商所

接口: futures_delivery_match_dce

目标地址: http://www.dce.com.cn/dalianshangpin/xqsj/tjsj26/jgtj/jgsj/index.html

描述: 大连商品交易所-交割配对

限量: 单次返回指定品种的的交割配对数据

输入参数

| 名称     | 类型  | 描述               |
|--------|-----|------------------|
| symbol | str | symbol="a"; 交易品种 |

输出参数

| 名称    | 类型      | 描述 |
|-------|---------|----|
| 合约号   | object  | -  |
| 配对日期  | object  | -  |
| 买会员号  | object  | -  |
| 配对手数  | int64   | -  |
| 卖会员号  | object  | -  |
| 交割结算价 | float64 | -  |

注意:

1 价格：自2019年12月02日起，纤维板报价单位由元/张改为元/立方米
2 配对手数：手
3 交割结算价：元/吨，鸡蛋为元/500千克，纤维板为元/立方米、胶合板为元/张
4 *为非期货公司会员

接口示例

```python
import akshare as ak

futures_delivery_match_dce_df = ak.futures_delivery_match_dce(symbol="a")
print(futures_delivery_match_dce_df)
```

数据示例

```
      合约号   配对日期  买会员号  配对手数   卖会员号   交割结算价
0     a1401  2014-01-02  0014     5  196.0  4425.0
1     a1401  2014-01-02  0014    26   51.0  4425.0
2     a1401  2014-01-02  0014     2   97.0  4425.0
3     a1401  2014-01-02  0014    20   52.0  4425.0
4     a1401  2014-01-02  0021     1  125.0  4425.0
     ...         ...   ...   ...    ...     ...
1415  a2401  2024-01-12  0051    78   51.0  4757.0
1416  a2401  2024-01-12  0110    21   51.0  4757.0
1417  a2401  2024-01-12  0173   200   51.0  4757.0
1418  a2401  2024-01-12  0196    40   51.0  4757.0
1419  a2401  2024-01-17  0196    10   30.0  4793.0
[1420 rows x 6 columns]
```
