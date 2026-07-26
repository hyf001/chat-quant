---
title: "broker_in_loss_list - 席位亏损排行"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/broker.md]
confidence: high
---
# broker_in_loss_list

- 分类: [[qhkc-broker|席位]]
- 主题路径: 席位 > 席位亏损排行
- 描述: 席位亏损排行数据接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/broker.html

## 相关

- [[qhkc-broker|席位]]
- [[_meta/topic-map]]

## 源文摘录

## 席位亏损排行

### 接口名称

broker_in_loss_list

### 接口描述

席位亏损排行数据接口

### 请求参数

| 参数名        | 说明     | 举例         |
|:-----------|:-------|------------|
| start_date | 查询开始日期 | 2018-07-08 |
| end_date   | 查询结束日期 | 2018-07-08 |
| count      | 返回数据条数 | 10; 默认10条  |

### 返回参数

| 参数名    | 类型     | 说明         |
|:-------|:-------|------------|
| broker | string | 席位         |
| profit | float  | 席位亏损金额，单位元 |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
broker_in_loss_list_df = pro.broker_in_loss_list(start_date="2018-07-08", end_date="2018-08-08", count="10")
print(broker_in_loss_list_df)
```

### 返回示例

```
  broker     profit
0   银河期货 -419310016
1   建信期货 -331576221
2   国贸期货 -287396120
3   南华期货 -286119224
4   格林大华 -282453330
5   光大期货 -278484680
6   招商期货 -200409531
7   国富期货 -183709404
8   中粮期货 -181432280
9   中辉期货 -165149465
```
