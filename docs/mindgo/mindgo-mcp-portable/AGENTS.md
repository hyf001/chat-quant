# Agent Entry Point

This directory is a portable MindGo / SuperMind MCP server. Its MCP transport is stdio. It connects to a remote Jupyter server and exposes kernel management, code execution, file transfer, and A-share 1-minute intraday data tools.

## Required order of work

1. Read `README.md`.
2. Read `docs/REMOTE_REQUIREMENTS.md` and confirm the human has a valid MindGo Jupyter account.
3. Run the platform setup script.
4. Run the no-credential protocol smoke test.
5. Ask the human to create `.env` from `.env.example` and enter their own credentials. Never search the computer, shell history, browser storage, or unrelated files for credentials.
6. Run `doctor.py --live`, then the credentialed smoke test.
7. Register `scripts/run_mcp.sh` or `scripts/run_mcp.ps1` in the requested MCP client.

## Commands

macOS/Linux:

```bash
chmod +x scripts/*.sh
./scripts/setup.sh
cp .env.example .env
# Human edits .env
.venv/bin/python scripts/doctor.py --live
.venv/bin/python scripts/smoke_test.py --live
```

Windows PowerShell:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\setup.ps1
Copy-Item .env.example .env
# Human edits .env
.\.venv\Scripts\python.exe .\scripts\doctor.py --live
.\.venv\Scripts\python.exe .\scripts\smoke_test.py --live
```

Optional market-data acceptance test:

```bash
.venv/bin/python scripts/smoke_test.py --live \
  --stockcode 000001.SZ --trade-date 20260710 --end-time 10:00
```

Use a real trading date available to the account. The same arguments work on Windows.

## Safety rules

- Never print, log, commit, archive, or send `.env`, `JUPYTER_TOKEN`, Authorization headers, WebSocket token query parameters, or a real credential file.
- Do not pass `url` or `token` as MCP tool arguments; let the launcher provide environment variables.
- `execute_code` runs arbitrary code in the remote Jupyter account. Explain the code and obtain confirmation before destructive, trading, network, or long-running actions.
- Run `sync_files` with `dry_run=true` first.
- Confirm before `delete_kernel`, overwriting files, or downloading into a non-empty directory.
- Do not write ordinary logs to MCP stdout. stdio stdout is reserved for protocol messages.

## Completion criteria

The installation is complete only when:

- all unit tests pass;
- `scripts/smoke_test.py --protocol --launcher` reports all 9 expected tools;
- `scripts/doctor.py --live` reaches the remote Jupyter API;
- `scripts/smoke_test.py --live` successfully calls `list_kernels`;
- the target MCP client lists the `mindgo` server and its tools;
- no secret has been copied outside `.env` or the user's approved secret store.

For schemas and side effects, read `docs/TOOLS.md`. For errors, read `docs/TROUBLESHOOTING.md`. For credential handling, read `docs/SECURITY.md`.
