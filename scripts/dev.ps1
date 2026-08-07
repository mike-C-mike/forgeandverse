param(
    [int]$Port = 1314
)

$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")

function Test-PythonModule {
    param(
        [Parameter(Mandatory = $true)][string]$PythonPath,
        [Parameter(Mandatory = $true)][string]$Module
    )

    $StdOut = [System.IO.Path]::GetTempFileName()
    $StdErr = [System.IO.Path]::GetTempFileName()
    try {
        $Arguments = "-c `"import $Module`""
        $Process = Start-Process -FilePath $PythonPath `
            -ArgumentList $Arguments `
            -Wait `
            -PassThru `
            -NoNewWindow `
            -RedirectStandardOutput $StdOut `
            -RedirectStandardError $StdErr
        return ($Process.ExitCode -eq 0)
    }
    finally {
        Remove-Item $StdOut, $StdErr -Force -ErrorAction SilentlyContinue
    }
}

function Invoke-CheckedNative {
    param(
        [Parameter(Mandatory = $true)][string]$FilePath,
        [Parameter(Mandatory = $true)][string[]]$Arguments
    )

    $PreviousPreference = $ErrorActionPreference
    try {
        $ErrorActionPreference = "Continue"
        & $FilePath @Arguments
        $ExitCode = $LASTEXITCODE
    }
    finally {
        $ErrorActionPreference = $PreviousPreference
    }

    if ($ExitCode -ne 0) {
        exit $ExitCode
    }
}

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
    if (Test-PythonModule -PythonPath $Python.Source -Module "yaml") {
        Invoke-CheckedNative -FilePath $Python.Source -Arguments @((Join-Path $PSScriptRoot "validate_hygiene.py"))
        Invoke-CheckedNative -FilePath $Python.Source -Arguments @((Join-Path $PSScriptRoot "build_release_ledger.py"))
        Invoke-CheckedNative -FilePath $Python.Source -Arguments @((Join-Path $PSScriptRoot "validate.py"))
    }
    else {
        Write-Warning "PyYAML is not installed, so repository validation was skipped. Run: python -m pip install -r .\scripts\requirements.txt"
    }
}
else {
    Write-Warning "Python was not found, so repository validation was skipped."
}

Write-Host "Starting Forge & Verse on http://localhost:$Port/" -ForegroundColor Cyan
$PreviousPreference = $ErrorActionPreference
try {
    $ErrorActionPreference = "Continue"
    & $Hugo server `
        --source $RepoRoot `
        --port $Port `
        --disableFastRender `
        --ignoreCache `
        --noHTTPCache `
        --buildDrafts `
        --buildFuture
    $ExitCode = $LASTEXITCODE
}
finally {
    $ErrorActionPreference = $PreviousPreference
}

if ($ExitCode -ne 0) {
    exit $ExitCode
}
