---
title: "broker_bbr - 席位多空比数据"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, qhkc, parameters, returns, example]
sources: [raw/data-dictionary/qhkc/broker.md]
confidence: high
---
# broker_bbr

- 分类: [[qhkc-broker|席位]]
- 主题路径: 席位 > 席位多空比数据
- 描述: 席位多空比数据接口
- 来源页面: https://akshare.akfamily.xyz/data/qhkc/broker.html

## 相关

- [[qhkc-broker|席位]]
- [[_meta/topic-map]]

## 源文摘录

## 席位多空比数据

### 接口名称

broker_bbr

### 接口描述

席位多空比数据接口

### 请求参数

| 参数名    | 说明   | 举例         |
|:-------|:-----|------------|
| broker | 席位   | 永安期货       |
| date   | 查询日期 | 2018-08-08 |

### 返回参数

| 参数名 | 类型    | 说明  |
|:----|:------|-----|
| bbr | float | 多空比 |

### 示例代码

```python
from akshare import pro_api
pro = pro_api(token="在此处输入您的 token, 可以联系奇货可查网站管理员获取")
broker_bbr_df = pro.broker_bbr(broker="永安期货", date="2018-08-08")
print(broker_bbr_df)
```

### 返回示例

```
     broker_bbr
bbr    54.36208
```
