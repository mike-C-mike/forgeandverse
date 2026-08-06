$ErrorActionPreference = "Stop"
$Script = Join-Path $PSScriptRoot "build_release_ledger.py"
$Python = Get-Command python.exe -ErrorAction SilentlyContinue
if (-not $Python) { throw "Python was not found on PATH." }
& $Python.Source $Script
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "Release ledger rebuilt." -ForegroundColor Green
