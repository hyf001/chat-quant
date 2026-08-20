# Dataset API

平台数据集是金融数据查询的默认入口。用户需要行情、历史序列、财务、因子、指数、宏观等数据时，先用本参考中的 Dataset API 查已注册数据集；只有没有合适数据集时，再考虑 AKShare 或其他外部接口。

## 导入

在 `mcp__chatq__python` 执行的 Python 代码中使用：

```python
from app.service.dataset.python_api import (
    list_datasets,
    describe_dataset,
    preview_dataset,
    query_dataset,
)
```

不要绕过 Dataset API 访问底层实现；查询时只需要关心数据集名称、字段和 SQL。

## 函数

```python
list_datasets(category=None)
```

返回已暴露给智能体的数据集，类型为 `pandas.DataFrame`。常用字段：

- `id`
- `name`
- `description`
- `category_path`
- `exposed_to_agent`
- `updated_at`

```python
describe_dataset(dataset)
```

返回 `dict`，包含：

- `id`
- `name`
- `description`
- `category_path`
- `create_sql`
- `columns`
- `sample_sql`

写 SQL 前必须先查看 `columns`，不要凭记忆猜字段名。

```python
preview_dataset(dataset, limit=20)
```

返回指定数据集的前几行 `pandas.DataFrame`。

```python
query_dataset(sql)
```

执行只读 `SELECT`，返回 `pandas.DataFrame`。只能查询已暴露给智能体的数据集；API 不会自动追加 `LIMIT`，传入什么 SQL 就执行什么 SQL。需要限制结果时，在 SQL 中显式写 `LIMIT`。

## 查询流程

1. 用 `list_datasets()` 找候选数据集。
2. 用 `describe_dataset(dataset_id)` 确认字段、视图名和口径。
3. 用 `preview_dataset(dataset_id)` 快速检查数据形态。
4. 用 `query_dataset(sql)` 查询目标结果。
5. 如果数据集不存在、未暴露、字段不匹配或为空，优先尝试其他平台数据集，再考虑外部接口。

## 示例

列出数据集：

```python
from app.service.dataset.python_api import list_datasets

datasets = list_datasets()
print(datasets[["id", "name", "description", "category_path"]].to_string(index=False))
```

查看字段：

```python
from app.service.dataset.python_api import describe_dataset

info = describe_dataset("stock_a_daily_price")
print(info["description"])
print(info["columns"])
print(info["sample_sql"])
```

查询日线行情：

```python
from app.service.dataset.python_api import query_dataset

df = query_dataset(
    """
    SELECT symbol, trade_date, open, high, low, close, volume
    FROM stock_a_daily_price
    WHERE symbol = '600519.SH'
      AND trade_date BETWEEN '2024-01-01' AND '2024-01-31'
    ORDER BY trade_date
    LIMIT 200
    """,
)
print("shape:", df.shape)
print(df.head(3).to_string(index=False))
print(df.tail(3).to_string(index=False))
```

## SQL 规则

- SQL 方言是 DuckDB SQL。
- 只写 `SELECT` 查询。
- 大结果必须加日期、代码、市场、分类或 `LIMIT` 约束。
- 字段名以 `describe_dataset()` 返回为准。
- 只能查询已暴露给智能体的数据集。
- 不要执行 `CREATE`、`DROP`、`INSERT`、`UPDATE`、`DELETE`、`COPY`、`ATTACH`、`INSTALL`、`LOAD` 等语句。

## 回答用户时

回答应包含：

- 使用的数据集 ID 或视图名。
- 查询条件：标的、日期范围、字段、排序或聚合口径。
- 结果行列规模和关键片段。
- 数据可能存在延迟、缺失、复权/单位/交易日口径差异；不把查询结果包装成投资建议。
