param(
    [int]$Port = 1314
)

$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")

$Candidates = @(
    (Join-Path $RepoRoot "hugo.exe"),
    (Join-Path $RepoRoot "..\hugo.exe")
)

$Hugo = $null
foreach ($Candidate in $Candidates) {
    if (Test-Path $Candidate) {
        $Hugo = (Resolve-Path $Candidate).Path
        break
    }
}

if (-not $Hugo) {
    $Command = Get-Command hugo.exe -ErrorAction SilentlyContinue
    if ($Command) { $Hugo = $Command.Source }
}

if (-not $Hugo) {
    throw "Hugo Extended was not found in the repository, its parent folder, or PATH."
}

$Python = Get-Command python.exe -ErrorAction SilentlyContinue
if ($Python) {
    & $Python.Source -c "import yaml" 2>$null
    if ($LASTEXITCODE -eq 0) {
        & $Python.Source (Join-Path $PSScriptRoot "build_release_ledger.py")
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
        & $Python.Source (Join-Path $PSScriptRoot "validate.py")
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    } else {
        Write-Warning "PyYAML is not installed, so repository validation was skipped. Run: python -m pip install -r .\scripts\requirements.txt"
    }
}

Write-Host "Starting Forge & Verse on http://localhost:$Port/" -ForegroundColor Cyan
& $Hugo server `
    --source $RepoRoot `
    --port $Port `
    --disableFastRender `
    --ignoreCache `
    --noHTTPCache `
    --buildDrafts `
    --buildFuture
