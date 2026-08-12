# MCP Tool Reference

The server exposes exactly nine tools over stdio. Optional `url` and `token` parameters exist for compatibility, but clients should omit them and let `scripts/run_mcp.*` load `.env`.

| Tool | Required arguments | Effect |
| --- | --- | --- |
| `list_kernels` | none | Read active remote kernels |
| `create_kernel` | none | Create a remote kernel; defaults to `python3` |
| `execute_code` | `kernel_id`, `code` | Execute arbitrary remote Python |
| `interrupt_kernel` | `kernel_id` | Interrupt remote execution |
| `delete_kernel` | `kernel_id` | Delete a remote kernel session |
| `sync_files` | none | Read a local tree and write it to Jupyter |
| `download_files` | none | Read Jupyter files and write them locally |
| `stock_intraday_realtime` | `stockcode`, `trade_date` | Query one A-share's 1-minute bars; may create a kernel |
| `stock_intraday_realtime_batch` | `stockcodes`, `trade_date` | Query a small list of A-shares; may create a kernel |

## Kernel tools

`create_kernel` accepts `kernel_name="python3"` and optional `path`. `execute_code` accepts `timeout=120.0` and returns `stdout`, `stderr`, `result`, `error`, and captured image paths. Images are written to temporary files on the computer running the MCP server.

`execute_code` has the same effective authority as the remote Jupyter user. It is not a sandbox.

## File tools

`sync_files` arguments:

```json
{
  "local_path": "/absolute/local/source",
  "remote_path": "project/target",
  "dry_run": true
}
```

Always run with `dry_run=true` first. The synchronizer honors `.gitignore` and skips common cache, virtual environment and dependency directories. UTF-8 files are sent as text; binary files are base64 encoded.

`download_files` arguments:

```json
{
  "remote_path": "project/result",
  "local_path": "/absolute/local/download-target"
}
```

It supports files and recursive directories. Remote paths containing `..` are rejected, and partial files are removed after failed downloads.

## Single-stock intraday tool

```json
{
  "stockcode": "000001.SZ",
  "trade_date": "20260710",
  "end_time": "10:30"
}
```

- `stockcode` accepts a six-digit code with or without `.SH`, `.SZ`, or `.BJ`.
- Plain codes beginning with `6` map to Shanghai; `8` or `9` map to Beijing; the rest map to Shenzhen.
- `trade_date` uses `YYYYMMDD`.
- `end_time` should use `HH:MM`. Historical dates default to `15:00`. The current day follows Shanghai trading time, including the lunch break.

The result includes `rows` with `open`, `high`, `low`, `close`, `volume`, and `amount`, plus a summary with last price, session high/low, total volume and total amount. MindGo's remote `turnover` field is normalized to `amount`.

## Batch intraday tool

```json
{
  "stockcodes": ["000001.SZ", "600000.SH"],
  "trade_date": "20260710",
  "end_time": "11:30"
}
```

The result contains one item per normalized symbol. The implementation has no hard input cap, but it is designed for a small decision set. Split large universes into controlled batches to avoid remote load and timeouts.
