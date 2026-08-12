# Security Notes

## Secrets

- `.env` is intentionally ignored by Git and excluded from the distribution ZIP.
- Only the human account owner should enter `JUPYTER_TOKEN`.
- Do not put credentials in MCP arguments, prompts, screenshots, logs, client JSON, issue reports, or shell command arguments.
- `scripts/launch_mcp.py` reads only four approved keys from `.env`; unrelated variables are ignored.
- Existing process environment variables override `.env`, allowing an approved secret manager to inject credentials.
- `doctor.py` reports only whether a token exists and hides the Jupyter user path.

If a token is exposed, revoke it at the provider and issue a new one. Deleting it from Git history or chat does not make the old token safe.

## Tool risk levels

- Lower risk: `list_kernels`, dedicated intraday tools.
- Stateful: `create_kernel`, `interrupt_kernel`.
- Destructive: `delete_kernel`.
- Local/remote file access: `sync_files`, `download_files`.
- Arbitrary execution: `execute_code`.

The intraday tools read market data but may create a remote Jupyter session and kernel. `execute_code` can read credentials available in the remote kernel, modify files, make network requests, or place trades if the remote account exposes trading APIs. Require explicit human approval for any such action.

## Distribution checks

Before sending a rebuilt archive:

1. Confirm it contains no `.env`, `.credentials.json`, `.venv`, cache, log, result, or notebook output.
2. Search text for real tokens, Authorization headers and personal absolute paths.
3. Rebuild `MANIFEST.sha256`.
4. Extract the ZIP in a temporary directory and rerun tests there.
