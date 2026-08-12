# MindGo MCP Portable Bundle

Portable stdio MCP server for a remote MindGo / SuperMind Jupyter environment. The bundle contains source code, locked Python dependencies, tests, cross-platform launchers, Agent instructions, and diagnostics. It contains no credentials.

## What you need

- macOS, Linux, or Windows
- Python 3.11 or newer
- Internet access during dependency installation
- Preferably `uv`; standard `venv` + `pip` is used as a fallback
- A valid MindGo / SuperMind Jupyter URL and token
- A remote environment where the proprietary MindGo `get_price` API is available for market-data tools

Read `docs/REMOTE_REQUIREMENTS.md` before starting. Agents must read `AGENTS.md` first.

## 1. Unzip and install

macOS/Linux:

```bash
unzip mindgo-mcp-portable-*.zip
cd mindgo-mcp-portable
chmod +x scripts/*.sh
./scripts/setup.sh
```

Windows PowerShell:

```powershell
Expand-Archive .\mindgo-mcp-portable-*.zip -DestinationPath .
Set-Location .\mindgo-mcp-portable
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\setup.ps1
```

Setup installs dependencies, creates `.env` from the template when missing, runs unit tests, and verifies the MCP protocol. The placeholder `.env` is not a valid live configuration yet.

## 2. Add your own credentials

Open `.env` and replace the placeholders:

```dotenv
JUPYTER_URL=https://your-jupyter-server.example/user/your-user
JUPYTER_TOKEN=your-own-token
JUPYTER_AUTH_SCHEME=Bearer
MINDGO_INTRADAY_NOTEBOOK_PATH=deepsolo_v3/少标的分时实时.ipynb
```

Do not send `.env` to an Agent or commit it. Let the human enter secrets locally.

## 3. Verify the remote service

macOS/Linux:

```bash
.venv/bin/python scripts/doctor.py --live
.venv/bin/python scripts/smoke_test.py --live
```

Windows:

```powershell
.\.venv\Scripts\python.exe .\scripts\doctor.py --live
.\.venv\Scripts\python.exe .\scripts\smoke_test.py --live
```

The first command verifies configuration and Jupyter connectivity without displaying the token. The second starts the MCP server over stdio and calls `list_kernels` through the MCP protocol.

To verify MindGo minute bars, use a trading date available to your account:

```bash
.venv/bin/python scripts/smoke_test.py --live \
  --stockcode 000001.SZ \
  --trade-date 20260710 \
  --end-time 10:00
```

## 4. Register with Codex

Use an absolute path to the launcher. The launcher loads `.env`, so the token does not need to be copied into Codex configuration.

macOS/Linux:

```bash
codex mcp add mindgo -- /ABSOLUTE/PATH/mindgo-mcp-portable/scripts/run_mcp.sh
codex mcp list
codex mcp get mindgo
```

Windows:

```powershell
codex mcp add mindgo -- powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\ABSOLUTE\PATH\mindgo-mcp-portable\scripts\run_mcp.ps1
codex mcp list
```

Restart the MCP client after registration if it does not immediately refresh tools.

## 5. Register with a JSON MCP client

Copy the relevant template from `configs/`, replace only `<ABSOLUTE_PATH>`, and merge the `mindgo` entry into the client's MCP configuration. Do not put token values in the client JSON.

## Verification levels

| Level | Credentials | What it proves |
| --- | --- | --- |
| Unit tests | No | Package logic and local file operations |
| `--protocol --launcher` smoke test | No | actual launcher, stdio startup, MCP initialize and all 9 tool schemas |
| `doctor.py --live` | Yes | Jupyter URL, authentication and REST API reachability |
| `smoke_test.py --live` | Yes | End-to-end MCP call to remote Jupyter |
| Stock smoke test | Yes | Remote MindGo `get_price` and intraday normalization |

## Package map

```text
AGENTS.md                    Agent entry point and completion rules
README.md                    Human quick start
.env.example                Secret-free configuration template
configs/                    MCP client configuration templates
docs/                       Tools, remote requirements, security, troubleshooting
scripts/setup.*             Cross-platform installation
scripts/run_mcp.*           MCP client launchers
scripts/doctor.py           Safe local/remote diagnostics
scripts/smoke_test.py       MCP protocol and live acceptance tests
supermind_mcp/              MCP server source
tests/                      Unit tests
pyproject.toml / uv.lock    Package metadata and locked dependencies
MANIFEST.sha256             File integrity checksums
```

## Important limitation

This bundle provides the MCP bridge, not a MindGo account or the proprietary MindGo runtime. A recipient without valid Jupyter credentials and `get_price` access can validate the local MCP protocol but cannot retrieve live or historical MindGo market data.

## License

MIT. See `LICENSE`.
