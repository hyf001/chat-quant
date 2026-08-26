---
name: data-visualization
description: 使用 Chat-Quant visualization 工具生成严格校验的服务化 HTML 可视化。适用于单个图表、表格、卡片组和完整报表，支持折线图、柱状图、堆叠柱状图、饼图、散点图、热力图和 K线/candlestick。规格文件内直接包含数据；多记录图表和表格使用 columns + rows，卡片使用 label + value。不用于数据清洗、聚合、ETL、留存矩阵或宽松 fallback 渲染。
---

# Data Visualization

使用 `mcp__chatq__visualization` 生成可视化 HTML。

## 工作流

1. 根据用户目标选择 `chart`、`table`、`card` 或 `report`。
2. 在项目目录内编写 `.json`、`.yaml` 或 `.yml` 规格文件。
3. 先运行 `validate --file ... --kind ... --json`。
4. 校验通过后运行对应的 `render` 命令。
5. 将 `render` 返回的 `data.iframe_url` 作为前端嵌入地址。

`render` 会自动执行同等校验。校验失败时不会生成 HTML。

## 命令

工具入参是单个 `command` 字符串：

```json
{"command": "report render --file visualization/report.json --output-file visualization/report.html --json"}
```

可用命令：

```bash
schema chart|table|card|report [--json]
validate --file spec.json [--kind chart|table|card|report] [--json]
chart render --file chart.json --output-file visualization/chart.html [--json]
table render --file table.json --output-file visualization/table.html [--json]
card render --file cards.json --output-file visualization/cards.html [--json]
report render --file report.json --output-file visualization/report.html [--json]
```

路径必须位于当前项目目录内。输出文件必须是 `.html`。默认把生成文件放在 `visualization/` 目录；如果用户指定其他项目内路径，按用户要求处理。

## 通用字段

所有规格都有：

```json
{
  "kind": "chart | table | card | report",
  "title": "标题"
}
```

可选元信息：

```json
{
  "subtitle": "说明、范围或统计口径",
  "source": "数据来源、复权方式或计算依据"
}
```

`subtitle` 和 `source` 必须是非空字符串。

## 数据格式

多记录图表和表格统一使用 `data.columns` + `data.rows`：

```json
{
  "data": {
    "columns": ["date", "close"],
    "rows": [
      ["2026-08-21", 103.5],
      ["2026-08-24", 102.9]
    ]
  }
}
```

不要使用 `data_file`、对象数组行数据、内联 CSV 文本或外部数据引用。

卡片直接使用 `label` + `value`：

```json
{
  "kind": "card",
  "title": "核心指标",
  "cards": [
    {
      "label": "最新收盘价",
      "value": 103.5,
      "unit": "元",
      "format": "number",
      "decimals": 2
    }
  ]
}
```

卡片 `format` 可选：`number`、`integer`、`percent`、`currency`、`string`。

## 图表

折线图：

```json
{
  "kind": "chart",
  "title": "收盘价趋势",
  "type": "line",
  "data": {
    "columns": ["date", "close"],
    "rows": [
      ["2026-08-21", 103.5],
      ["2026-08-24", 102.9]
    ]
  },
  "x": {"field": "date"},
  "series": [{"name": "收盘价", "field": "close"}]
}
```

K线图：

```json
{
  "kind": "chart",
  "title": "股票K线",
  "type": "candlestick",
  "data": {
    "columns": ["date", "open", "close", "low", "high"],
    "rows": [
      ["2026-08-21", 101.2, 103.5, 100.8, 104.1],
      ["2026-08-24", 103.7, 102.9, 101.6, 104.4]
    ]
  },
  "x": {"field": "date"},
  "series": [
    {
      "name": "价格",
      "fields": {
        "open": "open",
        "close": "close",
        "low": "low",
        "high": "high"
      }
    }
  ]
}
```

饼图：

```json
{
  "kind": "chart",
  "title": "行业占比",
  "type": "pie",
  "data": {
    "columns": ["sector", "weight"],
    "rows": [["金融", 32.1], ["消费", 18.4]]
  },
  "series": [
    {
      "name": "权重",
      "name_field": "sector",
      "value_field": "weight"
    }
  ]
}
```

图表类型规则：

- `line` 和 `bar`：每个 `series` 使用 `field`，字段值必须为数字。
- `candlestick`：每个 `series` 使用 `fields.open`、`fields.close`、`fields.low`、`fields.high`，字段值必须为数字。
- `scatter`：每个 `series` 使用 `fields.x` 和 `fields.y`，字段值必须为数字。
- `heatmap`：只允许一个 `series`，使用 `fields.x`、`fields.y`、`fields.value`。
- `pie`：每个 `series` 使用 `name_field` 和 `value_field`，`value_field` 必须为数字。

## 表格

```json
{
  "kind": "table",
  "title": "交易明细",
  "data": {
    "columns": ["date", "close", "volume"],
    "rows": [["2026-08-21", 103.5, 1203400]]
  }
}
```

## 报表

报表可组合 `cards`、`charts` 和 `tables`。至少包含一种内容。

```json
{
  "kind": "report",
  "title": "市场分析报告",
  "subtitle": "近10个交易日走势与关键指标",
  "source": "a_stock_daily_price / 前复权",
  "layout": {"columns": 2},
  "cards": [
    {
      "label": "最新收盘价",
      "value": 103.5,
      "unit": "元",
      "format": "number",
      "decimals": 2
    }
  ],
  "charts": [
    {
      "title": "收盘价趋势",
      "type": "line",
      "data": {
        "columns": ["date", "close"],
        "rows": [
          ["2026-08-21", 103.5],
          ["2026-08-24", 102.9]
        ]
      },
      "x": {"field": "date"},
      "series": [{"name": "收盘价", "field": "close"}]
    }
  ],
  "tables": []
}
```

`layout.columns` 可选，取值为 `1`、`2` 或 `3`。

## 校验要求

严格按 schema 写规格。未知字段、缺失必填字段、字段类型错误、重复列名、行列数量不一致、字段引用不存在、数值字段非数字等都必须通过工具错误返回给智能体。

错误返回包含 `path`、`code`、`message` 和可选 `hint`。根据错误明细修正规格后重新运行 `validate` 或 `render`。不要在校验失败时手写替代 HTML。
