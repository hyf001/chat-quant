---
name: financial_data_query
description: 当用户需要通过平台数据集或金融数据接口查询行情、宏观、基金、期货、债券、指数、期权、外汇、加密货币或另类数据时使用。
---

# 金融数据查询

当用户询问金融数据、行情表、历史序列、财务指标、宏观指标、基金、期货、债券、指数成份、期权、外汇利率、加密货币或其他平台覆盖的数据时，使用本技能。

核心任务：优先使用平台 Dataset Python API 查询已注册数据集；只有数据集没有覆盖、用户明确要求外部接口、或任务需要核对外部数据源时，才按 `llm-wiki` 的方式阅读本地 AKShare wiki 并调用 AKShare。查询后把数据集或接口、参数、口径和来源限制清楚地反馈给用户。

## 数据源优先级

1. **优先使用平台数据集**：使用 `app.service.dataset.python_api` 中的 `list_datasets`、`describe_dataset`、`preview_dataset`、`query_dataset`。需要写查询代码或确认调用方式时，阅读 `references/dataset-api.md`。
2. **再考虑 AKShare**：只有平台数据集没有合适覆盖、数据集查询失败且无法换用其他数据集、用户明确要求 AKShare、或需要核对外部公开数据源时，才使用 AKShare wiki。
3. 不要在未检查平台数据集前直接 `import akshare as ak`。

## 本地知识源

Dataset API 参考：

- `references/dataset-api.md`：平台数据集查询 façade、函数说明、SQL 规则和代码样例。

AKShare wiki 位于，仅在需要 AKShare 时阅读：

- `docs/akshare/wiki/SCHEMA.md`：wiki 约定、标签和页面结构。
- `docs/akshare/wiki/index.md`：分类和接口总目录。
- `docs/akshare/wiki/_meta/topic-map.md`：按官方数据分类组织的主题地图。
- `docs/akshare/wiki/concepts/categories/*.md`：数据分类页。
- `docs/akshare/wiki/entities/interfaces/*.md`：接口页，包含参数、返回字段、示例代码和来源摘录。
- `docs/akshare/wiki/raw/data-dictionary/`：原始数据字典快照，仅在需要核对源文时阅读。

需要参考 AKShare 查询样例或工具调用格式时，阅读 `references/examples.md`。

## Python 执行环境

执行查询代码时，使用平台提供的 `mcp__chatq__python` 工具，不要写死本机 Python 路径，也不要直接调用 Bash、`python`、`.venv/bin/python` 或系统解释器。

工具入参是 `command` 字符串；实际传入 `command` 的内容从 `run` 开始：

```text
run --code "..."
```

或先在当前智能体工作项目目录下生成查询脚本，再用完整绝对路径执行：

```text
run --code-file /当前智能体工作项目目录/queries/query_financial_data.py
```

使用 `--code-file` 时，路径必须是当前智能体工作项目目录下的完整绝对路径；不要传相对路径，不要传仓库外、系统目录或用户敏感目录中的文件。

## 渐进式阅读

每次开始查数前，先做轻量定向：

1. 读 `references/dataset-api.md`，用 Dataset API 列出已暴露数据集，并按用户关键词、资产类别、字段、日期口径寻找候选数据集。
2. 对候选数据集先 `describe_dataset()`，确认字段名、视图名、口径和可查询范围，再写 SQL。
3. 如果没有合适数据集，再进入 AKShare wiki 定向阅读。

使用 AKShare 前再做：

1. 读 `SCHEMA.md`，确认 wiki 结构和约定。
2. 读 `index.md`，定位可能的数据分类或接口。
3. 浏览相关 `concepts/categories/` 分类页和 `entities/interfaces/` 接口页，确认候选数据源。

然后按问题逐步深入：

1. 先用 `rg` 搜索用户的关键词、中文数据名、资产类别、接口名或字段名。
2. 读最相关的分类页或 `_meta/topic-map.md`，缩小接口范围。
3. 只读取候选接口页，确认函数名、参数、返回字段、示例和限制。
4. 只有接口页信息不足或需要核对源文时，才读取 `raw/data-dictionary/` 里的原始快照。

优先使用精确接口页，不要一次性加载大量 wiki 文件。

## 查询流程

1. 仅在必要时向用户澄清关键条件：标的、市场、代码、日期范围、频率、字段或输出格式。
2. 先用 Dataset API 找候选数据集，并说明选择依据；优先查询 `exposed_to_agent=true` 的数据集。
3. 根据 `describe_dataset()` 返回的字段写 SQL，不凭记忆猜字段名；查询只写 `SELECT`，大结果加 `LIMIT` 或聚合。
4. 使用 `mcp__chatq__python` 执行 Python 查询代码。
5. 如果数据集不存在、未暴露、字段不匹配或返回空数据，先换用其他平台数据集或调整 SQL；仍不满足时再考虑 AKShare。
6. 如需 AKShare，从 AKShare wiki 中找到候选接口，并说明选择依据；同类数据尽量同时识别 2-3 个可替代接口。
7. 返回结果时说明数据集 ID/视图名或外部接口、参数、SQL 摘要、行列规模、关键数据片段和来源限制。

## 失败重试策略

- 数据集查询失败时，先检查 `describe_dataset()` 字段、日期格式、代码格式和暴露状态，再尝试同类数据集。
- 使用 AKShare 时，单个接口失败至少尝试 1 个同类替代接口；如果 wiki 中有明确的多数据源接口，优先尝试 2-3 个不同数据源。
- A 股历史行情常见替代方向包括东财、腾讯、新浪等来源；以本地 wiki 记录为准，不凭记忆编造函数名。
- 只有在平台数据集和必要的替代外部接口都不能满足时，才向用户说明无法完成。
- 最终答复要区分“成功数据集/接口”和“失败数据集/接口”，简要列出失败名称、关键参数和失败原因；不要只建议用户稍后重试。

## 编码规则

- 优先从 `app.service.dataset.python_api` 导入 Dataset API 函数，不直接读取 SQLite、DuckDB 或 Parquet 文件。
- 使用 AKShare 时再 `import akshare as ak`，并严格遵循 wiki 中记录的函数签名、参数取值和示例。
- 使用 `pandas` 做筛选、排序、日期解析、字段选择和预览格式化。
- 尽量缩小查询范围：能传代码、市场、日期范围或频率时就传。
- 大结果不要完整打印；优先输出 `shape`、必要的字段类型、`head()`、`tail()` 或筛选后的关键行。
- 把空数据、接口报错、限流、网络失败、数据源更新滞后视为正常可能性，并清楚报告。
- 不把查询结果包装成确定性投资建议；事实、解释和风险提示要分开。
