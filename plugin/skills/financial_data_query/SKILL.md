---
name: financial_data_query
description: 当用户需要查询金融、行情、宏观、基金、期货、债券、指数、期权、外汇、加密货币或另类数据时使用。
---

# 金融数据查询

当用户询问金融数据、行情表、历史序列、财务指标、宏观指标、基金、期货、债券、指数成份、期权、外汇利率、加密货币或其他 AKShare 覆盖的数据时，使用本技能。

核心任务：按 `llm-wiki` 的方式阅读本地 AKShare wiki，选择合适的数据接口，编写并执行 Python 查询代码，然后把查到的数据、参数和来源限制清楚地反馈给用户。

## 本地知识源

AKShare wiki 位于：

- `docs/akshare/wiki/SCHEMA.md`：wiki 约定、标签和页面结构。
- `docs/akshare/wiki/index.md`：分类和接口总目录。
- `docs/akshare/wiki/_meta/topic-map.md`：按官方数据分类组织的主题地图。
- `docs/akshare/wiki/concepts/categories/*.md`：数据分类页。
- `docs/akshare/wiki/entities/interfaces/*.md`：接口页，包含参数、返回字段、示例代码和来源摘录。
- `docs/akshare/wiki/raw/data-dictionary/`：原始数据字典快照，仅在需要核对源文时阅读。

## 渐进式阅读

每次开始查数前，先做轻量定向：

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
2. 从 AKShare wiki 中找到候选接口，并说明选择依据。
3. 根据接口页里的参数和示例编写 Python 查询代码，不凭记忆猜参数。
4. 使用当前项目提供的 Python 环境直接执行 Python 代码。
5. 如果环境缺少 `akshare` 或依赖不可用，如实说明；不要切换到系统 Python，也不要擅自安装依赖。
6. 返回结果时说明接口、参数、行列规模、关键数据片段和来源限制。

## 编码规则

- 使用 `import akshare as ak`。
- 严格遵循 wiki 中记录的函数签名、参数取值和示例。
- 使用 `pandas` 做筛选、排序、日期解析、字段选择和预览格式化。
- 尽量缩小查询范围：能传代码、市场、日期范围或频率时就传。
- 大结果不要完整打印；优先输出 `shape`、必要的字段类型、`head()`、`tail()` 或筛选后的关键行。
- 把空数据、接口报错、限流、网络失败、数据源更新滞后视为正常可能性，并清楚报告。
- 不把查询结果包装成确定性投资建议；事实、解释和风险提示要分开。
