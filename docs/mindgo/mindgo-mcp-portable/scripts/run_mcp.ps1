$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $Root ".venv\Scripts\python.exe"

if (-not (Test-Path $Python)) {
    [Console]::Error.WriteLine("MindGo MCP is not installed. Run scripts\setup.ps1 first.")
    exit 2
}

& $Python (Join-Path $Root "scripts\launch_mcp.py")
exit $LASTEXITCODE
