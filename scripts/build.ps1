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
if (-not $Python) {
    throw "Python was not found. Install Python and run: python -m pip install -r .\scripts\requirements.txt"
}

if (-not (Test-PythonModule -PythonPath $Python.Source -Module "yaml")) {
    throw "PyYAML is not installed. Run: python -m pip install -r .\scripts\requirements.txt"
}

Invoke-CheckedNative -FilePath $Python.Source -Arguments @((Join-Path $PSScriptRoot "test_validate_public.py"))
Invoke-CheckedNative -FilePath $Python.Source -Arguments @((Join-Path $PSScriptRoot "validate_hygiene.py"))
Invoke-CheckedNative -FilePath $Python.Source -Arguments @((Join-Path $PSScriptRoot "build_release_ledger.py"))
Invoke-CheckedNative -FilePath $Python.Source -Arguments @((Join-Path $PSScriptRoot "validate.py"))
Invoke-CheckedNative -FilePath $Hugo -Arguments @(
    "--source", $RepoRoot,
    "--gc",
    "--minify",
    "--cleanDestinationDir",
    "--logLevel", "info"
)
Invoke-CheckedNative -FilePath $Python.Source -Arguments @((Join-Path $PSScriptRoot "validate_public.py"))

Write-Host "Build completed: $RepoRoot\public" -ForegroundColor Green
