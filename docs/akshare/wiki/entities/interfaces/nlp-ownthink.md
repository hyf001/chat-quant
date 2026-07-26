---
title: "nlp_ownthink - 知识图谱"
created: 2026-07-26
updated: 2026-07-26
type: entity
tags: [akshare, data-dictionary, interface, nlp, parameters, returns, example]
sources: [raw/data-dictionary/nlp/nlp.md]
confidence: high
---
# nlp_ownthink

- 分类: [[nlp-nlp|AKShare 自然语言处理]]
- 主题路径: AKShare 自然语言处理 > 知识图谱
- 描述: 思知-知识图谱的接口, 以此来查询知识图谱数据
- 目标地址: https://ownthink.com/
- 限量: 单次返回查询的数据结果
- 来源页面: https://akshare.akfamily.xyz/data/nlp/nlp.html

## 相关

- [[nlp-nlp|AKShare 自然语言处理]]
- [[_meta/topic-map]]

## 源文摘录

### 知识图谱

接口: nlp_ownthink

目标地址: https://ownthink.com/

描述: 思知-知识图谱的接口, 以此来查询知识图谱数据

限量: 单次返回查询的数据结果

输入参数

| 名称        | 类型  | 描述                                                        |
|-----------|-----|-----------------------------------------------------------|
| word      | str | word="人工智能"                                               |
| indicator | str | indicator="entity"; Please refer **Indicator Info** table |

Indicator Info

| fields | type             | description                    |
|--------|------------------|--------------------------------|
| entity | str              | 	实体名                           |
| desc   | str              | 	实体简介                          |
| tag    | list             | 	实体标签                          |
| avg    | pandas.DataFrame | 	实体属性值，第一列为实体的属性，第二列为实体属性所对应的值 |

输出参数-entity

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | str | 结果  |

接口示例-entity

```python
import akshare as ak

nlp_ownthink_df = ak.nlp_ownthink(word="人工智能", indicator="entity")
print(nlp_ownthink_df)
```

数据示例-entity

```
人工智能[计算机科学的一个分支]
```

输出参数-desc

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | str | 结果  |

接口示例-desc

```python
import akshare as ak

nlp_ownthink_df = ak.nlp_ownthink(word="人工智能", indicator="desc")
print(nlp_ownthink_df)
```

数据示例-desc

```
人工智能（Artificial Intelligence），英文缩写为AI。
```

输出参数-avg

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | str | 结果  |

接口示例-avg

```python
import akshare as ak

nlp_ownthink_df = ak.nlp_ownthink(word="人工智能", indicator="avg")
print(nlp_ownthink_df)
```

数据示例-avg

```
     字段                       值
0   中文名                    人工智能
1   外文名  ARTIFICIALINTELLIGENCE
2    简称                      AI
3  提出时间                   1956年
4  提出地点             DARTMOUTH学会
5  名称来源             雨果·德·加里斯的著作
```

输出参数-tag

| 名称  | 类型   | 描述  |
|-----|------|-----|
| -   | list | 结果  |

接口示例-tag

```python
import akshare as ak

nlp_ownthink_df = ak.nlp_ownthink(word="人工智能", indicator="tag")
print(nlp_ownthink_df)
```

数据示例-tag

```
['中国通信学会', '学科']
```
