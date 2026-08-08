---
title: "amac_manager_cancelled_info - 已注销私募基金管理人名单"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, fund, parameters, returns, example]
sources: [raw/data-dictionary/fund/fund_private.md]
confidence: high
---
# amac_manager_cancelled_info

- 分类: [[fund-fund-private|AKShare 私募基金数据]]
- 主题路径: AKShare 私募基金数据 > 中国证券投资基金业协会 > 诚信信息 > 已注销私募基金管理人名单
- 描述: 中国证券投资基金业协会-信息公示-诚信信息-已注销私募基金管理人名单
- 目标地址: https://gs.amac.org.cn/amac-infodisc/res/cancelled/manager/index.html
- 限量: 单次返回当前时刻所有历史数据
- 来源页面: https://akshare.akfamily.xyz/data/fund/fund_private.html

## 相关

- [[fund-fund-private|AKShare 私募基金数据]]
- [[_meta/topic-map]]

## 源文摘录

##### 已注销私募基金管理人名单

接口: amac_manager_cancelled_info

目标地址: https://gs.amac.org.cn/amac-infodisc/res/cancelled/manager/index.html

描述: 中国证券投资基金业协会-信息公示-诚信信息-已注销私募基金管理人名单

限量: 单次返回当前时刻所有历史数据

输入参数

| 名称 | 类型 | 描述 |
|----|----|----|
| -  | -  | -  |

输出参数

| 名称       | 类型     | 描述 |
|----------|--------|----|
| 管理人名称    | object | -  |
| 统一社会信用代码 | object | -  |
| 登记时间     | object | -  |
| 注销时间     | object | -  |
| 注销类型     | object | -  |

接口示例

```python
import akshare as ak

amac_manager_cancelled_info_df = ak.amac_manager_cancelled_info()
print(amac_manager_cancelled_info_df)
```

数据示例

```
           管理人名称            统一社会信用代码        登记时间        注销时间  注销类型
0        北京国民信和投资基金有限公司          05559209-0  2014-05-26  2015-04-07   100
1            湖南海盟投资有限公司          68501913-3  2014-05-26  2015-04-07   100
2      广元友利股权投资基金管理有限公司          07144608-5  2014-11-26  2015-04-07   100
3        上海骏福股权投资基金有限公司          06784881-5  2014-06-04  2015-04-07   100
4        上海清科凯盛投资管理有限公司          59312920-4  2014-04-23  2015-04-07   100
                 ...                 ...         ...         ...   ...
22267      上海津尧资产管理有限公司          34224529-4  2015-07-30  2024-04-02   100
22268     深圳市清江基金管理有限公司  91440300335206596E  2017-07-12  2024-04-02   100
22269      苏州宝时投资管理有限公司          31419103-0  2014-11-19  2024-04-03   100
22270     深圳市禾瑞股权投资有限公司  91440300MA5D9XA002  2017-01-23  2024-04-03   100
22271  中楚私募基金管理（海南）有限公司  91460200MAA95MYA9Q  2023-04-03  2024-04-04   200
[22272 rows x 5 columns]
```
