$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

$PythonCommand = Get-Command python -ErrorAction SilentlyContinue
if (-not $PythonCommand) {
    throw "Python 3.11+ is required and must be available as 'python'."
}

& $PythonCommand.Source -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 'Python 3.11+ is required')"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$UvCommand = Get-Command uv -ErrorAction SilentlyContinue
if ($UvCommand) {
    Write-Host "Installing locked dependencies with uv..."
    & $UvCommand.Source sync --extra dev --locked
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
} else {
    Write-Host "uv not found; using Python venv + pip fallback."
    & $PythonCommand.Source -m venv .venv
    $VenvPython = Join-Path $Root ".venv\Scripts\python.exe"
    & $VenvPython -m pip install --upgrade pip
    & $VenvPython -m pip install -e ".[dev]"
}

if (-not (Test-Path (Join-Path $Root ".env"))) {
    Copy-Item (Join-Path $Root ".env.example") (Join-Path $Root ".env")
    Write-Host "Created .env from the secret-free template. Replace its placeholders before live tests."
}

$VenvPython = Join-Path $Root ".venv\Scripts\python.exe"
Write-Host "Running unit tests..."
& $VenvPython -m pytest tests -q
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Running credential-free MCP protocol test..."
& $VenvPython scripts\smoke_test.py --protocol --launcher
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Setup complete. Edit $Root\.env, then run:"
Write-Host "  .\.venv\Scripts\python.exe .\scripts\doctor.py --live"
Write-Host "  .\.venv\Scripts\python.exe .\scripts\smoke_test.py --live"
