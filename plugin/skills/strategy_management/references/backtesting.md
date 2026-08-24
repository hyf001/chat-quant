# 策略回测

## 执行入口

使用 MCP 工具 `mcp__chatq__strategy`，只传一个 CLI-style `command` 字符串。下面所有代码块都是 `command` 字符串本身，不是 Bash 命令，也不是 JSON：

```text
<subcommand> [--flags]
```

不要用 Bash 或本地 HTTP 请求替代 MCP 工具。当前业务项目由后端绑定，不要传 `--project-path`、`--project-id`、`--user-id` 或 API base URL。

ID 前缀含义：

- `str_xxx`：策略 ID，只能用于 `backtest`、`show`、`versions` 等策略命令。
- `stv_xxx`：策略版本 ID，用于 `backtest run --strategy-version-id` 和 `backtest list --strategy-version-id`。
- `sbt_xxx`：回测记录 ID，用于 `backtest show --backtest-id`。

不确定参数时先调用：

```text
backtest run --help
backtest list --help
backtest show --help
backtest trades --help
backtest equity --help
```

## 默认回测当前版本

不传版本 ID 时，回测当前策略版本：

```text
backtest run --strategy-id str_xxx --symbol 600519.SH --start 2024-01-01 --end 2024-04-30 --cash 100000 --commission 0.001 --slippage 0.0002
```

工具会自动推断策略模式；不要传 `--mode`。

## 指定版本回测

需要对比历史版本时传 `--strategy-version-id`：

```text
backtest run --strategy-id str_xxx --strategy-version-id stv_xxx --symbol 600519.SH --start 2024-01-01 --end 2024-04-30
```

## 运行时参数覆盖

只用 `--param key=value` 覆盖源码协议中已注册的参数：

```text
backtest run --strategy-id str_xxx --symbol 600519.SH --start 2024-01-01 --end 2024-04-30 --param buy_drop_pct=0.10 --param sell_rise_pct=0.20 --param step_pct=0.10
```

不要用 `--param` 传策略参数 schema。

## 标的和周期

回测时传交易标的、日期、资金和费用参数即可。不要主动传 `--market` 或 `--asset-class`。

单标的策略传一个 `--symbol`；多标的策略重复传多个 `--symbol`：

```text
backtest run --strategy-id str_xxx --symbol 600519.SH --symbol 000858.SZ --start 2024-01-01 --end 2024-04-30
```

目前回测周期为日线；通常省略 `--timeframe`，需要显式传时只传 `--timeframe 1d`。

## 常用参数

- `--symbol`：标的代码。单只股票策略只传一个。
- `--timeframe`：周期，目前只支持 `1d`，通常省略。
- `--start` / `--end`：回测日期区间。
- `--cash`：初始资金。
- `--commission`：手续费率。
- `--slippage`：滑点比例。
- `--benchmark-symbol`：基准代码；不需要基准时可以省略。
- `--note`：回测备注。

## 查看回测记录

查看当前项目的回测记录列表，不按策略过滤：

```text
backtest list --limit 20
```

按策略版本过滤记录，只能传 `--strategy-version-id stv_xxx`：

```text
backtest list --strategy-version-id stv_xxx --limit 20
```

如果手里只有策略 ID `str_xxx`，先查看版本，再用返回的 `stv_xxx` 查回测记录：

```text
strategy versions --strategy-id str_xxx
backtest list --strategy-version-id stv_xxx --limit 20
```

不要把策略 ID 当作 `backtest list` 的位置参数，也不要给 list 传 `--strategy-id`：

```text
错误：backtest list str_xxx
错误：backtest list --strategy-id str_xxx
正确：backtest list --strategy-version-id stv_xxx
```

查看单次回测详情：

```text
backtest show --backtest-id sbt_xxx
```

查看交易执行明细：

```text
backtest trades --backtest-id sbt_xxx --start 2024-01-01 --end 2024-04-30 --limit 100
```

按标的和时间过滤交易明细：

```text
backtest trades --backtest-id sbt_xxx --symbol 600519.SH --start 2024-01-01 --end 2024-04-30 --limit 100
```

查看权益曲线点位，默认从头返回：

```text
backtest equity --backtest-id sbt_xxx --start 2024-01-01 --end 2024-04-30 --limit 120
```

查看权益曲线末尾点位：

```text
backtest equity --backtest-id sbt_xxx --start 2024-01-01 --end 2024-04-30 --tail --limit 120
```

## 结果处理

回测完成后记录 `backtest_id`，并关注：

- 回测状态。
- 总收益、年化收益、最大回撤、夏普比率、交易次数。
- 需要逐笔执行记录时使用 `backtest trades`，可加 `--start` / `--end` 过滤交易时间，不要依赖 `backtest show`。
- 需要权益曲线点位时使用 `backtest equity`，可加 `--start` / `--end` 过滤曲线日期，不要依赖 `backtest show`。
- 失败时的 `failure_code`、`failure_message` 和详细错误。
