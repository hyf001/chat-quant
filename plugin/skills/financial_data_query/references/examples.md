# 查询样例

只在需要参考输出形态或工具调用格式时阅读本文件。

## A 股历史行情

用户问题：

```text
帮我查一下贵州茅台 2024 年 1 月的日线行情，给我前后几行和字段说明。
```

处理要点：

1. 用 `rg "贵州茅台|历史行情|stock_zh_a_hist" docs/akshare/wiki` 找候选接口。
2. 阅读最相关的接口页，确认函数名、参数、返回字段和数据限制。
3. 用 `mcp__chatq__python` 执行查询，不直接调用 Bash 或本机 Python。

工具调用示例：

```json
{
  "command": "run --code \"import akshare as ak\\nimport pandas as pd\\ndf = ak.stock_zh_a_hist(symbol='600519', period='daily', start_date='20240101', end_date='20240131', adjust='')\\nprint('shape:', df.shape)\\nprint('columns:', list(df.columns))\\nprint('head:')\\nprint(df.head(3).to_string(index=False))\\nprint('tail:')\\nprint(df.tail(3).to_string(index=False))\""
}
```

回答要包含：

- 使用的 AKShare 接口和关键参数。
- 数据行列规模、字段列表、前后几行。
- 数据源可能延迟、缺失、限流或口径变化；不把结果解释成投资建议。

## 脚本文件模式

当查询代码较长时，先在当前智能体工作项目目录下写脚本，例如：

```text
/当前智能体工作项目目录/queries/query_stock_daily.py
```

再调用：

```json
{
  "command": "run --code-file /当前智能体工作项目目录/queries/query_stock_daily.py"
}
```

注意：

- `--code-file` 必须是完整绝对路径。
- 文件必须位于当前智能体工作项目目录下。
- 不要传仓库外、系统目录、用户密钥目录或相对路径。
