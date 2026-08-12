# Troubleshooting

## Setup cannot find Python

Install Python 3.11 or newer and make `python3` (macOS/Linux) or `python` (Windows) available in the terminal. Delete a partially created `.venv` before retrying if its Python version is wrong.

## Dependency installation fails

- Confirm the computer can reach the Python package index.
- Prefer `uv sync --extra dev --locked` for reproducible versions.
- Behind a corporate proxy, configure the approved proxy/CA settings for `uv` or `pip`.
- Do not copy another computer's `.venv`; virtual environments are not portable.

## Protocol test passes but live test fails

This means the local MCP server is healthy and the problem is configuration or remote access. Run:

```bash
.venv/bin/python scripts/doctor.py --live
```

Check `.env`, token validity, the full Jupyter user base path, firewall/proxy rules, and WebSocket support.

## HTTP 401 or 403

The token is invalid, expired, using the wrong authentication scheme, or lacks Jupyter API permissions. Obtain a new authorized token; do not print the old one for debugging.

## Jupyter works but intraday data fails

- Confirm `MINDGO_INTRADAY_NOTEBOOK_PATH` matches the remote workspace.
- Confirm the remote kernel exposes MindGo `get_price` and `pandas`.
- Use a valid A-share code and an available trading date.
- Try a small single-stock request before a batch request.
- Confirm the account's data permissions include the requested date and instrument.

## WebSocket connection fails

The Jupyter REST API and kernel WebSocket are separate paths. A proxy may allow `/api/kernels` but block `/api/kernels/{id}/channels`. Preserve the user base path and confirm that `wss://` traffic is allowed.

## MCP client cannot start the server

- Use an absolute launcher path in client configuration.
- Run the launcher manually from a terminal and inspect stderr only.
- Ensure setup created `.venv` inside the extracted bundle.
- On macOS/Linux, run `chmod +x scripts/*.sh`.
- On Windows, use the provided PowerShell command and allow scripts for the current process.
- Restart the MCP client after editing its configuration.

## Client sees fewer or more than nine tools

Run `scripts/smoke_test.py --protocol --launcher`. If that passes, the client may be using a different MCP configuration or cached tool catalog. Remove duplicate registrations and restart the client.
