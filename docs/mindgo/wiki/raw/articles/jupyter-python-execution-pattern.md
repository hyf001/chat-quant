---
source_url: local extracted method from portable Jupyter case
ingested: 2026-08-11
sha256: 3b8c5610880ce9e8fcb55fb1ee5e9ae42151776544a2ba60bb95e9906f65b500
---

# Remote Jupyter Python execution pattern for MindGo data

This source is distilled from the portable Jupyter access case bundled in the MindGo materials. The knowledge base only keeps the data-access method: execute Python inside an authorized remote MindGo / SuperMind Jupyter kernel.

## Required remote capabilities

- A valid Jupyter base URL, including the user base path.
- A valid token and authentication scheme, normally Bearer.
- Permission to use Jupyter kernels, sessions, contents and WebSocket channels.
- A remote Python kernel where MindGo runtime functions such as get_price, get_all_securities, get_fundamentals and get_arsenal_api are available.

## Jupyter API surfaces used by the method

- GET /api/kernels to inspect kernels.
- POST /api/kernels or POST /api/sessions to create a Python kernel/session.
- /api/kernels/{id}/channels WebSocket to send execute_request messages and read stdout/stderr/results.
- /api/contents/{path} to upload or download files when a script needs local/remote exchange.

## Data-access idea

1. Create or reuse a remote Python kernel.
2. Send a Python code string that imports pandas/json, calls MindGo functions, normalizes the result to JSON-serializable records, and prints the JSON between explicit start/end markers.
3. Parse stdout locally and convert the marker payload to rows, summaries or DataFrames.

## Safety boundary

Remote Python execution has the authority of the Jupyter account. Keep tokens out of prompts and logs. Treat arbitrary code execution, file writes, file deletion and trading functions as high-risk actions that need explicit user approval.
