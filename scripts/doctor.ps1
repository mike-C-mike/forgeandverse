$ErrorActionPreference = "Continue"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$Failures = 0

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

function Test-Tool {
    param(
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][scriptblock]$Check
    )

    try {
        $Result = & $Check
        Write-Host ("[OK] {0}: {1}" -f $Name, $Result) -ForegroundColor Green
    }
    catch {
        Write-Host ("[MISSING] {0}: {1}" -f $Name, $_.Exception.Message) -ForegroundColor Red
        $script:Failures++
    }
}

Test-Tool "Git" {
    $Command = Get-Command git.exe -ErrorAction Stop
    (& $Command.Source --version).Trim()
}

Test-Tool "Python" {
    $Command = Get-Command python.exe -ErrorAction Stop
    (& $Command.Source --version).Trim()
}

Test-Tool "PyYAML" {
    $Command = Get-Command python.exe -ErrorAction Stop
    if (-not (Test-PythonModule -PythonPath $Command.Source -Module "yaml")) {
        throw "Not installed. Run: python -m pip install -r .\scripts\requirements.txt"
    }
    (& $Command.Source -c "import yaml; print(yaml.__version__)" 2>$null).Trim()
}

Test-Tool "Hugo Extended" {
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
        $Command = Get-Command hugo.exe -ErrorAction Stop
        $Hugo = $Command.Source
    }
    $Version = (& $Hugo version).Trim()
    if ($Version -notmatch "extended") {
        throw "Hugo is installed but is not the Extended build"
    }
    $Version
}

if ($Failures -gt 0) {
    Write-Host ("Doctor found {0} missing requirement(s)." -f $Failures) -ForegroundColor Yellow
    exit 1
}

Write-Host "Forge & Verse development environment is ready." -ForegroundColor Cyan
