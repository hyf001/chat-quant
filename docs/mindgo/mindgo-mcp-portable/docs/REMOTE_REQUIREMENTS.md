# Remote MindGo Requirements

The MCP server is only a bridge. The remote MindGo / SuperMind environment must satisfy these requirements before live calls can pass.

## Required account information

Obtain these values from the MindGo/SuperMind account owner or administrator:

- Jupyter base URL, including any user base path;
- a currently valid API token;
- authentication scheme, normally `Bearer`;
- permission to use the Jupyter kernels, sessions, contents, and WebSocket APIs.

Do not ask an Agent to discover credentials from browser data, shell history, other projects, or hidden files.

## Required Jupyter APIs

The server uses:

- `GET /api/kernels`
- `POST /api/kernels`
- `POST /api/kernels/{id}/interrupt`
- `DELETE /api/kernels/{id}`
- `GET /api/sessions`
- `POST /api/sessions`
- `/api/kernels/{id}/channels` WebSocket
- `/api/contents/{path}` for upload and download

The configured `JUPYTER_URL` must retain the full user base path. For example, if the Jupyter UI opens under `/user/alice`, do not configure only the domain root.

## Market-data requirements

The tools `stock_intraday_realtime` and `stock_intraday_realtime_batch` execute Python inside the remote kernel. That kernel must provide:

- `get_price` in the notebook runtime;
- `pandas`;
- permission to query the requested A-share instruments and dates.

The default notebook/session path is:

```text
deepsolo_v3/少标的分时实时.ipynb
```

If the account uses another path, set `MINDGO_INTRADAY_NOTEBOOK_PATH` in `.env`. `doctor.py --live` checks whether the path exists. The MCP may create a Jupyter session/kernel for the configured path, so an intraday query is read-only with respect to market data but may create remote session state.

## Credential acquisition is not included

This archive deliberately contains no real URL, token, account identifier, or remote notebook. A recipient without an authorized MindGo account can still install the package, run unit tests, and verify the MCP tool catalog, but cannot complete live acceptance tests.
