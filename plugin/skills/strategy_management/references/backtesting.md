# 策略回测

## 执行入口

所有命令从仓库根目录执行：

```bash
uv run python -m cli.chatq_strategy <command>
```

不要传 API base URL。连接地址由项目配置读取。

## 默认回测当前版本

不传版本 ID 时，回测当前策略版本：

```bash
uv run python -m cli.chatq_strategy backtest "$STRATEGY_ID" \
  --symbol 600519.SH \
  --start 2024-01-01 \
  --end 2024-04-30 \
  --cash 100000 \
  --commission 0.001 \
  --slippage 0.0002
```

执行工具会自动推断策略模式，不要传 `--mode`。

## 指定版本回测

需要对比历史版本时传 `--version`：

```bash
uv run python -m cli.chatq_strategy backtest "$STRATEGY_ID" \
  --version "$VERSION_ID" \
  --symbol 600519.SH \
  --start 2024-01-01 \
  --end 2024-04-30
```

## 运行时参数覆盖

只用 `--param key=value` 覆盖源码协议中已注册的参数：

```bash
uv run python -m cli.chatq_strategy backtest "$STRATEGY_ID" \
  --symbol 600519.SH \
  --start 2024-01-01 \
  --end 2024-04-30 \
  --param buy_drop_pct=0.10 \
  --param sell_rise_pct=0.20 \
  --param step_pct=0.10
```

不要用 `--param` 传策略参数 schema。

## 市场和资产类型

对于单只 A 股股票回测，`market=CN`、`asset_class=stock` 是默认值，通常省略。

只有用户明确要求其他市场或资产类型时再传：

```bash
--market HK --asset-class stock
--market US --asset-class stock
--market CN --asset-class etf
--market CN --asset-class index
```

不支持的市场和资产类型组合会导致行情数据源错误。

## 常用配置

- `--symbol`：标的代码。单只股票策略只传一个。
- `--start` / `--end`：回测日期区间。
- `--cash`：初始资金。
- `--commission`：手续费率。
- `--slippage`：滑点比例。
- `--benchmark-symbol`：基准代码；不需要基准时可以省略。
- `--note`：回测备注。

## 查看回测记录

查看记录列表：

```bash
uv run python -m cli.chatq_strategy backtests \
  --version "$VERSION_ID" \
  --limit 20
```

查看单次回测详情：

```bash
uv run python -m cli.chatq_strategy backtest-show "$BACKTEST_ID"
```

## 结果处理

回测完成后记录 `backtest_id`，并关注：

- 回测状态。
- 总收益、年化收益、最大回撤、夏普比率、交易次数。
- 失败时的 `failure_code`、`failure_message` 和详细错误。
