---
title: "broker_pk - 席位对对碰"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/broker.md]
confidence: high
---
# broker_pk

- 分类: [[qhkc-broker|席位]]
- 主题路径: 席位 > 席位对对碰
- 描述: 席位对对碰数据接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/broker.html

## 相关

- [[qhkc-broker|席位]]
- [[_meta/topic-map]]

## 源文摘录

## 席位对对碰

### 接口名称

broker_pk

### 接口描述

席位对对碰数据接口

### 请求参数

| 参数名     | 说明   | 举例   |
|:--------|:-----|------|
| broker1 | 席位1  | 永安期货 |
| broker2 | 席位2  | 兴证期货 |
| symbol  | 品种编码 | 螺纹钢  |

### 返回参数

| 参数名              | 类型  | 说明           |
|:-----------------|:----|--------------|
| total_count      | int | 统计数据量        |
| win_count        | int | 席位1获胜次数      |
| recent_win_count | int | 席位1最近10次获胜次数 |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
broker_pk_df = pro.broker_pk(broker1="永安期货", broker2="兴证期货", symbol="RB")
print(broker_pk_df)
```

### 返回示例

```
                  broker_pk
total_count             614
win_count               295
recent_win_count          4
```
