---
title: MindGo indexmap / Arsenal query_index 方法
created: 2026-08-11
updated: 2026-08-11
type: concept
tags: ["mindgo", "indexmap", "arsenal", "stock", "market-data"]
sources: ["raw/code/indexmap-arsenal-query.py.md"]
confidence: high
---
# MindGo indexmap / Arsenal query_index 方法

`获取indexmap指标数据方法.py` 展示了另一条数据入口：在 MindGo 环境中调用 `get_arsenal_api('cbas-babel-frondend-pod')`，再 POST 到 `/babel/api/query_index`。

当前脚本核心结构：

```python
api = get_arsenal_api('cbas-babel-frondend-pod')
r = api.post('/babel/api/query_index', files={'queryId': (None, apiid), 'baseDay': (None, BASE_TIME)})
data = r.json()
key_to_label = {item['key']: item['label'] for item in data['titles']}
```

参数含义：

- `apiid`：指标/接口 ID，例如脚本注释中提到 `985` 表示异动股票。
- `BASE_TIME`：交易日期，格式 `YYYYMMDD`。
- 返回 JSON 中的 `titles` 可映射字段 key 到中文 label。

注意：脚本目前创建了 `processed_data = []` 但没有把返回行数据解析进去，因此它是“入口方法”而非完整可用的数据转换器。后续应从 `data` 中确认 rows/list 的真实字段，再生成 DataFrame。常规行情取数优先参考 [[mindgo-market-data-api]]；需要远程执行时参考 [[mindgo-jupyter-python-execution]]。
